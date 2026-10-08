"""A physical-length editor whose value/signals remain in canonical cm."""

from PyQt6.QtCore import QSignalBlocker
from PyQt6.QtGui import QValidator
from PyQt6.QtWidgets import QDoubleSpinBox

from open_garden_planner.core.units import (
    METRIC,
    DisplayUnits,
    format_length,
    parse_length,
    units_for,
)


def widget_units(source: object | None) -> DisplayUnits:
    """Resolve a widget's explicit project without sharing state across windows."""
    while source is not None:
        units = units_for(source)
        if hasattr(source, "display_units"):
            return units
        scene = getattr(source, "canvas_scene", None)
        if scene is not None:
            return units_for(scene)
        items = getattr(source, "_current_items", [])
        if items:
            return units_for(items[0].scene())
        scene_method = getattr(source, "scene", None)
        if callable(scene_method):
            return units_for(scene_method())
        parent = getattr(source, "parent", None)
        source = parent() if callable(parent) else None
    return METRIC


class LengthSpinBox(QDoubleSpinBox):
    """Metric behavior stays native; imperial entry accepts explicit fractions.

    Stored values have six cm decimals in imperial. Display rounds to 1/64 inch;
    simply changing display units never writes that rounding back to a project.
    """

    def __init__(self, parent=None, *, unit_source=None):
        self._unit_source = unit_source if unit_source is not None else parent
        self._display_units = widget_units(self._unit_source)
        super().__init__(parent)
        self.setKeyboardTracking(False)

    def setDecimals(self, decimals: int) -> None:  # noqa: N802
        self._requested_decimals = decimals
        super().setDecimals(6 if self._display_units.imperial else decimals)

    def setSuffix(self, suffix: str) -> None:  # noqa: N802
        self._metric_suffix = suffix
        super().setSuffix("" if self._display_units.imperial else suffix)

    def set_display_units(self, units: DisplayUnits) -> None:
        if units == self._display_units:
            return
        blocker = QSignalBlocker(self)
        self._display_units = units
        super().setDecimals(6 if units.imperial else getattr(self, "_requested_decimals", 2))
        super().setSuffix("" if units.imperial else getattr(self, "_metric_suffix", ""))
        del blocker

    def textFromValue(self, value: float) -> str:  # noqa: N802
        units = getattr(self, "_display_units", METRIC)
        return format_length(value, units) if units.imperial else super().textFromValue(value)

    def valueFromText(self, text: str) -> float:  # noqa: N802
        units = self._display_units
        if not units.imperial:
            return super().valueFromText(text)
        stripped = text.removeprefix(self.prefix()).removesuffix(self.suffix())
        if stripped.strip() == self.textFromValue(self.value()):
            return self.value()  # untouched rounded display is not an edit
        return parse_length(stripped, units)

    def validate(self, text: str, position: int):
        units = getattr(self, "_display_units", METRIC)
        if not units.imperial:
            return super().validate(text, position)
        try:
            cm = parse_length(text.removeprefix(self.prefix()), units)
            state = QValidator.State.Acceptable if self.minimum() <= cm <= self.maximum() else QValidator.State.Intermediate
        except ValueError:
            state = QValidator.State.Intermediate
        return state, text, position

    def stepBy(self, steps: int) -> None:  # noqa: N802
        if self._display_units.imperial:
            self.setValue(self.value() + steps * 2.54)  # one inch per arrow
        else:
            super().stepBy(steps)
