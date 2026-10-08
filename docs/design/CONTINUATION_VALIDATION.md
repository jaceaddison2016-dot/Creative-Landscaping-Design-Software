# Creative continuation validation

Evidence: 2026-10-08 UTC. Branch `feature/creative-design-preview`; draft PR [#3](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/pull/3). Implementation follows the verbatim [continuation brief](../../CREATIVE_CONTINUATION_BRIEF.md), the master plan and redesign brief. The color direction is approved; revised layout approval is pending.

## Executed checks

- Focused continuation regression: **134 passed in 32.24 s**, including actual property/drawing input, fractional inches, negative coordinates, repeated unit switching, undo/redo, save/reopen, calibration, DXF/CSV physical references, material costs, workspaces, popup destruction, German strings and retained dialogs.
- Initial full suite: **7,664 passed, 2 failed, 36 skipped, 42 warnings in 513.57 s**. Failures were stale benchmark fixtures (only additive default preferences) and an icon-source guard seeing a parser minus literal. Fixtures regenerated with unchanged objects; normalization now names the Unicode code point without a UI-icon literal. Both checks passed in the affected 61-test run (32.64 s). A fresh full-suite rerun is required before handoff. Earlier diagnostic lifetime run was interrupted after identifying ownership. The instrumented integration prefix completed 652 passed / 13 skipped in 351.92 s; it is diagnostic evidence, not the final full-suite result.
- Ruff passed on source and capture script. Bandit HIGH passed. Translation fill/compile passed; the focused i18n suite passed (23 tests). Agent parity passed; moved source citations updated for the citation gate.
- Source captures: real Qt 6.11.0 on Linux offscreen, with local computer zone America/Detroit. See per-variant evidence.json for canvas/window size, fonts, sun state and serialized scene. Light/dark 1920 × 1080 and 960 × 720 captures complete; final recaptures reflect compact coordinate rows. Canvas widths: 1,380 / 1,920 (71.9%) and 654 / 960 (68.1%), with the small-screen library collapsed through its real dock control. Independent source review is pending.

## Unit coverage

| Surface | Behavior |
| --- | --- |
| New Creative project / legacy files | Imperial default for new; absent preferences mean metric. Internal cm and `.ogp` 1.4 remain. |
| Drawing / typed coordinates | Feet/inches, decimal feet, fractions, explicit cm/m/mm/in/ft and negative coordinates; comma/semicolon component separators; `@` relative and `<` polar retained. Imperial decimal punctuation is a dot. |
| Properties / plant sizes / arrays | Canonical cm signals with project display units; units fixed for each active editor so switching cannot reinterpret pending text. Controls rebuild or refresh on unit change. |
| Dimensions / measurement / rulers / handles / coordinates | Project-aware feet/inches or decimal feet; inch display rounds to 1/64 only for display, never saved into geometry. |
| Grid / snapping | Default new grid 1 ft; editable physical spacing, persisted as cm, undoable. Snap distances remain canonical. |
| Image calibration / guides / fillet / chamfer | Explicit physical input converted once to cm. |
| Areas / soil and mulch | ft² and yd³; price conversions preserve total cost and canonical saved price meaning. |
| PNG/SVG/PDF | Render real project labels/symbols; PDF scale bar now represents its actual physical length. Paper size captions/plan dimensions adapt; numeric scale ratios remain unitless. |
| DXF | Imperial entities in feet with INSUNITS=2; metric cm with 5; source geometry unchanged. |
| CSV | Imperial numeric `_ft` columns, including actual plant centers; metric columns retain cm headers and now report the actual plant center too. |

Remaining scientific/canonical surfaces: gardening fertilizer/pest/harvest data uses grams/kg/L and scientific rates, soil chemistry and weather retain their original units, provider/Agent API data and internal schemas remain cm. Paper margins and printer standards retain mm/cm calculations; imperial architectural scale presets (for example 1/8 inch = 1 foot) are not added. Location time-zone selection is not implemented: sun controls use computer-local time and convert to UTC.

## Presentation and compatibility limits

The sample's curved bed is an editable sampled polygon, not a spline bed. Original architectural linework is an option alongside detailed SVG symbols; plant metadata and footprints stay unchanged. Texture strength adjusts painting independently. The inherited shadow overlay sits below objects: opaque ground/materials can conceal shade; the synthetic lawn uses a translucent fill so the live shade is visible. No replacement solar engine is introduced. A company logo, finished title blocks, curated local plant catalog, and broader Land F/X workflows remain future master-plan stages.

## Platforms and download gate

No new Windows build exists for this continuation. The available foundation artifact was built from `439e486414070161d9fea58a6123644e8d0afdc3` and contains the earlier interface; see [Windows download](../WINDOWS_DOWNLOAD.md). Do not use it to assess these screenshots or imperial work.

Revised visual approval precedes another installer, as requested in continuation brief §8. Native Windows packaged startup/fonts/icons/drawing/input/save/reopen/exports are **not tested for these changes** yet. Signing and human testing remain pending. macOS previously passed dependency/source self-test on Apple Silicon and Intel; **no working Mac installer is established**, and the continuation has not run on a Mac. Qt3D GPU, native dialogs, accessibility and real display scaling require native/manual checks. Context7 is unavailable; the implementation uses installed Qt bindings and existing repository patterns. The separate upstream wiki checkout is absent, so no external wiki was synchronized.
