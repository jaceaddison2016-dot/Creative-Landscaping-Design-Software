"""New Project dialog for creating projects with specified dimensions."""

from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)

from open_garden_planner.core.units import METRIC
from open_garden_planner.ui.widgets.length_spin_box import LengthSpinBox


class NewProjectDialog(QDialog):
    """Dialog for creating a new project with specified canvas dimensions.

    Allows the user to specify width and height in meters, which are
    converted to centimeters for internal use.
    """

    # Default canvas size in meters
    DEFAULT_WIDTH_M = 50.0
    DEFAULT_HEIGHT_M = 30.0

    # Limits in meters
    MIN_SIZE_M = 1.0
    MAX_SIZE_M = 1000.0

    def __init__(self, parent: object = None, *, display_units=None) -> None:
        """Initialize the New Project dialog.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.display_units = display_units or getattr(parent, "default_new_project_units", METRIC)

        self.setWindowTitle(self.tr("New Project"))
        self.setModal(True)
        self.setMinimumWidth(350)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)

        # Canvas dimensions group
        dimensions_group = QGroupBox(self.tr("Canvas Dimensions"))
        dimensions_layout = QFormLayout(dimensions_group)

        # Width input
        width_layout = QHBoxLayout()
        self.width_spinbox = self._dimension_spin(self.DEFAULT_WIDTH_M)
        width_layout.addWidget(self.width_spinbox)
        width_layout.addStretch()
        dimensions_layout.addRow(self.tr("Width:"), width_layout)

        # Height input
        height_layout = QHBoxLayout()
        self.height_spinbox = self._dimension_spin(self.DEFAULT_HEIGHT_M)
        height_layout.addWidget(self.height_spinbox)
        height_layout.addStretch()
        dimensions_layout.addRow(self.tr("Height:"), height_layout)

        layout.addWidget(dimensions_group)

        # Garden year group
        year_group = QGroupBox(self.tr("Garden Year"))
        year_layout = QVBoxLayout(year_group)

        self._year_checkbox = QCheckBox(self.tr("Assign a year to this plan"))
        self._year_checkbox.setChecked(False)
        year_layout.addWidget(self._year_checkbox)

        year_spin_layout = QHBoxLayout()
        self._year_spinbox = QSpinBox()
        self._year_spinbox.setRange(2000, 2100)
        self._year_spinbox.setValue(date.today().year)
        self._year_spinbox.setMinimumWidth(100)
        self._year_spinbox.setEnabled(False)
        year_spin_layout.addWidget(self._year_spinbox)
        year_spin_layout.addStretch()
        year_layout.addLayout(year_spin_layout)

        self._year_checkbox.toggled.connect(self._year_spinbox.setEnabled)

        layout.addWidget(year_group)

        # Info label
        info_label = QLabel(
            self.tr("Tip: You can resize the canvas later from Edit > Canvas Size.")
        )
        info_label.setProperty("secondary", True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # Add some spacing
        layout.addSpacing(10)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _dimension_spin(self, default_m: float) -> QDoubleSpinBox:
        factor = 100 if self.display_units.imperial else 1
        spin = LengthSpinBox(unit_source=self) if self.display_units.imperial else QDoubleSpinBox()
        spin.setRange(self.MIN_SIZE_M * factor, self.MAX_SIZE_M * factor)
        spin.setDecimals(6 if self.display_units.imperial else 1)
        spin.setValue(default_m * factor)
        spin.setSuffix("" if self.display_units.imperial else " m")
        spin.setMinimumWidth(180 if self.display_units.imperial else 120)
        return spin

    @property
    def width_cm(self) -> float:
        """Get the canvas width in centimeters."""
        return self.width_spinbox.value() * (1 if self.display_units.imperial else 100.0)

    @property
    def height_cm(self) -> float:
        """Get the canvas height in centimeters."""
        return self.height_spinbox.value() * (1 if self.display_units.imperial else 100.0)

    @property
    def width_m(self) -> float:
        """Get the canvas width in meters."""
        return self.width_cm / 100

    @property
    def height_m(self) -> float:
        """Get the canvas height in meters."""
        return self.height_cm / 100

    @property
    def garden_year(self) -> int | None:
        """Get the selected garden year, or None if the year checkbox is unchecked."""
        if self._year_checkbox.isChecked():
            return self._year_spinbox.value()
        return None

    def set_dimensions_m(self, width_m: float, height_m: float) -> None:
        """Set the canvas dimensions in meters.

        Args:
            width_m: Width in meters
            height_m: Height in meters
        """
        self.set_dimensions_cm(width_m * 100, height_m * 100)

    def set_dimensions_cm(self, width_cm: float, height_cm: float) -> None:
        """Set the canvas dimensions in centimeters.

        Args:
            width_cm: Width in centimeters
            height_cm: Height in centimeters
        """
        factor = 1 if self.display_units.imperial else 100.0
        self.width_spinbox.setValue(width_cm / factor)
        self.height_spinbox.setValue(height_cm / factor)
