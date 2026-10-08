# Desktop interface audit

> Historical first-preview evidence. The newer continuation changes the default desktop workspace and units. See [current validation](CONTINUATION_VALIDATION.md).


October 7, 2026, America/Detroit. Baseline: desktop foundation
`439e486414070161d9fea58a6123644e8d0afdc3`, upstream-derived v1.29.5.
See [UPSTREAM_PROVENANCE.md](../../UPSTREAM_PROVENANCE.md) and
[PLATFORM_STATUS.md](../../PLATFORM_STATUS.md) for code/license/platform evidence.

## Genuine before evidence

[Main editor](previews/before/editor.png) and [welcome](previews/before/welcome.png)
are Qt widget grabs from the unchanged `GardenPlannerApp` and `WelcomeDialog`,
not illustration mockups. Both use the same synthetic 24×18 m editable plan as
the proposed captures. A patio is selected, its real properties are opened,
the existing solar overlay is enabled and object-name labels are hidden through
the existing View action. No production user settings or client project are used.

## Findings and protected seams

| Surface | Finding | Source / protected behavior |
| --- | --- | --- |
| Theme | Mature light/dark semantic roles, generated QSS, icon listeners and widget propagation already exist. | `ui/theme.py`, `ui/icons.py`; reuse rather than duplicate. |
| Top row | Five core icons, many constraints, 11 category icons and search compete in one row. Icon-only categories depend on hover. | `ui/widgets/toolbar.py`, `constraint_toolbar.py`, `category_toolbar.py`; preserve all actions and shortcuts. |
| Canvas | Real Y-up centimeter scene, grid/rulers, snapping, calibrated images, dimensions and selection handles. | `ui/canvas/`; no visual refactor may change physical geometry or conversion seams. |
| Sidebar | Wide contextual form plus many collapsed panels. Panel order, pin/peek and scrolling embody ADR-030 fixes. | `application.py::_setup_sidebar`, `ui/widgets/panel_stack.py`; never reparent individual accordion panels. |
| Properties | Original form is useful but horizontal numeric pairs and Arrange row require room; crowded at larger text sizes. | `ui/panels/properties_panel.py`; retain command routing, live edits, debounce and focus-out commits. |
| Object library | Real categories, SVG/texture thumbnails and global search. Provider search and metadata are separate existing panels. | `ui/widgets/gallery_data.py`, `category_dropdown.py`, `global_search.py`; preview uses the same registry. |
| Layers | Visibility, locking, opacity, ordering and names are command-backed, not mutable aliases. | `ui/panels/layers_panel.py`, application layer handlers. |
| Welcome | Upstream banner, New/Open, recents, missing-file handling, startup checkbox and Close. No thumbnails or modification dates in its standard list. | `ui/dialogs/welcome_dialog.py`; keep signal contract and real file-opening handlers. |
| Sun | Existing menu/toolbar already has a date picker, minute slider, animation, heatmap busy state and night/no-location hints. | `sun_sim_toolbar.py`, `sun_shadow_controller.py`, `sun_heatmap.py`; no invented play button or replacement solar math. |
| Time model | Date/time is computer-local; solar controller converts to UTC. Location is saved, simulation overlay/time is runtime-only. | See §8.20 and existing solar tests; project-time-zone UI remains master-plan work. |
| Save/recovery | Atomic load/save, dirty warnings, undo, autosave and startup recovery already exist. | `core/project.py`, `_startup_sequence`; no new schema or hidden save success. |
| Dialogs/outputs | Many owned dialogs plus native file pickers; PDF/SVG/PNG/DXF/CSV paths already exist. | Reuse exports. No approved company title-block asset exists. |

## Shortcuts and discovery that must survive

| Interaction | Existing access |
| --- | --- |
| New / Open / Save / Save As | Ctrl+N / Ctrl+O / Ctrl+S / Ctrl+Shift+S |
| Undo / Redo | Ctrl+Z / Ctrl+Y |
| Cut / Copy / Paste / Duplicate | Ctrl+X / Ctrl+C / Ctrl+V / Ctrl+D |
| Delete / Select all | Delete / Ctrl+A |
| Select / Measure / Journal | V / M / J |
| Object search | Ctrl+F; existing category dropdowns |
| Fullscreen drawing preview | F11; Escape returns |
| Location / sun controls | File → Set Garden Location; View → Sun & 3D → Sun & Shade Simulation |
| Theme / licensing | View → Theme; Help → About retains upstream and data notices |

New preview dock toggles, Focus canvas and Reset workspace are added to View.
They do not take over any inherited shortcut. A plant's generic circle placement
uses the inherited two-click center/rim gesture; no fake one-click placement is
claimed. Online/offline plant services, CAD constraints, calendar, tasks, harvest,
3D and optional automation remain inherited capabilities, not rewritten surfaces.

## Scope of this review

The first-task experiment covers the two representative surfaces. Full owned
dialog restyling, broad dark-state QA, approved identity, compact density, automatic
recent thumbnails, templates, project timezone, client title blocks and imperial
entry are deferred until their respective approval/implementation steps.
Native dock glyph contrast, full screen-reader behavior, packaged fonts, GPU
rendering and native OS scaling need later platform/manual QA. The portfolio
site could not be re-verified because of a proxy 403; no website assets were copied.
