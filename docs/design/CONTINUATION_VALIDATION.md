# Creative continuation validation

Evidence: 2026-10-08 UTC. Branch `feature/creative-design-preview`; draft PR [#3](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/pull/3). Implementation follows the verbatim [continuation brief](../../CREATIVE_CONTINUATION_BRIEF.md), the master plan and redesign brief. The color direction is approved; revised layout approval is pending.

## Executed checks

Final reviewed source: `7cfbcdc7746c3ae24806ebc7f12cd5ea3f986f90`. Documentation/capture commits after this SHA do not change application source.

| Check | Result |
| --- | --- |
| Final full suite on the reviewed source | **7,711 passed / 36 skipped / 42 warnings in 570.74 s**, exit 0. Skips are GPU/RHI/render-tier, Windows registry and Windows Qt-runtime-specific checks. |
| Final imperial workflow | **51 passed in 25.71 s**: actual input, peer precision, units/annotations/undo, save/reopen, recovery snapping, materials, shortcuts, CAD declared-unit conversions and fractional soil/container-height initialization/steps. |
| Expanded UI/i18n/offset regression | **118 passed in 50.13 s**. |
| Interoperability/units/project regression | **68 passed in 1.93 s**; later declared-unit expansion **91 passed in 24.14 s**. |
| Independent source re-review | **106 passed in 66.09 s** in a fresh ordinary clone: 95 committed checks plus 11 independent probes; **no outstanding P0/P1**. See [review](../reviews/CREATIVE_CONTINUATION.md). |
| Ruff | **Passed** over src/, tests/, scripts/. |
| Bandit HIGH | **Passed**, zero high-severity findings. |
| Translations | Fill/compile passed; German/i18n regression **23 passed**. |
| Repository gates | Agent parity, skill citations, tracked secret scan and git diff whitespace passed. |
| Source self-test | **Passed**: six Qt3D imports, matching runtime/wheel 6.11.0, Agent API server binding. This is not a frozen Windows test. |
| Real source screenshots | Light/dark 1920 × 1080 and small 960 × 720; welcome/editor/imperial/Sun Study, captured from the reviewed source. Qt 6.11.0 Linux offscreen, computer zone America/Detroit. Per-variant evidence.json records source SHA, fonts, window/canvas size, solar state and serialized scene. Canvas widths: 1,380 / 1,920 (71.9%) and 654 / 960 (68.1%); the small-screen library is collapsed through its real dock control. |

### Failed and interrupted runs, distinguished from passing evidence

- Initial full suite: **7,664 passed / 2 failed / 36 skipped / 42 warnings in 513.57 s**. Failures were stale benchmark fixtures containing only additive preferences and an icon-source guard seeing a parser minus literal. Object geometry was unchanged when regenerating fixtures; normalization now names the Unicode code point. Both failed checks passed in the affected 61-test rerun.
- A startup-test observer scheduled before QApplication caused a timeout; the observer was corrected after tracing Qt's missing event dispatcher, without changing production startup or increasing its timeout. A full rerun was deliberately interrupted at **248 passed / 13 skipped in 113.66 s** before correcting that observer.
- Clean complete suite at `510cda0`: **7,669 passed / 36 skipped / 42 warnings in 530.18 s**. Independent review then exposed six retained-workflow defects not covered by those tests. Their fixes and new regressions produced another clean complete run at `004d2ff`: **7,684 passed / 36 skipped / 42 warnings in 528.78 s**.
- A narrow-window regression initially asserted width before Qt completed layout (**117 passed / 1 failed**). It now waits for the actual measured label width while retaining the assertion.
- Subsequent independent review found declared-unit factor clamping/survey gaps and default-constructor precision. The old-source suite at `afa1bb7` was deliberately interrupted at **956 passed / 13 skipped / 42 warnings in 238.73 s** so the final run uses the corrected constructor. Those issues passed their targeted checks and final independent re-review.
- The earlier instrumented lifetime run was interrupted after identifying popup ownership. Its integration prefix (**652 passed / 13 skipped in 351.92 s**) is diagnostic evidence, not a complete suite pass. CategoryDropdown ownership, deferred test deletion and repeated styling were corrected; tests/assertions were retained and no timeout was raised.

## Unit coverage

| Surface | Behavior |
| --- | --- |
| New Creative project / legacy files | Imperial default for new; absent preferences mean metric. Internal cm and `.ogp` 1.4 remain. |
| Drawing / typed coordinates | Feet/inches, decimal feet, fractions, explicit cm/m/mm/in/ft and negative coordinates; comma/semicolon component separators; `@` relative and `<` polar retained. Imperial decimal punctuation is a dot. |
| Properties / plant sizes / arrays | Canonical cm signals with project display units; units fixed for each active editor so switching cannot reinterpret pending text. Controls rebuild or refresh on unit change. |
| Dimensions / measurement / rulers / handles / coordinates | Project-aware feet/inches or decimal feet; inch display rounds to 1/64 only for display, never saved into geometry. |
| Grid / snapping | Default new grid 1 ft; editable physical spacing, persisted as cm, undoable. Snap distances remain canonical; project load/recovery synchronizes every attached view through CanvasScene. |
| Image calibration / guides / fillet / chamfer | Explicit physical input converted once to cm. |
| Areas / soil and mulch | ft² and yd³; price conversions preserve total cost and canonical saved price meaning. |
| PNG/SVG/PDF | Render real project labels/symbols; PDF scale bar now represents its actual physical length. Paper size captions/plan dimensions adapt; numeric scale ratios remain unitless. |
| DXF | Imperial entities in feet with INSUNITS=2; metric cm with 5; source geometry unchanged. Import defaults derive from declared units; explicit overrides retained; unknown/unitless files default to 1 cm per unit. |
| CSV | Imperial numeric `_ft` columns, including actual plant centers; metric columns retain cm headers and now report the actual plant center too. |

Remaining scientific/canonical surfaces: gardening fertilizer/pest/harvest data uses grams/kg/L and scientific rates, soil chemistry and weather retain their original units, provider/Agent API data and internal schemas remain cm. Paper margins and printer standards retain mm/cm calculations; imperial architectural scale presets (for example 1/8 inch = 1 foot) are not added. Location time-zone selection is not implemented: sun controls use computer-local time and convert to UTC.

## Presentation and compatibility limits

The sample's curved bed is an editable sampled polygon, not a spline bed. Original architectural linework is an option alongside detailed SVG symbols; plant metadata and footprints stay unchanged. Texture strength adjusts painting independently. The inherited shadow overlay sits below objects: opaque ground/materials can conceal shade; the synthetic lawn uses a translucent fill so the live shade is visible. No replacement solar engine is introduced. A company logo, finished title blocks, curated local plant catalog, and broader Land F/X workflows remain future master-plan stages.

## Platforms and download gate

No new Windows build exists for this continuation. The available foundation artifact was built from `439e486414070161d9fea58a6123644e8d0afdc3` and contains the earlier interface; see [Windows download](../WINDOWS_DOWNLOAD.md). Do not use it to assess these screenshots or imperial work.

Revised visual approval precedes another installer, as requested in continuation brief §8. Native Windows packaged startup/fonts/icons/drawing/input/save/reopen/exports are **not tested for these changes** yet. Signing and human testing remain pending. macOS previously passed dependency/source self-test on Apple Silicon and Intel; **no working Mac installer is established**, and the continuation has not run on a Mac. Qt3D GPU, native dialogs, accessibility and real display scaling require native/manual checks. Context7 is unavailable; the implementation uses installed Qt bindings and existing repository patterns. The separate upstream wiki checkout is absent, so no external wiki was synchronized.
