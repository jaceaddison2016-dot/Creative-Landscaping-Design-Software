"""Creative desktop workspace over the retained Open Garden Planner editor."""

from datetime import datetime

from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDockWidget,
    QFormLayout,
    QLabel,
    QMenu,
    QSizePolicy,
    QTabWidget,
    QToolBar,
    QToolButton,
)

from open_garden_planner.app import settings as app_settings
from open_garden_planner.app.application import GardenPlannerApp
from open_garden_planner.core.display_commands import (
    SetDisplayUnitsCommand,
    SetGridSpacingCommand,
    SetPresentationCommand,
)
from open_garden_planner.core.tools import ToolType
from open_garden_planner.core.units import (
    FOOT_CM,
    IMPERIAL,
    METRIC,
    DisplayUnits,
    LengthFormat,
    UnitSystem,
)
from open_garden_planner.ui.creative_preview import (
    CreativeLibrary,
    CreativeWelcomeDialog,
    _tr,
    identity,
)
from open_garden_planner.ui.creative_theme import apply_creative_theme
from open_garden_planner.ui.icons import get_icon
from open_garden_planner.ui.panels.layers_panel import LayersPanel
from open_garden_planner.ui.theme import ThemeMode


class CreativePreviewWindow(GardenPlannerApp):
    """Keep the real canvas, controllers, commands, dialogs and project manager."""

    default_new_project_units = IMPERIAL

    def tr(self, source_text: str, disambiguation: str | None = None, n: int = -1) -> str:
        # QObject.tr otherwise uses the subclass name. Inherited menu/dialog
        # strings live in GardenPlannerApp, while new preview strings use _tr.
        return QCoreApplication.translate("GardenPlannerApp", source_text, disambiguation, n)

    def __init__(self) -> None:
        super().__init__()
        self._install_preview_workspace()
        self._geometry_restored = self._ui_state.restore_geometry(self)
        saved_workspace = app_settings.create_qsettings().value("UiState/creative_workspace", 0, type=int)
        self._workspace_combo.setCurrentIndex(saved_workspace if saved_workspace in (0, 1, 2) else 0)
        self._enforce_toolbar_visibility()
        self._compact_status_bar()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        if hasattr(self, "location_label"):
            self._compact_status_bar()

    def _compact_status_bar(self) -> None:
        """Keep drawing measurements readable when optional context is crowded."""
        compact = self.width() < 1250
        for label in (self.location_label, self.season_label):
            label.setVisible(not compact)
        for icon in self.statusBar().findChildren(QLabel):
            if icon.toolTip() in (self.tr("Garden location"), self.tr("Season")):
                icon.setVisible(not compact)
        self.coord_label.setMinimumWidth(110 if compact else 200)
        self.zoom_label.setMinimumWidth(35 if compact else 60)
        self.tool_label.setMinimumWidth(45 if compact else 80)
        if self.coordinate_input_field is not None:
            self.coordinate_input_field.setFixedWidth(150 if compact else 220)

    def _restore_ui_state(self) -> None:
        # Restore after the Creative docks exist. The optional capture runner
        # uses an isolated account; normal desktop paths remain unchanged.
        self._geometry_restored = False

    def _install_preview_workspace(self) -> None:
        # Move the sidebar CONTAINER, never its ordered accordion panels.
        # SidebarController registration/pinning remains unchanged (ADR-030).
        self.properties_dock = QDockWidget(_tr("Selection & properties"), self)
        self.properties_dock.setObjectName("CreativePropertiesDock")
        self.sidebar.setMinimumWidth(300)
        self.sidebar.setMaximumWidth(10000)
        self.properties_panel.enable_creative_groups()
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
        self._install_compact_toolbar()
        self.canvas_scene.display_units_changed.connect(self._refresh_units)
        self.canvas_scene.set_display_units(IMPERIAL)
        self.canvas_view.set_grid_size(FOOT_CM)
        self.canvas_scene.set_presentation("architectural", .3)
        self._project_manager.mark_clean()
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
        self.resizeDocks([self.library_dock, self.properties_dock], [200, 320], Qt.Orientation.Horizontal)

    def focus_canvas(self) -> None:
        self.library_dock.hide()
        self.properties_dock.hide()
        self.canvas_view.setFocus()

    def _enter_preview_mode(self) -> None:
        self._creative_fullscreen_state = {
            widget: widget.isVisible() for widget in (
                self.library_dock, self.properties_dock, self.preview_header,
                self.category_toolbar, self.constraint_toolbar, self._sun_toolbar, self.creative_actions,
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

    def _apply_application_theme(self, mode: ThemeMode) -> None:
        # The inherited handler persists preferences/checkmarks and calls this
        # hook once. Avoid three application-wide stylesheet passes.
        apply_creative_theme(QApplication.instance(), mode)

    def _install_compact_toolbar(self) -> None:
        self.project_label.setMaximumWidth(360)
        self.project_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.preview_header.removeAction(self._sun_sim_action)
        self._workspace_combo = QComboBox()
        self._workspace_combo.addItems([_tr("Landscape"), _tr("Sun Study"), _tr("Gardening")])
        self._workspace_combo.setAccessibleName(_tr("Workspace"))
        self._workspace_combo.currentIndexChanged.connect(self._set_workspace)
        self.preview_header.addWidget(self._workspace_combo)
        self.creative_actions = QToolBar(_tr("Landscape tools"), self)
        self.creative_actions.setObjectName("CreativeLandscapeToolbar")
        self.creative_actions.setMovable(False)
        self.insertToolBar(self.main_toolbar, self.creative_actions)
        self.insertToolBarBreak(self.creative_actions)

        def tool_action(button, menu):
            action = QAction(button.icon(), button.toolTip(), self)
            action.setCheckable(button.isCheckable())
            action.setChecked(button.isChecked())
            action.setEnabled(button.isEnabled())
            if not button.shortcut().isEmpty():
                action.setShortcut(button.shortcut())
                button.setShortcut(QKeySequence())
                self.addAction(action)
            action.triggered.connect(button.click)
            button.toggled.connect(action.setChecked)
            menu.addAction(action)
            return action

        def group(label, icon):
            button = QToolButton()
            button.setText(_tr(label))
            button.setToolTip(_tr(label))
            button.setAccessibleName(_tr(label))
            if (glyph := get_icon(icon)) is not None:
                button.setIcon(glyph)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            menu = QMenu(button)
            button.setMenu(menu)
            self.creative_actions.addWidget(button)
            return button, menu

        select, edit = group("Select/Edit", "select")
        select_action = tool_action(self.main_toolbar._buttons[ToolType.SELECT], edit)
        select.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        select.clicked.connect(self.main_toolbar._buttons[ToolType.SELECT].click)
        select_action.toggled.connect(select.setChecked)
        select.setCheckable(True)
        select.setChecked(True)
        edit.addSeparator()
        edit.addActions(self.menuBar().actions()[1].menu().actions())
        advanced = edit.addMenu(_tr("Advanced tools"))
        for button in self.constraint_toolbar._buttons.values():
            tool_action(button, advanced)
        for tool in (ToolType.TEXT, ToolType.CALLOUT, ToolType.JOURNAL_PIN):
            tool_action(self.main_toolbar._buttons[tool], advanced)
        groups = {
            "Site & Structures": ("house", {"house", "fence", "infrastructure", "rectangle"}),
            "Hardscape": ("terrace", {"garden_bed", "furniture"}),
            "Planting": ("tree", {"tree", "shrub", "flower", "vegetable", "vertical_container"}),
        }
        for title, (icon, categories) in groups.items():
            _, menu = group(title, icon)
            for category in self.category_toolbar._categories:
                if category.icon_name not in categories:
                    continue
                submenu = menu.addMenu(category.name)
                for item in category.items:
                    action = submenu.addAction(item.name)
                    action.triggered.connect(lambda _checked=False, entry=item: self._choose_library_item(entry))
        _, dimensions = group("Dimensions", "measure")
        tool_action(self.main_toolbar._buttons[ToolType.MEASURE], dimensions)
        for tool, button in self.constraint_toolbar._buttons.items():
            if "DISTANCE" in tool.name or "EDGE_LENGTH" in tool.name:
                tool_action(button, dimensions)
        dimensions.addSeparator()
        units_menu = dimensions.addMenu(_tr("Project units"))
        units_group = QActionGroup(self)
        units_group.setExclusive(True)
        self._unit_actions = {}
        for label, units in (("Feet & inches", IMPERIAL),
                             ("Decimal feet", DisplayUnits(UnitSystem.IMPERIAL, LengthFormat.DECIMAL_FEET)),
                             ("Metric", METRIC)):
            action = units_menu.addAction(_tr(label))
            action.setCheckable(True)
            units_group.addAction(action)
            action.triggered.connect(lambda _checked=False, value=units: self._change_units(value))
            self._unit_actions[units] = action
        dimensions.addAction(_tr("Grid spacing…"), self._edit_grid_spacing)
        _, sun = group("Sun Study", "sun")
        sun.addAction(self._sun_sim_action)
        sun.addAction(_tr("Open sun workspace"), lambda: self._workspace_combo.setCurrentIndex(1))
        _, export = group("Export", "file_export")
        export_menu = next(action.menu() for action in self.menuBar().actions()[0].menu().actions()
                           if action.text() == self.tr("&Export"))
        export.addActions(export_menu.actions())
        view = self.menuBar().actions()[2].menu()
        presentation = view.addMenu(_tr("Drawing presentation"))
        presentation.addAction(_tr("Architectural plant symbols"), lambda: self._set_presentation("architectural"))
        presentation.addAction(_tr("Detailed plant symbols"), lambda: self._set_presentation("detailed"))
        presentation.addAction(_tr("Material texture strength…"), self._edit_texture_strength)
        gardening = view.addMenu(_tr("Gardening workspace"))
        for index in range(1, self._tab_widget.count()):
            action = gardening.addAction(self._tab_widget.tabText(index))
            action.triggered.connect(lambda _checked=False, tab=index: self._open_gardening_tab(tab))
        # Preserve the retained Find & Replace Ctrl+F action.
        search_action = view.addAction(_tr("Search object library"))
        search_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        search_action.triggered.connect(self._focus_library_search)
        for shortcut in self.category_toolbar.findChildren(QShortcut):
            if shortcut.key().toString() == "Ctrl+F":
                shortcut.setEnabled(False)
        self._sun_sim_action.toggled.connect(self._on_creative_sun_toggled)
        self._set_workspace(0)
        self._enforce_toolbar_visibility()

    def _choose_library_item(self, entry) -> None:
        self._on_tool_selected(entry.tool_type)
        self._on_gallery_item_selected(entry)

    def _change_units(self, units: DisplayUnits) -> None:
        if units != self.canvas_scene.display_units:
            self.canvas_view.setFocus()
            self.canvas_view.command_manager.execute(SetDisplayUnitsCommand(self.canvas_scene, units))

    def _refresh_units(self) -> None:
        for units, action in self._unit_actions.items():
            action.setChecked(units == self.canvas_scene.display_units)
        # Finish a pending text edit before rebuilding its existing controls.
        self.canvas_view.setFocus()
        self.properties_panel._current_identity = None
        self.properties_panel.set_selected_items(list(self.canvas_scene.selectedItems()))
        self.constraints_panel.refresh()
        self.plant_database_panel.set_selected_items(list(self.canvas_scene.selectedItems()))
        self.update_coordinates(*getattr(self, "_last_coordinates", (0, 0)))
        selected = list(self.canvas_scene.selectedItems())
        self.update_selection(len(selected), selected)
        field = self.coordinate_input_field
        if self.canvas_scene.display_units.imperial:
            field.setPlaceholderText('@10ft,0  10ft,5ft')
            field._help_tooltip = _tr("Bare numbers mean feet. Use commas between coordinates; fractions such as 10' 6 1/2\" are accepted. @ means relative; < introduces a polar angle.")
        else:
            field.setPlaceholderText(field.tr("@dx,dy   @dist<angle   x,y"))
            field._help_tooltip = field.tr("Typed coordinate input. Examples: @500,0 (relative), @300<45 (polar, 0deg = east, CCW positive), 1000,500 (absolute). Press Enter to commit.")
        field.setToolTip(field._help_tooltip)
        self.canvas_view._calibration_input.setPlaceholderText(_tr("Distance (ft/in)") if self.canvas_scene.display_units.imperial else self.canvas_view.tr("Distance in cm"))
        self.canvas_view.viewport().update()

    def _edit_grid_spacing(self) -> None:
        from open_garden_planner.ui.widgets.length_input import get_length
        value, ok = get_length(self, _tr("Grid spacing"), _tr("Grid spacing (cm):"),
                               self.canvas_view.grid_size, .1, 100000)
        if ok:
            self.canvas_view.command_manager.execute(SetGridSpacingCommand(self.canvas_view, value))

    def _set_presentation(self, style: str) -> None:
        if style != self.canvas_scene.plant_symbol_style:
            self.canvas_view.command_manager.execute(SetPresentationCommand(
                self.canvas_scene, style, self.canvas_scene.texture_strength))

    def _edit_texture_strength(self) -> None:
        from PyQt6.QtWidgets import QInputDialog
        strength, ok = QInputDialog.getInt(self, _tr("Material texture strength"),
                                          _tr("Texture detail (%):"), int(self.canvas_scene.texture_strength * 100), 0, 100)
        if ok:
            self.canvas_view.command_manager.execute(SetPresentationCommand(
                self.canvas_scene, self.canvas_scene.plant_symbol_style, strength / 100))

    def _set_workspace(self, index: int) -> None:
        gardening = index == 2
        if not gardening:
            self._tab_widget.setCurrentIndex(0)
        for tab in range(1, self._tab_widget.count()):
            self._tab_widget.setTabVisible(tab, gardening)
        self._tab_widget.tabBar().setVisible(gardening)
        if index == 1 and not self._sun_sim_action.isChecked():
            self._sun_sim_action.trigger()
        self._sun_toolbar.setVisible(index == 1 and self._sun_sim_action.isChecked())
        app_settings.create_qsettings().setValue("UiState/creative_workspace", index)

    def _on_creative_sun_toggled(self, checked: bool) -> None:
        if checked:
            self._workspace_combo.setCurrentIndex(1)
        self._sun_toolbar.setVisible(checked and self._workspace_combo.currentIndex() == 1)

    def _open_gardening_tab(self, index: int) -> None:
        self._workspace_combo.setCurrentIndex(2)
        self._tab_widget.setCurrentIndex(index)

    def _on_tab_changed(self, index: int) -> None:
        if index > 0 and hasattr(self, "_workspace_combo"):
            self._workspace_combo.setCurrentIndex(2)
        super()._on_tab_changed(index)

    def _focus_library_search(self) -> None:
        self.library_dock.show()
        self.library_tabs.setCurrentIndex(0)
        self.library.search.setFocus()
        self.library.search.selectAll()

    def _enforce_toolbar_visibility(self) -> None:
        if not hasattr(self, "creative_actions"):
            super()._enforce_toolbar_visibility()
            return
        for toolbar in (self.main_toolbar, self.category_toolbar, self.constraint_toolbar):
            toolbar.hide()
        self.preview_header.show()
        self.creative_actions.show()
        self.soil_overlay_toolbar.hide()
        self._sun_toolbar.setVisible(self._workspace_combo.currentIndex() == 1 and self._sun_sim_action.isChecked())

    def _new_project_document(self, **kwargs) -> None:
        super()._new_project_document(**kwargs)
        self.canvas_scene.set_display_units(IMPERIAL)
        self.canvas_view.set_grid_size(FOOT_CM)
        self.canvas_scene.set_presentation("architectural", .3)
        self._project_manager.mark_clean()

    def _update_window_title(self, _: object = None) -> None:
        super()._update_window_title()
        self.setWindowTitle(self.windowTitle().replace("Open Garden Planner", _tr("Creative Landscape Studio")))

    def _save_to_file(self, file_path) -> None:
        super()._save_to_file(file_path)
        if not self._project_manager.is_dirty and self._project_manager.current_file == file_path:
            from open_garden_planner.ui.project_thumbnails import save_thumbnail
            save_thumbnail(self.canvas_view, file_path)

    def _load_project_file(self, file_path) -> None:
        self.canvas_view.setFocus()
        super()._load_project_file(file_path)
        self._refresh_units()

    def _on_sun_toolbar_visibility(self, visible: bool) -> None:
        # In Creative, workspace visibility and simulation state are separate.
        # The checked QAction still owns explicit enabling/disabling.
        if not hasattr(self, "_workspace_combo"):
            super()._on_sun_toolbar_visibility(visible)
