"""Physical reference measurements across the actual Creative desktop workflow."""

import csv
import json
from unittest.mock import MagicMock

import ezdxf
import pytest
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QGroupBox, QMessageBox

from open_garden_planner.app.creative_preview import CreativePreviewWindow
from open_garden_planner.app.settings import get_settings
from open_garden_planner.core.display_commands import SetGridSpacingCommand
from open_garden_planner.core.object_types import ObjectType
from open_garden_planner.core.project import ProjectManager
from open_garden_planner.core.tools import ToolType
from open_garden_planner.core.tools.constraint_tool import DistanceInputDialog
from open_garden_planner.core.units import IMPERIAL, METRIC, DisplayUnits, LengthFormat, UnitSystem
from open_garden_planner.services.dxf_service import DxfExportService
from open_garden_planner.services.export_service import ExportService
from open_garden_planner.services.shopping_list_service import ShoppingListService
from open_garden_planner.ui.canvas.items import CircleItem, RectangleItem
from open_garden_planner.ui.dialogs.calibration_dialog import CalibrationDialog
from open_garden_planner.ui.dialogs.new_project_dialog import NewProjectDialog
from open_garden_planner.ui.widgets.length_spin_box import LengthSpinBox
from open_garden_planner.ui.widgets.volume_spin_box import VolumeSpinBox


@pytest.fixture
def window(qtbot, monkeypatch):
    get_settings().show_welcome_on_startup = False
    monkeypatch.setattr(QMessageBox, "question", lambda *_a, **_k: QMessageBox.StandardButton.Discard)
    win = CreativePreviewWindow()
    qtbot.addWidget(win)
    win.showNormal()
    win.resize(1440, 900)
    yield win
    win._project_manager.mark_clean()
    win.close()


def enter(spin, text, qtbot):
    spin.lineEdit().setText(text)
    qtbot.keyClick(spin.lineEdit(), Qt.Key.Key_Return)


def test_default_new_project_and_fractional_property_edit_undo(window, qtbot):
    dialog = NewProjectDialog(window)
    qtbot.addWidget(dialog)
    enter(dialog.width_spinbox, "80 ft", qtbot)
    assert dialog.width_cm == pytest.approx(2438.4)
    window._new_project_document(width_cm=2438.4, height_cm=1828.8)
    assert window.canvas_scene.display_units == IMPERIAL
    assert window.canvas_view.grid_size == pytest.approx(30.48)
    patio = RectangleItem(200, 200, 609.6, 365.76, object_type=ObjectType.TERRACE_PATIO, name="Patio")
    window.canvas_scene.addItem(patio)
    patio.setSelected(True)
    window.properties_panel.set_selected_items([patio])
    fields = window.properties_panel.findChildren(LengthSpinBox)
    width = next(field for field in fields if field.value() == 609.6)
    assert '20\'' in width.text()
    enter(width, '10\' 6 1/2"', qtbot)
    assert patio.rect().width() == pytest.approx(321.31)
    assert window._project_manager.is_dirty
    window.canvas_view.setFocus()
    window._on_undo()
    assert patio.rect().width() == pytest.approx(609.6)
    window._on_redo()
    assert patio.rect().width() == pytest.approx(321.31)
    assert {group.title() for group in window.properties_panel.findChildren(QGroupBox)} >= {
        "Essentials", "Appearance", "Advanced"}


def test_typed_negative_fractional_coordinates_and_polar_input(window, qtbot):
    window.canvas_view.set_active_tool(ToolType.FENCE)
    tool = window.canvas_view.active_tool
    tool.commit_typed_coordinate(QPointF(100, 100))
    window.canvas_view.refresh_input_anchor()
    field = window.coordinate_input_field
    text = '@-1 ft,-3/8 in'
    field.setText(text)
    field.textEdited.emit(text)
    qtbot.keyClick(field, Qt.Key.Key_Return)
    assert tool.last_point.x() == pytest.approx(69.52)
    assert tool.last_point.y() == pytest.approx(100.9525)  # CAD Y inversion
    window.canvas_view.refresh_input_anchor()
    text = '@10.5<0'
    field.setText(text)
    field.textEdited.emit(text)
    qtbot.keyClick(field, Qt.Key.Key_Return)
    assert tool.last_point.x() == pytest.approx(389.56)


