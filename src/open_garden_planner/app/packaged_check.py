"""Opt-in prototype QA using real Qt controls in the running packaged app.

Invoked only by --prototype-check OUTPUT in an isolated CI/development account.
Normal startup never imports QtTest or changes user preferences for this probe.
All generated projects are synthetic and confined to the supplied output folder.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path


def configure_probe() -> None:
    """Keep the probe's settings, recents and cache apart from normal accounts."""
    from open_garden_planner.app import settings
    from open_garden_planner.ui.theme import ThemeMode

    settings.ORGANIZATION_NAME = "Creative Prototype QA"
    settings.APPLICATION_NAME = "Packaged workflow checks"
    settings._settings_instance = None
    settings.create_qsettings().clear()
    prefs = settings.get_settings()
    prefs.show_welcome_on_startup = False
    prefs.agent_api_enabled = False
    prefs.download_plant_images = False
    prefs.language = "en"
    prefs.theme_mode = ThemeMode.LIGHT


def schedule_probe(app, window, output: Path) -> None:
    """Observe only after QApplication exists and the normal editor has shown."""
    from PyQt6.QtCore import QTimer

    def run() -> None:
        report = {"status": "FAIL", "run_id": os.environ.get("CREATIVE_PROBE_RUN_ID")}
        try:
            output.mkdir(parents=True, exist_ok=True)
            report.update(exercise_window(app, window, output))
            report["status"] = "PASS"
            code = 0
        except Exception:
            report["traceback"] = traceback.format_exc()
            code = 2
        try:
            (output / "result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        finally:
            # A filesystem failure must not strand a GUI child in the event
            # loop. The external driver rejects a missing report.
            window._project_manager.mark_clean()
            window.close()
            app.exit(code)

    QTimer.singleShot(500, run)


def exercise_window(app, window, output: Path) -> dict:
    """Draw, type, undo, save/reopen and export inside the actual executable."""
    import ezdxf
    from PyQt6.QtCore import QPointF, Qt, qVersion
    from PyQt6.QtGui import QFontInfo
    from PyQt6.QtTest import QTest

    from open_garden_planner.app.creative_preview import CreativePreviewWindow
    from open_garden_planner.core.object_types import ObjectType
    from open_garden_planner.core.tools import ToolType
    from open_garden_planner.core.units import IMPERIAL
    from open_garden_planner.services.dxf_service import DxfExportService
    from open_garden_planner.services.export_service import ExportService
    from open_garden_planner.services.pdf_report_service import PdfReportOptions, PdfReportService
    from open_garden_planner.ui.canvas.items import CircleItem, RectangleItem
    from open_garden_planner.ui.creative_preview import CreativeWelcomeDialog
    from open_garden_planner.ui.icons import get_icon
    from open_garden_planner.ui.widgets.length_spin_box import LengthSpinBox

    def require(condition: bool, description: str) -> None:
        if not condition:
            raise AssertionError(description)

    def close_to(actual: float, expected: float) -> bool:
        return math.isclose(actual, expected, abs_tol=1e-6)

    def type_text(widget, text: str) -> None:
        widget.setFocus()
        QTest.keyClick(widget, Qt.Key.Key_A, Qt.KeyboardModifier.ControlModifier)
        QTest.keyClicks(widget, text)
        QTest.keyClick(widget, Qt.Key.Key_Return)
        QTest.qWait(120)

    def click_scene(point: QPointF) -> None:
        pixel = window.canvas_view.mapFromScene(point)
        require(window.canvas_view.viewport().rect().contains(pixel), "Drawing point must be visible")
        QTest.mouseClick(window.canvas_view.viewport(), Qt.MouseButton.LeftButton, pos=pixel)
        QTest.qWait(100)

    require(isinstance(window, CreativePreviewWindow), "Normal executable must open Creative")
    require("Creative Landscape Studio" in window.windowTitle(), "Creative title missing")
    window.showNormal()
    window.resize(1440, 900)
    window.reset_workspace()
    window._new_project_document(width_cm=2438.4, height_cm=1828.8)
    window.canvas_view.fit_in_view()
    QTest.qWait(150)
    require(window.canvas_scene.display_units == IMPERIAL, "New project must default to imperial")
    require(close_to(window.canvas_view.grid_size, 30.48), "One-foot grid missing")

    # Two typed corners traverse the normal coordinate field, tool dispatcher,
    # rectangle creation command and cm serializer. CAD Y inversion is explicit.
    window._on_tool_selected(ToolType.RECTANGLE)
    type_text(window.coordinate_input_field, "10 ft,-10 ft")
    type_text(window.coordinate_input_field, "30 ft,-22 ft")
    patios = [item for item in window.canvas_scene.items() if isinstance(item, RectangleItem)]
    require(len(patios) == 1, "Typed drawing did not create one rectangle")
    patio = patios[0]
    require(close_to(patio.rect().width(), 609.6), "20-foot drawn width is wrong")
    require(close_to(patio.rect().height(), 365.76), "12-foot drawn height is wrong")

    # Activate a bundled gallery row and place a real tree using viewport clicks.
    type_text(window.library.search, "Round Deciduous")
    require(window.library.items.count() == 1, "Bundled plant library missing")
    row = window.library.items.item(0)
    QTest.mouseClick(window.library.items.viewport(), Qt.MouseButton.LeftButton,
                     pos=window.library.items.visualItemRect(row).center())
    click_scene(QPointF(1524, 914.4))
    click_scene(QPointF(1706.88, 914.4))
    trees = [item for item in window.canvas_scene.items()
             if isinstance(item, CircleItem) and item.object_type == ObjectType.TREE]
    require(len(trees) == 1, "Mouse drawing did not place the bundled tree")

    window._on_tool_selected(ToolType.SELECT)
    click_scene(patio.mapToScene(patio.rect().center()))
    window._sidebar_controller.set_selection_pinned("properties", True)
    QTest.qWait(150)
    fields = window.properties_panel.findChildren(LengthSpinBox)
    width = next(field for field in fields if close_to(field.value(), 609.6))
    require("20'" in width.text(), "Imperial property text missing")
    type_text(width.lineEdit(), "10' 6 1/2\"")
    require(close_to(patio.rect().width(), 321.31), "Fractional inch edit has wrong physical size")
    require(close_to(patio.rect().height(), 365.76), "Width edit changed untouched height")
    window.canvas_view.setFocus()
    QTest.keyClick(window.canvas_view, Qt.Key.Key_Z, Qt.KeyboardModifier.ControlModifier)
    QTest.qWait(100)
    require(close_to(patio.rect().width(), 609.6), "Packaged Ctrl+Z failed")
    QTest.keyClick(window.canvas_view, Qt.Key.Key_Y, Qt.KeyboardModifier.ControlModifier)
    QTest.qWait(100)
    require(close_to(patio.rect().width(), 321.31), "Packaged Ctrl+Y failed")
    require(all(width.fontMetrics().inFont(char) for char in "0123456789'\"/²³"),
            "Measurement font glyphs missing")
    control_font = QFontInfo(width.font()).family()
    patio_id = patio.item_id
    project = output / "imperial-roundtrip.ogp"
    window._save_to_file(project)
    require(project.is_file() and not window._project_manager.is_dirty, "Project save failed")
    window._load_project_file(str(project))
    patio = next(item for item in window.canvas_scene.items() if getattr(item, "item_id", None) == patio_id)
    require(close_to(patio.rect().width(), 321.31), "Reopen lost fractional inch geometry")
    require(window.canvas_scene.display_units == IMPERIAL, "Reopen lost project units")
    patio.setSelected(True)
    QTest.qWait(150)
    require(window.grab().save(str(output / "imperial-properties.png")),
            "Native imperial properties screenshot failed")

    ExportService.export_to_png(window.canvas_scene, output / "physical.png")
    PdfReportService.generate(window.canvas_scene, PdfReportOptions(), output / "physical.pdf")
    DxfExportService.export(window.canvas_scene, output / "physical.dxf")
    ExportService.export_plant_list_to_csv(window.canvas_scene, output / "physical.csv")
    require((output / "physical.png").read_bytes().startswith(b"\x89PNG"), "PNG export failed")
    require((output / "physical.pdf").read_bytes().startswith(b"%PDF-"), "PDF export failed")
    drawing = ezdxf.readfile(output / "physical.dxf")
    require(drawing.header["$INSUNITS"] == 2, "Imperial DXF must declare feet")
    rect_entity = next(entity for entity in drawing.modelspace() if entity.dxftype() == "LWPOLYLINE")
    xs = [point[0] for point in rect_entity.get_points()]
    require(close_to(max(xs) - min(xs), 10 + 6.5 / 12), "DXF physical width is wrong")
    with (output / "physical.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1 and "position_x_ft" in rows[0], "Imperial plant CSV is wrong")
    tree = next(item for item in window.canvas_scene.items() if isinstance(item, CircleItem))
    require(close_to(float(rows[0]["position_x_ft"]), tree.mapToScene(tree.rect().center()).x() / 30.48),
            "CSV physical position is wrong")

    icons = {}
    for name in ("file_save", "tree", "sun", "select"):
        icon = get_icon(name)
        require(icon is not None and not icon.isNull() and not icon.pixmap(24, 24).isNull(),
                f"Bundled icon unavailable: {name}")
        icons[name] = True
    require(not app.windowIcon().isNull(), "Bundled application icon missing")

    # Optional approved sample is copied by the external driver into this
    # synthetic check directory; the original repository file is never written.
    sample = output / "approved-sample.ogp"
    if sample.is_file():
        window._load_project_file(str(sample))
    else:
        window._project_manager.set_location({"latitude": 42.1, "longitude": -86.48, "name": "QA sample"})
    window._sun_toolbar.set_datetime_local(datetime(2026, 6, 21, 16, 0))
    if not window._sun_sim_action.isChecked():
        window._sun_sim_action.trigger()
    QTest.qWait(350)
    require(window._sun_controller.state == "active", "Live geometric shade did not activate")
    window._workspace_combo.setCurrentIndex(0)
    window.library.search.clear()
    window.canvas_view.fit_in_view()
    QTest.qWait(150)
    require(window.grab().save(str(output / "editor.png")), "Native editor screenshot failed")
    window._workspace_combo.setCurrentIndex(1)
    QTest.qWait(150)
    require(window.grab().save(str(output / "sun-study.png")), "Native sun screenshot failed")
    welcome = CreativeWelcomeDialog(window)
    welcome.show()
    QTest.qWait(100)
    require(welcome.grab().save(str(output / "welcome.png")), "Native welcome screenshot failed")
    welcome.close()
    return {
        "frozen": bool(getattr(sys, "frozen", False)), "executable": sys.executable,
        "os": os.name, "qt": qVersion(), "platform_plugin": app.platformName(),
        "control_font": control_font, "icons": icons,
        "imperial_width_cm": 321.31, "dxf_width_ft": max(xs) - min(xs),
        "checks": ["typed drawing", "mouse plant placement", "fractional inch property edit",
                   "Ctrl+Z/Ctrl+Y", "save/reopen", "PNG/PDF/DXF/CSV", "fonts/icons", "live sun/shade"],
        "sun_computer_zone": datetime.now().astimezone().tzname(),
        "human_manual_test": "not performed", "gpu_3d_test": "not performed",
    }
