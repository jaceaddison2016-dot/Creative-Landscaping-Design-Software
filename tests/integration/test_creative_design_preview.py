"""Actual Qt preview workflows, without enabling the design in normal startup."""

import os
import subprocess
import sys
import textwrap
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication, QMessageBox

from open_garden_planner.app.creative_preview import CreativePreviewWindow
from open_garden_planner.app.settings import get_settings
from open_garden_planner.core.object_types import ObjectType
from open_garden_planner.ui.canvas.items import CircleItem
from open_garden_planner.ui.creative_preview import CreativeWelcomeDialog
from open_garden_planner.ui.creative_theme import DARK, LIGHT, apply_creative_theme
from open_garden_planner.ui.theme import (
    ThemeColors,
    ThemeMode,
    apply_theme,
    current_colors,
    is_dark_theme,
)


@pytest.fixture
def window(qtbot, monkeypatch):
    get_settings().show_welcome_on_startup = False
    monkeypatch.setattr(QMessageBox, "question", lambda *_a, **_k: QMessageBox.StandardButton.Discard)
    app = QApplication.instance()
    old_font = app.font()
    apply_creative_theme(app, ThemeMode.LIGHT)
    win = CreativePreviewWindow()
    win.showNormal()
    win.resize(1920, 1080)
    qtbot.addWidget(win)
    yield win
    win._project_manager.mark_clean()
    win.close()
    app.setFont(old_font)
    apply_theme(app, ThemeMode.LIGHT)


def test_library_click_places_undoable_tree_and_round_trips(window, qtbot, tmp_path):
    window.library.search.setText("Round Deciduous")
    assert window.library.items.count() == 1
    row = window.library.items.item(0)
    QApplication.processEvents()
    qtbot.mouseClick(window.library.items.viewport(), Qt.MouseButton.LeftButton,
                     pos=window.library.items.visualItemRect(row).center())
    event = MagicMock(spec=QMouseEvent)
    event.button.return_value = Qt.MouseButton.LeftButton
    event.buttons.return_value = Qt.MouseButton.LeftButton
    event.modifiers.return_value = Qt.KeyboardModifier.NoModifier
    window.canvas_view.active_tool.mouse_press(event, QPointF(1000, 1000))
    window.canvas_view.active_tool.mouse_move(event, QPointF(1100, 1000))
    window.canvas_view.active_tool.mouse_release(event, QPointF(1100, 1000))
    window.canvas_view.active_tool.mouse_press(event, QPointF(1100, 1000))
    window.canvas_view.active_tool.mouse_release(event, QPointF(1100, 1000))
    plants = [item for item in window.canvas_scene.items() if isinstance(item, CircleItem)]
    assert len(plants) == 1
    assert plants[0].object_type == ObjectType.TREE
    assert window._project_manager.is_dirty
    assert "Unsaved changes" in window.project_label.text()
    window._on_undo()
    assert not any(isinstance(item, CircleItem) for item in window.canvas_scene.items())
    window._on_redo()
    assert len([item for item in window.canvas_scene.items() if isinstance(item, CircleItem)]) == 1
    path = tmp_path / "placed tree.ogp"
    window._save_to_file(path)
    assert not window._project_manager.is_dirty
    window._load_project_file(str(path))
    assert len([item for item in window.canvas_scene.items() if isinstance(item, CircleItem)]) == 1


def test_dock_focus_reset_and_layer_commands_survive_restart(window, qtbot):
    window.library_tabs.setCurrentIndex(1)
    # Drive the real existing layer view's mutation request, then prove both
    # representations and undo are connected to the same inherited scene.
    layer = window.canvas_scene.active_layer
    window.library_layers.layer_renamed.emit(layer.id, "Planting plan")
    assert window.canvas_scene.active_layer.name == "Planting plan"
    assert window.library_layers._layers[0].name == "Planting plan"
    assert window.layers_panel._layers[0].name == "Planting plan"
    window._on_undo()
    assert window.canvas_scene.active_layer.name != "Planting plan"
    window.focus_canvas()
    assert window.library_dock.isHidden() and window.properties_dock.isHidden()
    window._save_ui_state()
    reopened = CreativePreviewWindow()
    qtbot.addWidget(reopened)
    assert reopened.library_dock.isHidden() and reopened.properties_dock.isHidden()
    reopened.reset_workspace()
    assert not reopened.library_dock.isHidden() and not reopened.properties_dock.isHidden()
    reopened._sun_toolbar.show()
    reopened._enter_preview_mode()
    assert reopened.library_dock.isHidden() and reopened.preview_header.isHidden()
    assert reopened._sun_toolbar.isHidden()
    reopened._exit_preview_mode()
    assert not reopened.library_dock.isHidden() and not reopened.preview_header.isHidden()
    assert not reopened._sun_toolbar.isHidden()


