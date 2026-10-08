"""Opt-in shell around GardenPlannerApp. Not imported by the normal entry point."""

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFormLayout,
    QLabel,
    QTabWidget,
    QToolBar,
    QToolButton,
)

from open_garden_planner.app.application import GardenPlannerApp
from open_garden_planner.ui.creative_preview import (
    CreativeLibrary,
    CreativeWelcomeDialog,
    _tr,
    identity,
)
from open_garden_planner.ui.creative_theme import apply_creative_theme
from open_garden_planner.ui.panels.layers_panel import LayersPanel
from open_garden_planner.ui.theme import ThemeMode


class CreativePreviewWindow(GardenPlannerApp):
    """Keep the real canvas, controllers, commands, dialogs and project manager."""

    def __init__(self) -> None:
        super().__init__()
        self._install_preview_workspace()
        self._ui_state.restore_geometry(self)
        self._enforce_toolbar_visibility()

    def _restore_ui_state(self) -> None:
        # Restore after the experimental docks exist. The runner isolates all
        # settings and autosave paths from the normal application's account.
        self._geometry_restored = False

    def _install_preview_workspace(self) -> None:
        # Move the sidebar CONTAINER, never its ordered accordion panels.
        # SidebarController registration/pinning remains unchanged (ADR-030).
        self.properties_dock = QDockWidget(_tr("Selection & properties"), self)
        self.properties_dock.setObjectName("CreativePropertiesDock")
        self.sidebar.setMinimumWidth(485)
        self.properties_panel._form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.properties_dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        self.library = CreativeLibrary()
        self.library.tool_selected.connect(self._on_tool_selected)
        self.library.item_selected.connect(self._on_gallery_item_selected)
        self.library_tabs = QTabWidget()
        self.library_tabs.addTab(self.library, _tr("Library"))
        # A second PURE VIEW over existing layer commands avoids reparenting
        # the original accordion. Both views stay synchronized by scene signals.
        self.library_layers = LayersPanel()
        self.library_layers.set_layers(self.canvas_scene.layers)
        self.library_layers.active_layer_changed.connect(self._on_active_layer_changed)
        self.library_layers.layer_visibility_changed.connect(self._on_layer_visibility_change_requested)
        self.library_layers.layer_lock_changed.connect(self._on_layer_lock_change_requested)
        self.library_layers.layer_opacity_changed.connect(self.canvas_scene.preview_layer_opacity)
        self.library_layers.layer_opacity_committed.connect(self._on_layer_opacity_committed)
        self.library_layers.layers_reordered.connect(self._on_layers_reordered)
        self.library_layers.layer_renamed.connect(self._on_layer_renamed)
        self.library_layers.layer_deleted.connect(self._on_layer_deleted)
        self.library_layers.layer_add_requested.connect(self._on_layer_add_requested)
        self.canvas_scene.layers_changed.connect(
            lambda: self.library_layers.set_layers(self.canvas_scene.layers)
        )
        self.canvas_scene.active_layer_changed.connect(self._sync_library_layer)
        self.library_tabs.addTab(self.library_layers, _tr("Layers"))
        self.library_dock = QDockWidget(_tr("Objects & plants"), self)
        self.library_dock.setObjectName("CreativeLibraryDock")
        self.library_dock.setWidget(self.library_tabs)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.library_dock)

        self.preview_header = QToolBar(_tr("Project"), self)
        self.preview_header.setObjectName("CreativeProjectToolbar")
        self.preview_header.setMovable(False)
        self.preview_header.addWidget(identity(compact=True))
        self.project_label = QLabel()
        self.preview_header.addWidget(self.project_label)
        # Share existing QAction objects, including enabled states and shortcuts.
        for action in self.menuBar().actions()[0].menu().actions():
            if action.shortcut().toString() in {"Ctrl+N", "Ctrl+O", "Ctrl+S"}:
                self.preview_header.addAction(action)
        self.preview_header.addSeparator()
        self.preview_header.addAction(self._sun_sim_action)
        self.preview_header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.insertToolBar(self.main_toolbar, self.preview_header)
        self.insertToolBarBreak(self.main_toolbar)
        self.insertToolBarBreak(self.category_toolbar)
        # Existing category commands retain their menus, shortcuts and tooltips;
        # add readable names without replacing their icon family.
        category_names = {
            "garden_bed": _tr("Beds & surfaces"), "rectangle": _tr("Shapes"),
            "tree": _tr("Trees"), "shrub": _tr("Shrubs"), "flower": _tr("Perennials"),
            "vegetable": _tr("Vegetables"), "house": _tr("Structures"),
            "furniture": _tr("Furniture"), "fence": _tr("Fences"),
            "infrastructure": _tr("Utilities"), "vertical_container": _tr("Containers"),
        }
        for category, button in zip(
            self.category_toolbar._categories, self.category_toolbar._category_buttons, strict=True
        ):
            button.setFixedWidth(135 if category.icon_name == "garden_bed" else 92)
            button.setFixedHeight(48)
            button.setText(category_names[category.icon_name])
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        tool_names = {"SELECT": _tr("Select"), "MEASURE": _tr("Measure"),
                      "TEXT": _tr("Text"), "CALLOUT": _tr("Callout"), "JOURNAL_PIN": _tr("Journal")}
        for tool, button in self.main_toolbar._buttons.items():
            button.setFixedWidth(104)
            button.setFixedHeight(36)
            button.setText(tool_names[tool.name])
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        for button in self.findChildren(QToolButton):
            if button.toolTip() and not button.accessibleName():
                button.setAccessibleName(button.toolTip())
        view_menu = self.menuBar().actions()[2].menu()
        view_menu.addSeparator()
        view_menu.addAction(self.library_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(_tr("Focus canvas"), self.focus_canvas)
        view_menu.addAction(_tr("Reset workspace"), self.reset_workspace)
        self._sun_toolbar.addSeparator()
        self._sun_toolbar.addWidget(QLabel(_tr("Geometric shade · computer time ({zone})").format(
            zone=datetime.now().astimezone().tzname())))
        self._project_manager.project_changed.connect(self._refresh_project_label)
        self._project_manager.dirty_changed.connect(self._refresh_project_label)
        self._refresh_project_label()
        self.reset_workspace()

    def _sync_library_layer(self, layer: object) -> None:
        if layer is not None:
            self.library_layers.select_layer(layer.id)

    def _refresh_project_label(self, _: object = None) -> None:
        state = _tr("Unsaved changes") if self._project_manager.is_dirty else _tr("No unsaved changes")
        self.project_label.setText(_tr("{name}  ·  {state}").format(
            name=self._project_manager.project_name, state=state))
        self.project_label.setContentsMargins(18, 0, 18, 0)

    def reset_workspace(self) -> None:
        self.library_dock.setFloating(False)
        self.properties_dock.setFloating(False)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.library_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)
        self.library_dock.show()
        self.properties_dock.show()
        self.resizeDocks([self.library_dock, self.properties_dock], [210, 485], Qt.Orientation.Horizontal)

    def focus_canvas(self) -> None:
        self.library_dock.hide()
        self.properties_dock.hide()
        self.canvas_view.setFocus()

    def _enter_preview_mode(self) -> None:
        self._creative_fullscreen_state = {
            widget: widget.isVisible() for widget in (
                self.library_dock, self.properties_dock, self.preview_header,
                self.category_toolbar, self.constraint_toolbar,
            )
        }
        super()._enter_preview_mode()
        for widget in self._creative_fullscreen_state:
            widget.hide()

    def _exit_preview_mode(self) -> None:
        super()._exit_preview_mode()
        for widget, visible in self._creative_fullscreen_state.items():
            widget.setVisible(visible)

    def _show_welcome_dialog(self) -> None:
        from open_garden_planner.app.settings import get_settings

        if not get_settings().show_welcome_on_startup:
            return
        dialog = CreativeWelcomeDialog(self)
        dialog.new_project_requested.connect(self._on_new_project)
        dialog.open_project_requested.connect(self._on_open_project)
        dialog.recent_project_selected.connect(self._open_project_file)
        dialog.exec()

    def _on_theme_changed(self, mode: ThemeMode) -> None:
        # Retain upstream preferences/checkmark handling, then apply the proposal.
        super()._on_theme_changed(mode)
        apply_creative_theme(QApplication.instance(), mode)
