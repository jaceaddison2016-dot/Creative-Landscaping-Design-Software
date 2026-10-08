"""Actual Qt preview workflows, without enabling the design in normal startup."""

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
    reopened._enter_preview_mode()
    assert reopened.library_dock.isHidden() and reopened.preview_header.isHidden()
    reopened._exit_preview_mode()
    assert not reopened.library_dock.isHidden() and not reopened.preview_header.isHidden()


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
    from pathlib import Path

    from PyQt6.QtCore import QTranslator
    from PyQt6.QtWidgets import QPushButton

    translator = QTranslator()
    path = Path(__file__).resolve().parents[2] / "src/open_garden_planner/resources/translations/open_garden_planner_de.qm"
    assert translator.load(str(path))
    app = QApplication.instance()
    app.installTranslator(translator)
    try:
        dialog = CreativeWelcomeDialog()
        qtbot.addWidget(dialog)
        assert dialog.new_button.text() == "Neues Projekt"
        assert "Schließen" in [button.text() for button in dialog.findChildren(QPushButton)]
        assert dialog._recent_list.item(0).text() == "Keine aktuellen Projekte"
    finally:
        app.removeTranslator(translator)