def test_dark_switch_and_upstream_palette_fallback(window):
    window._on_theme_changed(ThemeMode.DARK)
    assert is_dark_theme()
    assert current_colors()["surface"] == DARK["surface"]
    assert current_colors()["canvas_background"] == LIGHT["canvas_background"]
    apply_theme(QApplication.instance(), ThemeMode.LIGHT)
    assert not is_dark_theme()
    assert current_colors() == ThemeColors.LIGHT


@pytest.mark.parametrize("kind", ["new", "open", "recent"])
def test_welcome_actions_keep_upstream_signal_contract(qtbot, tmp_path, kind):
    path = tmp_path / "sample.ogp"
    path.write_text("{}", encoding="utf-8")
    get_settings().add_recent_file(str(path))
    dialog = CreativeWelcomeDialog()
    qtbot.addWidget(dialog)
    dialog.show()
    if kind == "recent":
        dialog._recent_list.setCurrentRow(0)
        assert dialog._open_selected_btn.isEnabled()
        with qtbot.waitSignal(dialog.recent_project_selected) as signal:
            qtbot.mouseClick(dialog._open_selected_btn, Qt.MouseButton.LeftButton)
        assert signal.args == [str(path)]
    else:
        signal = dialog.new_project_requested if kind == "new" else dialog.open_project_requested
        button = dialog.new_button if kind == "new" else dialog.open_button
        with qtbot.waitSignal(signal):
            qtbot.mouseClick(button, Qt.MouseButton.LeftButton)


def test_missing_recent_is_visible_and_cannot_open(qtbot, tmp_path):
    get_settings().add_recent_file(str(tmp_path / "missing.ogp"))
    dialog = CreativeWelcomeDialog()
    qtbot.addWidget(dialog)
    dialog._recent_list.setCurrentRow(0)
    assert "not found" in dialog._recent_list.item(0).text()
    assert not dialog._open_selected_btn.isEnabled()


def test_german_preview_and_inherited_footer(qtbot):
    from PyQt6.QtCore import QTranslator
    from PyQt6.QtWidgets import QPushButton

    translator = QTranslator()
    path = Path(__file__).resolve().parents[2] / "src/open_garden_planner/resources/translations/open_garden_planner_de.qm"
    assert translator.load(str(path))
    app = QApplication.instance()
    app.installTranslator(translator)
    try:
        get_settings().show_welcome_on_startup = False
        window = CreativePreviewWindow()
        qtbot.addWidget(window)
        assert window.menuBar().actions()[0].text() == "&Datei"
        new_action = next(action for action in window.menuBar().actions()[0].menu().actions()
                          if action.shortcut().toString() == "Ctrl+N")
        assert new_action.text() == "&Neues Projekt"
        assert new_action in window.preview_header.actions()
        dialog = CreativeWelcomeDialog()
        qtbot.addWidget(dialog)
        assert dialog.new_button.text() == "Neues Projekt"
        assert "Schließen" in [button.text() for button in dialog.findChildren(QPushButton)]
        assert dialog._recent_list.item(0).text() == "Keine aktuellen Projekte"
    finally:
        app.removeTranslator(translator)