def test_switching_units_focus_and_save_reopen_do_not_drift(window, qtbot, tmp_path):
    item = RectangleItem(200.123456, 300.987654, 321.123456, 198.654321, name="Precise")
    window.canvas_scene.addItem(item)
    item.setSelected(True)
    window.properties_panel.set_selected_items([item])
    baseline = ProjectManager()._serialize_item(item)
    # Focus and finish an untouched rounded inch display: must retain cm exactly.
    for spin in window.properties_panel.findChildren(LengthSpinBox):
        spin.interpretText()
    for _ in range(8):
        for units in (METRIC, DisplayUnits(UnitSystem.IMPERIAL, LengthFormat.DECIMAL_FEET), IMPERIAL):
            window._change_units(units)
    assert ProjectManager()._serialize_item(item) == baseline
    window.canvas_view.command_manager.execute(SetGridSpacingCommand(window.canvas_view, 15.24))
    file = tmp_path / "precise.ogp"
    window._save_to_file(file)
    assert json.loads(file.read_text())["display_units"]["system"] == "imperial"
    window._load_project_file(str(file))
    loaded = next(obj for obj in window.canvas_scene.items() if getattr(obj, "name", "") == "Precise")
    assert ProjectManager()._serialize_item(loaded) == baseline
    assert window.canvas_view.grid_size == pytest.approx(15.24)
    assert not window._project_manager.is_dirty
    # Old documents with no additive preferences retain metric display/geometry.
    data = json.loads(file.read_text())
    data.pop("display_units")
    data.pop("presentation")
    file.write_text(json.dumps(data))
    window._load_project_file(str(file))
    assert window.canvas_scene.display_units == METRIC
    assert ProjectManager()._serialize_item(next(obj for obj in window.canvas_scene.items() if getattr(obj, "name", "") == "Precise")) == baseline


def test_calibration_constraint_and_soil_volume_inputs(window, qtbot):
    dialog = CalibrationDialog(QPixmap(200, 100), window)
    qtbot.addWidget(dialog)
    dialog._on_point_clicked(QPointF(0, 0))
    dialog._on_point_clicked(QPointF(100, 0))
    dialog._distance_input.setText("20 ft")
    pixels, cm = dialog.get_calibration_data()
    assert cm / pixels == pytest.approx(6.096)
    constraint = DistanceInputDialog(609.6, window.canvas_view)
    qtbot.addWidget(constraint)
    enter(constraint._spin, '2\' 11 15/16"', qtbot)
    assert constraint.distance_cm() == pytest.approx(91.28125)
    volume = VolumeSpinBox(unit_source=window)
    qtbot.addWidget(volume)
    volume.setRange(0, 10000)
    volume.setDecimals(1)
    enter(volume, "1 yd3", qtbot)
    assert volume.value() == pytest.approx(764.554858)


def test_dxf_csv_exports_contain_feet_without_mutating_geometry(window, tmp_path):
    patio = RectangleItem(30.48, 60.96, 609.6, 365.76, name="Patio")
    window.canvas_scene.addItem(patio)
    before = ProjectManager()._serialize_item(patio)
    dxf = tmp_path / "plan.dxf"
    DxfExportService.export(window.canvas_scene, dxf)
    doc = ezdxf.readfile(dxf)
    assert doc.header["$INSUNITS"] == 2
    points = list(next(iter(doc.modelspace().query("LWPOLYLINE"))).get_points())
    assert max(point[0] for point in points) - min(point[0] for point in points) == pytest.approx(20)
    assert max(point[1] for point in points) - min(point[1] for point in points) == pytest.approx(12)
    assert ProjectManager()._serialize_item(patio) == before
    plant = CircleItem(.9525, 30.48, 15.24, object_type=ObjectType.SHRUB, name="Shrub")
    window.canvas_scene.addItem(plant)
    csv_path = tmp_path / "plants.csv"
    assert ExportService.export_plant_list_to_csv(window.canvas_scene, csv_path) == 1
    with csv_path.open(newline="") as stream:
        row = next(csv.DictReader(stream))
    assert float(row["position_x_ft"]) == pytest.approx(.03125)
    assert "position_x_cm" not in row
    window._change_units(METRIC)
    ExportService.export_plant_list_to_csv(window.canvas_scene, csv_path)
    with csv_path.open(newline="") as stream:
        metric_row = next(csv.DictReader(stream))
    assert float(metric_row["position_x_cm"]) == pytest.approx(.95)
    assert float(metric_row["position_y_cm"]) == pytest.approx(30.48)
    DxfExportService.export(window.canvas_scene, dxf)
    assert ezdxf.readfile(dxf).header["$INSUNITS"] == 5


def test_material_quantities_and_prices_remain_physically_equivalent(window):
    bed = RectangleItem(0, 0, 304.8, 304.8, object_type=ObjectType.GARDEN_BED,
                        metadata={"soil_depth_cm": 30.48})
    window.canvas_scene.addItem(bed)
    soil = MagicMock()
    soil.get_effective_record.return_value = None
    service = ShoppingListService(window.canvas_scene, soil, window._project_manager)
    rows = {row.id: row for row in service.build()}
    assert rows["soil_fill:m3"].unit == "yd³"
    assert rows["soil_fill:m3"].quantity == pytest.approx(100 / 27, abs=.001)
    assert rows["mulch:m2"].quantity == pytest.approx(100, abs=.1)
    service.update_price(rows["soil_fill:m3"], 50)
    cost = rows["soil_fill:m3"].total_cost
    window._change_units(METRIC)
    metric = next(row for row in service.build() if row.id == "soil_fill:m3")
    assert metric.total_cost == pytest.approx(cost)


