# Inherited feature reuse — Milestone A

All implementation references are upstream code preserved in this import. Test
coverage is automated evidence; it does not stand in for a person's desktop test.

| Requested area | Existing implementation | A validation / next change |
| --- | --- | --- |
| 2D landscape workspace | `ui/canvas/canvas_scene.py`, `canvas_view.py`, `core/tools/` | Inherited drawing/selection/resize tests; real-process scene render. Keep editor. |
| Plant placement/editing | gallery, `CircleTool`, `models/plant_data.py`, plant detail panel | Gallery-drop/species-autopopulate integration tests; tree/shrub save/render. Curated landscape content is C. |
| Dimensions | `core/constraints/`, rulers, property panels | Existing metric accuracy retained. Feet/inches are **not implemented** in A; B adds conversion/display. |
| Undo/redo | `core/commands.py`, `CommandManager` | Drawing/undo/dirty/layer tests. New edits must use execute/register_applied. |
| Layers and object stacking | scene layer model, layer panel/commands | Layer undo and stacking round-trip tests. |
| Image import/calibration | background image items, calibration dialog | Existing image/calibration tests; human placement/import still unverified. |
| Project save/load | `core/project.py`, `.ogp` JSON, version 1.4 | Item matrix and old-format stacking tests; real app save/reopen. Browser `.clp` is unrelated. |
| Autosave/recovery | `services/autosave_service.py`, crash handling | Autosave tests; crash/recovery dialogs need human checks. |
| PNG/SVG/CSV exports | `services/export_service.py` and shopping-list service | Inherited export tests; actual process PNG/CSV. |
| PDF and DXF | report service and DXF services | Actual process PDF/DXF validates signature/geometry. CAD interoperability and printing unverified. |
| Date/time sun and shadows | `core/solar.py`, `shadow_geometry.py`, `sun_shadow_controller.py` | Solar/geometry/overlay integration tests. No replacement solar engine. Actual site accuracy and usability are D. |
| Shade accumulation/heatmap | `core/shade_aggregation.py`, shade heatmap/controller | Existing aggregation/overlay tests; future C/D landscape examples and explanatory legends. |
| 3D | shipped Qt3D adapter; separate dormant Qt Quick 3D spike | Import/version self-test only. Offscreen skips and GPU interaction remain unverified. |
| Optional automation | `agent_api/` providers, bridge, loopback MCP | Real app queries/render/save/export; writes left disabled. Preserve security tests. |
| Native downloads | upstream `installer/ogp.spec`, `build_installer.py`, NSIS | Windows CI freezes/installs/exercises actual editor. Mac package/signing deferred. |

The inheritance is intentional: A adds traceability and distribution checks,
without changing application algorithms, commands, serialization, assets or UI
strings. UI rebranding and workflow reduction will be explicit later milestones.
