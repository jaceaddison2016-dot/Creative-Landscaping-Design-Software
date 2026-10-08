"""Project display units. Geometry and command values always remain centimeters."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction

INCH_CM = 2.54
FOOT_CM = 30.48
SQUARE_FOOT_CM2 = FOOT_CM ** 2
CUBIC_YARD_CM3 = (3 * FOOT_CM) ** 3


class UnitSystem(StrEnum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class LengthFormat(StrEnum):
    FEET_INCHES = "feet_inches"
    DECIMAL_FEET = "decimal_feet"


@dataclass(frozen=True)
class DisplayUnits:
    system: UnitSystem = UnitSystem.METRIC
    length_format: LengthFormat = LengthFormat.FEET_INCHES

    @property
    def imperial(self) -> bool:
        return self.system == UnitSystem.IMPERIAL

    def to_dict(self) -> dict[str, str]:
        return {"system": self.system.value, "length_format": self.length_format.value}

    @classmethod
    def from_dict(cls, data: object) -> DisplayUnits:
        # Missing/unknown preferences must not reinterpret legacy geometry.
        if not isinstance(data, dict):
            return cls()
        try:
            return cls(UnitSystem(data.get("system", "metric")),
                       LengthFormat(data.get("length_format", "feet_inches")))
        except (ValueError, TypeError):
            return cls()


METRIC = DisplayUnits()
IMPERIAL = DisplayUnits(UnitSystem.IMPERIAL)


def units_for(source: object | None) -> DisplayUnits:
    """Read an explicit scene/project preference; never use process-global units."""
    units = getattr(source, "display_units", METRIC)
    return units if isinstance(units, DisplayUnits) else METRIC


_NUMBER = r"(?:\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d*)?|\.\d+)"
_FEET = re.compile(rf"^({_NUMBER})\s*(?:ft|feet|foot|')\s*(?:({_NUMBER})\s*(?:in|inches|inch|\")?)?$")
_SINGLE = re.compile(rf"^({_NUMBER})\s*(mm|cm|m|ft|feet|foot|'|in|inch|inches|\")?$")


def _number(text: str) -> float:
    parts = text.split()
    value = sum(float(Fraction(part)) for part in parts)
    if not math.isfinite(value):
        raise ValueError("Length must be finite")
    return value


def parse_length(text: str, units: DisplayUnits = METRIC) -> float:
    """Return cm. Bare numbers mean cm in metric, feet in imperial.

    Explicit cm/m/mm/ft/in always override the project unit. Fractions and mixed
    inches are accepted. A leading minus applies to the entire length. Imperial
    coordinate pairs must use a comma or semicolon, preserving component spaces.
    """
    value = text.strip().lower().replace("′", "'").replace("’", "'").replace("″", '"').replace(chr(0x2212), "-")
    sign = -1 if value.startswith("-") else 1
    value = value.removeprefix("-").removeprefix("+").strip()
    try:
        match = _FEET.fullmatch(value)
        if match:
            result = sign * (_number(match[1]) * FOOT_CM + _number(match[2] or "0") * INCH_CM)
            if not math.isfinite(result):
                raise ValueError("Length must be finite")
            return result
        match = _SINGLE.fullmatch(value)
        if not match:
            raise ValueError("Invalid length")
        unit = match[2] or ("ft" if units.imperial else "cm")
        factor = {"mm": .1, "cm": 1., "m": 100., "ft": FOOT_CM,
                  "feet": FOOT_CM, "foot": FOOT_CM, "'": FOOT_CM,
                  "in": INCH_CM, "inch": INCH_CM, "inches": INCH_CM, '"': INCH_CM}[unit]
        result = sign * _number(match[1]) * factor
        if not math.isfinite(result):
            raise ValueError("Length must be finite")
        return result
    except (ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Invalid length") from exc


def format_length(cm: float, units: DisplayUnits = METRIC, *, metric_auto: bool = True) -> str:
    if not units.imperial:
        return f"{cm / 100:.2f} m" if metric_auto and abs(cm) >= 100 else f"{cm:.1f} cm"
    if units.length_format == LengthFormat.DECIMAL_FEET:
        return f"{cm / FOOT_CM:.4f} ft"
    # Display to nearest 1/64 inch. Rounding is never written into geometry.
    ticks = int(math.floor(abs(cm) / INCH_CM * 64 + .5))
    feet, ticks = divmod(ticks, 12 * 64)
    inches, numerator = divmod(ticks, 64)
    fraction = f" {Fraction(numerator, 64)}" if numerator else ""
    sign = "-" if cm < 0 and ticks + feet * 768 else ""
    return f'{sign}{feet}\' {inches}{fraction}"'


def format_area(cm2: float, units: DisplayUnits = METRIC) -> str:
    if units.imperial:
        return f"{cm2 / SQUARE_FOOT_CM2:.2f} ft²"
    return f"{cm2 / 10000:.2f} m²" if abs(cm2) >= 10000 else f"{cm2:.1f} cm²"


def format_dimension(cm: float, units: DisplayUnits = METRIC) -> str:
    return format_length(cm, units) if units.imperial else f"{cm / 100:.2f} m"


def format_volume(cm3: float, units: DisplayUnits = METRIC) -> str:
    return f"{cm3 / CUBIC_YARD_CM3:.3f} yd³" if units.imperial else f"{cm3 / 1000:.1f} L"
