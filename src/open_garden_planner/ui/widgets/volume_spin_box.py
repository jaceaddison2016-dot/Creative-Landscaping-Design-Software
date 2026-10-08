"""Soil volume editor: canonical litres, optional cubic-yard presentation."""

import math

from PyQt6.QtGui import QValidator
from PyQt6.QtWidgets import QDoubleSpinBox

from open_garden_planner.core.units import CUBIC_YARD_CM3, format_volume
from open_garden_planner.ui.widgets.length_spin_box import widget_units


class VolumeSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, *, unit_source=None):
        self._unit_source = unit_source or parent
        self._display_units = widget_units(self._unit_source)
        super().__init__(parent)
        self.setKeyboardTracking(False)

    def setDecimals(self, decimals: int) -> None:  # noqa: N802
        super().setDecimals(6 if self._display_units.imperial else decimals)

    def setSuffix(self, suffix: str) -> None:  # noqa: N802
        super().setSuffix("" if self._display_units.imperial else suffix)

    def textFromValue(self, value: float) -> str:  # noqa: N802
        units = self._display_units
        return format_volume(value * 1000, units) if units.imperial else super().textFromValue(value)

    def valueFromText(self, text: str) -> float:  # noqa: N802
        if not self._display_units.imperial:
            return super().valueFromText(text)
        if text.strip() == self.textFromValue(self.value()):
            return self.value()
        value = text.strip().lower()
        litres = value.endswith("l")
        number = value.removesuffix("l") if litres else value.removesuffix("yd³").removesuffix("yd3")
        result = float(number) * (1 if litres else CUBIC_YARD_CM3 / 1000)
        if not math.isfinite(result):
            raise ValueError("Volume must be finite")
        return result

    def validate(self, text: str, position: int):
        if not self._display_units.imperial:
            return super().validate(text, position)
        try:
            value = self.valueFromText(text)
            state = QValidator.State.Acceptable if self.minimum() <= value <= self.maximum() else QValidator.State.Intermediate
        except ValueError:
            state = QValidator.State.Intermediate
        return state, text, position
