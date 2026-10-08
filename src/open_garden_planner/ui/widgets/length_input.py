"""Modal physical-length input without changing canonical command units."""

from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QInputDialog, QMessageBox

from open_garden_planner.core.units import format_length, parse_length
from open_garden_planner.ui.widgets.length_spin_box import widget_units


def get_length(parent, title: str, label: str, value: float,
               minimum: float, maximum: float, decimals: int = 2) -> tuple[float, bool]:
    """Return cm and acceptance. Metric retains the native numeric dialog."""
    units = widget_units(parent)
    if not units.imperial:
        return QInputDialog.getDouble(parent, title, label, value, minimum, maximum, decimals)
    text, accepted = QInputDialog.getText(
        parent, title, label.replace("(cm)", "(ft/in)"), text=format_length(value, units)
    )
    if not accepted:
        return value, False
    try:
        result = parse_length(text, units)
        if not minimum <= result <= maximum:
            raise ValueError("Outside physical range")
    except ValueError:
        QMessageBox.warning(parent, title, QCoreApplication.translate(
            "CreativePreview", "Enter a length within the allowed range, such as 10' 6 1/2\" or 10.5 ft."
        ))
        return value, False
    return result, True