def test_interactive_runner_keeps_saved_language_geometry_and_docks(tmp_path):
    """Launch the actual runner after saving a workspace in its isolated account."""
    root = Path(__file__).resolve().parents[2]
    env = {**os.environ, "QT_QPA_PLATFORM": "offscreen",
           "XDG_CONFIG_HOME": str(tmp_path / "config"),
           "XDG_DATA_HOME": str(tmp_path / "data"),
           "XDG_CACHE_HOME": str(tmp_path / "cache"),
           "CREATIVE_RUNNER_TEST_SETTINGS": str(tmp_path / "preferences.ini"),
           "CREATIVE_RUNNER_TEST_ROOT": str(tmp_path / "runner")}
    account = """
        import os
        from pathlib import Path
        from PyQt6 import QtWebEngineWidgets
        from PyQt6.QtCore import QSettings, QStandardPaths
        from PyQt6.QtWidgets import QApplication
        from open_garden_planner.app import settings
        settings.ORGANIZATION_NAME = 'cofade_design_preview'
        settings.APPLICATION_NAME = 'Creative Design Preview'
        settings.create_qsettings = lambda: QSettings(os.environ['CREATIVE_RUNNER_TEST_SETTINGS'] + '.' + settings.APPLICATION_NAME, QSettings.Format.IniFormat)
        QStandardPaths.writableLocation = lambda kind: str(Path(os.environ['XDG_DATA_HOME']) / QApplication.applicationName())
    """
    seed = textwrap.dedent(account) + textwrap.dedent("""
        app = QApplication([])
        app.setOrganizationName(settings.ORGANIZATION_NAME)
        app.setApplicationName(settings.APPLICATION_NAME)
        prefs = settings.get_settings()
        prefs.show_welcome_on_startup = False
        prefs.agent_api_enabled = False
        prefs.language = 'de'
        from open_garden_planner.app.creative_preview import CreativePreviewWindow
        from open_garden_planner.ui.canvas.items import CircleItem
        from open_garden_planner.ui.theme import ThemeMode
        window = CreativePreviewWindow()
        window._on_theme_changed(ThemeMode.DARK)
        window.showNormal()
        window.resize(800, 640)
        window.focus_canvas()
        app.processEvents()
        sample = Path(os.environ['CREATIVE_RUNNER_TEST_ROOT']) / 'build/creative-preview/Southwest Michigan - sample landscape.ogp'
        sample.parent.mkdir(parents=True)
        window.canvas_scene.addItem(CircleItem(100, 100, 40, name='My saved tree'))
        window._save_to_file(sample)
        window._save_ui_state()
        window.close()
    """)
    verify = textwrap.dedent(account) + textwrap.dedent("""
        import importlib.util
        from types import SimpleNamespace
        from PyQt6.QtCore import QTimer
        from PyQt6.QtWidgets import QApplication
        from open_garden_planner.app.creative_preview import CreativePreviewWindow
        spec = importlib.util.spec_from_file_location('creative_runner', 'scripts/creative_design_preview.py')
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        runner.ROOT = Path(os.environ['CREATIVE_RUNNER_TEST_ROOT'])
        from open_garden_planner.ui.creative_preview import CreativeWelcomeDialog
        from open_garden_planner.ui.theme import is_dark_theme
        result = []
        observed_geometry = []
        def check():
            window = next(w for w in QApplication.topLevelWidgets() if isinstance(w, CreativePreviewWindow))
            observed_geometry.extend([window.width(), window.height()])
            result.extend([
                window.menuBar().actions()[0].text() == '&Datei',
                (window.width(), window.height()) == (800, 640),
                window.library_dock.isHidden(), window.properties_dock.isHidden(),
                is_dark_theme(),
                any(getattr(item, 'name', '') == 'My saved tree' for item in window.canvas_scene.items()),
                not any(isinstance(w, CreativeWelcomeDialog) for w in QApplication.topLevelWidgets()),
            ])
            window._project_manager.mark_clean()
            window.close()
            QApplication.instance().quit()
        runner.QTimer = SimpleNamespace(singleShot=lambda delay, callback: QTimer.singleShot(delay, check))
        assert runner.main() == 0
        assert result == [True] * 7, (result, observed_geometry)
    """)
    capture = textwrap.dedent(account) + textwrap.dedent("""
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location('creative_runner', 'scripts/creative_design_preview.py')
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        runner.ROOT = Path(os.environ['CREATIVE_RUNNER_TEST_ROOT'])
        capture_dir = runner.ROOT / 'capture'
        sys.argv = ['creative_design_preview.py', '--capture', str(capture_dir)]
        assert runner.main() == 0
        for filename in ('editor.png', 'welcome.png'):
            assert (capture_dir / filename).read_bytes().startswith(bytes.fromhex('89504e47'))
    """)
    for code in (seed, verify, capture, verify):
        process = subprocess.run([sys.executable, "-c", code], cwd=root, env=env,
                                 capture_output=True, text=True, timeout=30)
        assert process.returncode == 0, process.stdout + process.stderr
