"""Run/capture the real desktop editor with an explicitly experimental design.

Normal `python -m open_garden_planner` remains unchanged. Settings, recents and
autosave use a separate preview account. Only synthetic plans are generated.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

# Required before QApplication, exactly as in the application's entry point.
from PyQt6 import QtWebEngineWidgets  # noqa: F401
from PyQt6.QtCore import QPointF, QTimer, qVersion
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication

from open_garden_planner.app import settings as app_settings
from open_garden_planner.app.application import GardenPlannerApp
from open_garden_planner.app.creative_preview import CreativePreviewWindow
from open_garden_planner.core.constraints import AnchorRef
from open_garden_planner.core.fill_patterns import FillPattern
from open_garden_planner.core.i18n import load_translator
from open_garden_planner.core.measure_snapper import AnchorType
from open_garden_planner.core.object_types import ObjectType
from open_garden_planner.core.project import ProjectManager
from open_garden_planner.core.units import FOOT_CM, IMPERIAL
from open_garden_planner.models.layer import Layer
from open_garden_planner.ui.canvas.canvas_scene import CanvasScene
from open_garden_planner.ui.canvas.items import CircleItem, PolygonItem, RectangleItem, TextItem
from open_garden_planner.ui.creative_preview import CreativeWelcomeDialog
from open_garden_planner.ui.creative_theme import apply_creative_theme
from open_garden_planner.ui.dialogs.welcome_dialog import WelcomeDialog
from open_garden_planner.ui.theme import ThemeMode, apply_theme

ROOT = Path(__file__).resolve().parents[1]


def make_landscape_fixture(path: Path) -> None:
    """An editable plan, saved through the inherited serializer, not painted UI art."""
    scene = CanvasScene(80 * FOOT_CM, 60 * FOOT_CM)
    scene.set_display_units(IMPERIAL)
    scene.grid_spacing_cm = FOOT_CM
    scene.set_presentation("architectural", .3)
    ground = scene.active_layer.id
    structures = Layer(name="Structures & hardscape", z_order=1)
    planting = Layer(name="Planting", z_order=2)
    annotations = Layer(name="Labels", z_order=3)
    for layer in (structures, planting, annotations):
        scene.add_layer(layer)
    items = [
        RectangleItem(80, 80, 2240, 1640, object_type=ObjectType.LAWN,
                      name="Lawn", layer_id=ground),
        RectangleItem(850, 1150, 800, 500, object_type=ObjectType.HOUSE,
                      name="Residence", layer_id=structures.id),
        RectangleItem(900, 740, 20 * FOOT_CM, 12 * FOOT_CM, object_type=ObjectType.TERRACE_PATIO,
                      name="Patio", layer_id=structures.id),
        RectangleItem(1580, 100, 300, 640, object_type=ObjectType.DRIVEWAY,
                      name="Driveway", layer_id=structures.id),
        RectangleItem(1240, 100, 100, 640, object_type=ObjectType.TERRACE_PATIO,
                      name="Walk", layer_id=structures.id),
        PolygonItem([QPointF(510 + 340 * math.cos(t), 520 + 230 * math.sin(t) + 40 * math.sin(2*t))
                     for t in (i * 2 * math.pi / 48 for i in range(48))],
                    object_type=ObjectType.GARDEN_BED, name="Curved planting bed", layer_id=ground),
        RectangleItem(1680, 1210, 440, 300, object_type=ObjectType.GARDEN_BED,
                      name="Foundation planting", layer_id=ground),
        CircleItem(1260, 940, 80, object_type=ObjectType.TABLE_ROUND,
                   name="Table", layer_id=structures.id),
        CircleItem(350, 1250, 160, object_type=ObjectType.TREE,
                   name="Shade tree", metadata={"object_height_cm": 650}, layer_id=planting.id),
        CircleItem(2040, 820, 130, object_type=ObjectType.TREE,
                   name="Ornamental tree", metadata={"object_height_cm": 450}, layer_id=planting.id),
    ]
    for x, y in ((380, 380), (570, 420), (760, 410), (370, 610), (570, 650),
                 (1780, 1350), (1950, 1350), (2080, 1350)):
        items.append(CircleItem(x, y, 70, object_type=ObjectType.SHRUB,
                                name="Shrub", layer_id=planting.id))
    for x, y in ((260, 490), (300, 580), (720, 590), (760, 520), (1930, 1260)):
        items.append(CircleItem(x, y, 36, object_type=ObjectType.PERENNIAL,
                                name="Perennial", layer_id=planting.id))
    for x, y in ((980, 920), (1480, 920), (1260, 1070)):
        items.append(RectangleItem(x, y, 55, 55, object_type=ObjectType.CHAIR,
                                   name="Chair", layer_id=structures.id))
    for x, y, text in ((980, 1530, "RESIDENCE"), (995, 790, "PATIO  20 ft x 12 ft"),
                       (1010, 460, "OPEN LAWN"), (170, 1550, "N  ↑")):
        items.append(TextItem(x, y, text, font_size=0.9, layer_id=annotations.id))
    for item in items:
        # Synthetic sample styling via existing item properties, not a new
        # renderer or changes to other users' object styles/artwork.
        if getattr(item, "object_type", None) == ObjectType.LAWN:
            item.fill_pattern = FillPattern.SOLID
            item.fill_color = QColor("#60E7EDD9")
        scene.addItem(item)
    patio = next(item for item in items if item.name == "Patio")
    scene.constraint_graph.add_constraint(
        AnchorRef(patio.item_id, AnchorType.CORNER, 0),
        AnchorRef(patio.item_id, AnchorType.CORNER, 1), 20 * FOOT_CM)
    scene.update_dimension_lines()
    manager = ProjectManager()
    manager.set_location({"latitude": 42.1, "longitude": -86.48, "name": "Southwest Michigan (synthetic)"})
    manager.save(scene, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", action="store_true", help="Capture/run the unchanged upstream interface")
    parser.add_argument("--dark", action="store_true")
    parser.add_argument("--capture", type=Path, help="Save genuine widget screenshots and exit")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()
    # Same redirection seam as the repository tests (ADR-041); normal production
    # names are not changed in settings.py. Do this BEFORE any stores exist.
    app_settings.ORGANIZATION_NAME = "cofade_design_preview"
    app_settings.APPLICATION_NAME = "Original Design Reference" if args.original else "Creative Design Preview"
    if args.capture:
        app_settings.APPLICATION_NAME += " Capture"
    app = QApplication(sys.argv[:1])
    app.setOrganizationName(app_settings.ORGANIZATION_NAME)
    app.setApplicationName(app_settings.APPLICATION_NAME)
    settings = app_settings.get_settings()
    load_translator(app, settings.language)
    if args.capture:
        # Repeatable evidence must start from a fresh workspace, rather than
        # replay toolbar/splitter geometry from a different experiment. This
        # removes only UI state in the already-isolated preview account.
        app_settings.create_qsettings().remove("UiState")
        settings.show_welcome_on_startup = False
        settings.clear_recent_files()
    settings.agent_api_enabled = False
    settings.download_plant_images = False
    mode = ThemeMode.DARK if args.dark else (ThemeMode.LIGHT if args.capture else settings.theme_mode)
    settings.theme_mode = mode
    theme = apply_theme if args.original else apply_creative_theme
    theme(app, mode)
    window = GardenPlannerApp() if args.original else CreativePreviewWindow()
    if args.capture:
        window.showNormal()
        window.resize(args.width, args.height)
    fixture_dir = args.capture if args.capture else ROOT / "build" / "creative-preview"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    fixture = fixture_dir / "Southwest Michigan - sample landscape.ogp"
    if args.capture or not fixture.exists():
        make_landscape_fixture(fixture)
    window._load_project_file(str(fixture))
    window._sun_toolbar.set_datetime_local(datetime(2026, 6, 21, 16, 0))
    window._sun_sim_action.trigger()
    theme(app, mode)
    window.canvas_scene.set_labels_visible(False)
    if isinstance(window, CreativePreviewWindow):
        window.library.category.setCurrentIndex(3)  # existing Trees category
        if args.capture:
            window.reset_workspace()
    window.show()

    def capture() -> None:
        window.canvas_view.fit_in_view()
        if window._labels_action.isChecked():
            window._labels_action.trigger()
        # Select the actual patio so the existing contextual property controls
        # and real dimensions are visible in both before/after captures.
        patio = next(item for item in window.canvas_scene.items() if getattr(item, "name", "") == "Patio")
        patio.setSelected(True)
        window._sidebar_controller.set_selection_pinned("properties", True)
        app.processEvents()
        QTimer.singleShot(350, take_shots)

    def take_shots() -> None:
        if args.capture:
            args.capture.mkdir(parents=True, exist_ok=True)
            if isinstance(window, CreativePreviewWindow):
                window._workspace_combo.setCurrentIndex(0)
                if args.width < 1100:
                    window.library_dock.hide()
                app.processEvents()
                window.canvas_view.fit_in_view()
                app.processEvents()
            window.grab().save(str(args.capture / "editor.png"))
            window.grab().save(str(args.capture / "imperial.png"))
            if isinstance(window, CreativePreviewWindow):
                window._workspace_combo.setCurrentIndex(1)
                app.processEvents()
                window.canvas_view.fit_in_view()
                app.processEvents()
                window.grab().save(str(args.capture / "sun-study.png"))
                window._workspace_combo.setCurrentIndex(0)
        welcome = WelcomeDialog(window) if args.original else CreativeWelcomeDialog(window)
        welcome.show()
        if isinstance(welcome, CreativeWelcomeDialog):
            welcome.add_project_thumbnail(fixture, window.canvas_view.viewport().grab())
        app.processEvents()
        if args.capture:
            welcome.grab().save(str(args.capture / "welcome.png"))
            evidence = {
                "qt": qVersion(), "font": app.font().family(),
                "width": window.width(), "height": window.height(),
                "device_pixel_ratio": window.devicePixelRatioF(),
                "canvas_width": window.canvas_view.width(),
                "original": args.original, "dark": args.dark,
                "sun_state": window._sun_controller.state,
                "project": str(fixture.relative_to(ROOT)) if fixture.is_relative_to(ROOT) else str(fixture),
                "snapshot": window._project_manager.snapshot_dict(window.canvas_scene),
            }
            (args.capture / "evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
            welcome.reject()
            window.close()
            app.quit()
        else:
            welcome.new_project_requested.connect(window._on_new_project)
            welcome.open_project_requested.connect(window._on_open_project)
            welcome.recent_project_selected.connect(window._open_project_file)
            # Retain the non-modal preview dialog for its window lifetime.
            window.creative_welcome = welcome

    if args.capture:
        QTimer.singleShot(900, capture)
    else:
        QTimer.singleShot(900, window.canvas_view.fit_in_view)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