def test_workspaces_symbols_and_shortcuts_retain_editor_capabilities(window, qtbot):
    assert not window.main_toolbar.isVisible()
    assert window.creative_actions.isVisible()
    window._workspace_combo.setCurrentIndex(1)
    assert window._sun_toolbar.isVisible()
    window._workspace_combo.setCurrentIndex(0)
    assert window._sun_toolbar.isHidden()
    assert window._sun_sim_action.isChecked()  # shadows can remain on the plan
    # Existing calendar shortcut can reveal the optional Gardening workspace.
    window._tab_widget.setCurrentIndex(1)
    assert window._workspace_combo.currentIndex() == 2
    assert window._tab_widget.isTabVisible(1)
    window._workspace_combo.setCurrentIndex(0)
    plant = CircleItem(300, 300, 90, object_type=ObjectType.TREE, name="Tree")
    window.canvas_scene.addItem(plant)
    before = ProjectManager()._serialize_item(plant)
    bounds = plant.sceneBoundingRect()
    window._set_presentation("detailed")
    assert ProjectManager()._serialize_item(plant) == before and plant.sceneBoundingRect() == bounds
    window._on_undo()
    assert window.canvas_scene.plant_symbol_style == "architectural"
    assert ProjectManager()._serialize_item(plant) == before
    QApplication.processEvents()


def test_presentation_refresh_preserves_custom_material_and_pen_on_reopen(window, tmp_path):
    from PyQt6.QtGui import QColor, QPen

    item = RectangleItem(100, 100, 609.6, 365.76, object_type=ObjectType.TERRACE_PATIO, name="Custom patio")
    item.fill_color = QColor("#d6ccb9")
    item._setup_styling()
    item.setPen(QPen(QColor("#392f28"), 3.75))
    window.canvas_scene.addItem(item)
    before = window._project_manager._serialize_item(item)
    window.canvas_scene.set_presentation("detailed", .1)
    assert item.fill_color.name() == "#d6ccb9"
    assert item.pen().color().name() == "#392f28"
    assert item.pen().widthF() == 3.75
    path = tmp_path / "materials.ogp"
    window._save_to_file(path)
    window._load_project_file(str(path))
    loaded = next(obj for obj in window.canvas_scene.items() if getattr(obj, "name", "") == "Custom patio")
    assert window._project_manager._serialize_item(loaded) == before
    loaded.setSelected(True)
    window.properties_panel.set_selected_items([loaded])
    from PyQt6.QtWidgets import QComboBox
    types = window.properties_panel.findChildren(QComboBox)
    assert any(combo.currentData() == ObjectType.TERRACE_PATIO for combo in types)


def test_normal_entrypoint_opens_the_actual_creative_editor(tmp_path):
    import os
    import subprocess
    import sys

    script = '''
from PyQt6 import QtWebEngineWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from open_garden_planner.app import settings
settings.ORGANIZATION_NAME = "creative_main_test"
settings.APPLICATION_NAME = "Isolated Creative Startup"
settings.get_settings().show_welcome_on_startup = False
settings.get_settings().agent_api_enabled = False
from open_garden_planner.app.creative_preview import CreativePreviewWindow
from open_garden_planner.main import main
def inspect():
    app = QApplication.instance()
    window = next(w for w in app.topLevelWidgets() if isinstance(w, CreativePreviewWindow))
    assert window.isVisible()
    assert "Creative Landscape Studio" in window.windowTitle()
    assert window.canvas_scene.display_units.imperial
    assert window.creative_actions.isVisible()
    assert not window.main_toolbar.isVisible()
    print("CREATIVE_MAIN_OK", flush=True)
    window._project_manager.mark_clean()
    window.close()
    app.quit()
original_show = CreativePreviewWindow.show
def monitored_show(window):
    original_show(window)
    def checked():
        try:
            inspect()
        except BaseException:
            import traceback
            traceback.print_exc()
            QApplication.instance().exit(2)
    QTimer.singleShot(1500, checked)
CreativePreviewWindow.show = monitored_show
raise SystemExit(main())
'''
    environment = {**os.environ, "QT_QPA_PLATFORM": "offscreen",
                   "XDG_CONFIG_HOME": str(tmp_path / "config"),
                   "XDG_DATA_HOME": str(tmp_path / "data"),
                   "XDG_CACHE_HOME": str(tmp_path / "cache")}
    result = subprocess.run([sys.executable, "-c", script], env=environment,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CREATIVE_MAIN_OK" in result.stdout
