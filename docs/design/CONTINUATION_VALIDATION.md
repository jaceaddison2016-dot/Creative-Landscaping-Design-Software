# Creative continuation validation

Evidence: 2026-10-08 UTC. Branch `feature/creative-design-preview`; draft PR [#3](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/pull/3). Implementation follows the verbatim [continuation brief](../../CREATIVE_CONTINUATION_BRIEF.md), the master plan and redesign brief. The owner approved the color direction and revised layout and authorized the matching Windows test build.

## Executed checks

Reviewed visual source: `7cfbcdc7746c3ae24806ebc7f12cd5ea3f986f90`. The following table records that source stage. The subsequent packaging stage adds an opt-in workflow diagnostic; its completed source/native results are recorded separately below.

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

The owner's visual approval satisfies continuation brief §8. A matching
[Windows test download](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773267264/artifacts/11549062663)
now includes these changes and passed native validation. The exact application
source is **`7c07a3220f0178f28ab7cf1b38a356cc6ff2aff1`**. Subsequent delivery
commits contain documentation and recorded evidence only. Older foundation
downloads have the earlier interface; use [current instructions](../WINDOWS_DOWNLOAD.md).

| Final packaging-stage check | Result |
| --- | --- |
| Complete source suite on build source | **7,726 passed / 36 skipped / 42 warnings in 576.91 s**, exit 0. |
| Source CI on build source | [Run 37773266704](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773266704) **success**. |
| Independent review | Safety fixes: **35 passed** plus separate recovery-sentinel probe. Native-platform correction: **65 focused passed**; final recorder check: **7 passed**. No outstanding P0/P1; see [packaging review record](../reviews/CREATIVE_WINDOWS_PACKAGING.md). |
| Ruff / Bandit HIGH / repository gates | Passed: src/tests/scripts lint, zero HIGH security findings, context parity, skill citations, tracked secrets and whitespace. |
| Native Windows source regression | **282 passed in 105.49 s**, Qt native Windows plugin. |
| Portable frozen application | PASS: subsystem self-test without inherited console handles, ≥8 s normal startup, actual-process MCP save/reopen/exports, real Qt key/mouse workflows. |
| Installed frozen application | PASS: NSIS silent installation, subsystem/normal-process checks, the same real Qt workflows. |
| Eight real Qt workflows, both copies | Typed drawing, mouse plant placement, fractional-inch edit, Ctrl+Z/Ctrl+Y, save/reopen, PNG/PDF/DXF/CSV, fonts/icons and live sun/shade. |
| Distribution integrity | PASS: portable runtime, installer executable, exact application source and PyQt binding source ZIP contents/CRC; licenses/notices/checksums included. |
| Artifact | [Run 37773267264](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773267264) **success**, 444.6 MiB test artifact uploaded. |
| Actual installed Windows captures | [Four original PNGs and results](windows-verified/README.md), source SHA/native identity validated, hashes matched, complete PNG decoding verified; visually inspected. |

### Packaging failures and their resolution

- Independent review reproduced recovery loss in a scratch directory: isolating
  QSettings alone left the diagnostic using the normal temporary autosave path.
  A direct-CLI regression failed before the fix. The opt-in diagnostic now retains
  a private TemporaryDirectory and switches process-local temporary storage before
  constructing the app. A real-entry-point sentinel test proves existing recovery
  bytes survive; normal application recovery remains unchanged.
- On Windows, giving only stdin DEVNULL caused Python to duplicate parent output
  handles despite DETACHED_PROCESS/close_fds. The frozen driver now passes all three
  streams as None; the child checks GetStdHandle. Both native results confirm no
  inherited standard handles. The source subprocess retains isolated logs.
- [Run 37770416502](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37770416502)
  (`f6789d3`): **272 passed / 3 failed in 99.63 s**. Diagnostic
  [run 37771677509](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37771677509)
  (`d928a8a`): **272 passed / 3 failed in 89.72 s**. Both stopped before freezing
  or making an installer. Their Windows offscreen plugin had an empty font database,
  including no ASCII digit glyphs, and distorted the narrow-window text measurement.
  The source Windows checks now use the native Windows plugin; font/layout assertions
  were retained. The successful run passed all 282 checks without a product layout
  or font workaround.
- Intermediate complete Linux runs remain distinct: **7,713 passed / 36 skipped /
  42 warnings in 565.02 s**, then safety-fix source `f6789d3` **7,719 passed /
  36 skipped / 42 warnings in 577.20 s**. The final 7,726-result suite above supersedes
  them for the actual build source.

### Remaining limits

Signing and human testing remain pending. The native runner's 1028 × 749 overview
with both docks open exposes overlapping/clipped plant labels; zoom or close/resize
docks. The imperial screenshot's width editor is below its visible scroll area,
while the test records its exact physical result. Sun activation is automated and
shadow paths are visible in the captures, but pixel accuracy is not asserted.
The probe uses fixed Qt waits, so slower native machines may need investigation if
automation fails. These limits are not represented as manual passes.

macOS previously passed dependency/source self-test on Apple Silicon and Intel;
**no working Mac installer is established**, and the continuation has not run on
a Mac. GPU 3D, printing, native dialogs, accessibility, real display scaling,
upgrades/uninstall, Windows ARM/older OS and antivirus acceptance remain untested.
Optional online providers were not exercised. The Linux task could not download
the whole binary artifact through its current storage-host allowlist; archive checks
and app execution occurred on Windows, and native captures were retrieved through
GitHub logs with exact hash/PNG verification. Cloud startup/network changes are
saved as an unpublished configuration draft for review; they are not active here.
Context7 is unavailable; installed Qt bindings and repository patterns were used.
The separate upstream wiki checkout is absent; wiki sync remains pending.
The PR remains draft; no merge, tag or production release was created.
