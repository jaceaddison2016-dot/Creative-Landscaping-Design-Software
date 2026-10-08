# Creative preview validation

October 7, 2026, America/Detroit. This evidence concerns an **opt-in source
experiment**. The Windows artifact recorded in PLATFORM_STATUS.md predates this
design; it does not contain these changes. No installer/release is produced while
visual approval is pending.

## Executed checks

| Check | Result / scope |
| --- | --- |
| Focused Qt / contrast / i18n run | 71 passed in 20.28 s after review fixes: 9 preview integration workflows, 39 contrast cases, 23 inherited i18n checks. Includes real subprocess launcher/restart/capture isolation. |
| Preview-only rerun after layout refinements | 8 passed. |
| Contrast measurements | 40 explicit pairings in contrast.csv; minimum tested text ratio 4.89, control ratio 3.76. |
| Source captures | All six capture processes exited zero; real before/light/dark/narrow/150%/200% editor and welcome PNGs. |
| Translation generation | New CreativePreview and inherited-footer contexts registered; German TS filled and QM compiled. Existing fill-script “MISSING” entries have translations already stored in TS; the unfinished-message gate passes. |
| Ruff | Passed after import formatting. |
| Bandit HIGH | Passed, no HIGH findings. |
| Agent context / citations | Passed. |
| Secret scan | Passed on tracked files; repeat after staging the new files. |
| Full inherited suite | Not completed. Two full runs and an alphabetical-prefix reproduction were interrupted after prolonged Qt styling work around the preview theme tests. Instrumentation observed roughly 79,000 retained widgets; the focused run completes. Root cause is not fully isolated, and no full-suite green result is claimed. CI/full-suite completion remains a gate before landing. |
| Independent senior review | First review of 439e486..c8859ed found sample-file overwrite, launcher preference/translation defects, fullscreen sun chrome and a broken link. Fixes and regression coverage are recorded in docs/reviews/CREATIVE_DESIGN_PREVIEW.md; clean re-review pending. |

The full suite includes drawing, selection, dragging, snapping, numeric editing,
undo/redo, layers, project serialization, recovery, solar/shadow and export tests.
Focused preview tests additionally drive a real library click → real inherited
tree gesture → undo/redo → save/reopen; synchronized layer commands; dock
restoration/fullscreen; light/dark/fallback; New/Open/recent/missing-file handling
and actual German translation loading, including the inherited footer.
The subprocess launcher test additionally verifies a saved edited sample,
German menus, dark theme, window geometry, hidden docks and suppressed welcome
survive an interactive restart and a separate screenshot capture.

## Capture conditions and limits

Linux cloud, Python 3.12.14, Qt/PyQt6 6.11.0, offscreen platform. DejaVu Sans
functional font / DejaVu Serif heading fallback; no Source font binaries.
`TZ=America/Detroit`; synthetic garden at 42.1, -86.48; 2026-06-21 16:00 local
sun study. Every evidence.json records actual Qt version, font, geometry, DPR,
active sun-controller state and the serialized synthetic plan snapshot.

| Capture directory | Logical editor size | DPR | Observed canvas-width share |
| --- | --- | --- | --- |
| before | 1920×1080 | 1 | 76.5% |
| light / dark | 1920×1080 | 1 | 63.2% |
| narrow | 1280×800 | 1 | 44.8% |
| scale150 | 1280×720 | 1.5 | 44.8% |
| scale200 | 960×600 | 2 | 38.8% |

Scaling uses Qt's scale-factor setting; it is **not native Windows/macOS OS
scaling verification**. At narrow widths the toolbars use Qt overflow, the
property form scrolls and both docks consume too much drawing room. Focus canvas
and the View dock toggles are available. A responsive essentials/advanced form
and compact mode remain follow-up work. At 200% the existing 600-logical-pixel
minimum height requires a 1200-pixel-tall window; fitting a 1080-pixel screen at
that scale needs additional layout work. Native dock glyphs, all inherited
dialog states and complete screen-reader behavior still require visual/manual QA.

Before captures use the unchanged upstream classes with a fresh isolated
reference capture account. Proposed captures use the real app subclass with a
separate capture account and fixture path; capture never replaces the interactive
sample or its settings. Both use the same serialized synthetic fixture;
selected patio geometry is unchanged. Capture setup opens the actual Properties
accordion and switches off the existing object-name-label action. These are
normal UI states, not drawn overlays. The warm solid lawn is sample-project
styling using existing properties, shared by before and after.

## Repeat a capture in the prepared cloud checkout

```bash
QT_QPA_PLATFORM=offscreen TZ=America/Detroit \
XDG_CONFIG_HOME=$PWD/build/cloud-state/config \
XDG_DATA_HOME=$PWD/build/cloud-state/data \
XDG_CACHE_HOME=$PWD/build/cloud-state/cache \
.venv/bin/python scripts/creative_design_preview.py --capture build/creative-preview/review
```

Use `--original` or `--dark` for the corresponding reference/alternative. For
150% use `QT_SCALE_FACTOR=1.5 --width 1280 --height 720` (put the environment
assignment before the command, and the flags after it); for 200%, factor 2 and
960×600. Captures reset only their capture account's UiState group for repeatability.
Interactive source preview keeps its workspace preferences and saved sample edits.

## Not tested / not changed

- No new native Windows/macOS package, installer, signing or font/icon packaging
  verification at this approval gate. Native GPU rendering remains unverified.
- No human keyboard/mouse usability or assistive-technology session. Automated
  interactions and accessible names cover the new controls, not the full app.
- No optional plant API, weather or satellite-network verification; dependencies,
  service behavior and production API defaults are unchanged. Preview automation
  is disabled in the isolated account.
- No official website style verification (proxy 403), logo/photography permission,
  downloaded font or title-block artwork. Asset approval inventory records this.
- No imperial-unit implementation, solar algorithm, schema/version change or
  broad dialog redesign. These requirements remain in MASTER_PLAN.md.
- Context7 tooling is not available here. Interfaces were checked against the
  installed Qt bindings and repository source; no Context7 verification is claimed.
- Wiki checkout is absent; wiki sync remains pending.
