# Creative desktop design system — proposed

Prepared October 7, 2026, America/Detroit. **Visual approval pending.**
This document implements the first-task scope of [CREATIVE_REDESIGN_BRIEF.md](CREATIVE_REDESIGN_BRIEF.md).
It supplements [MASTER_PLAN.md](MASTER_PLAN.md); Windows delivery, macOS,
imperial units, licensing, recovery and validation remain required.

## Evidence and authority

| Classification | Evidence / status |
| --- | --- |
| Verified company specifications | None supplied: no approved logo, font files, photography or brand standards in this checkout. |
| Website extraction in this task | None. The portfolio URL returned a network proxy 403. Its current CSS and typefaces could not be inspected. |
| Reference observations supplied by the brief | Circular tree emblem with serif lettering; navy/gold/pale gray-blue testimonial treatment. These are references, not exact verified specifications. |
| Proposed adaptation | All hex values, font pairing, layout and placeholder identity below. Approval of a direction does not establish rights to redistribute company assets. |

The navy identity block is **plain text explicitly labeled “Identity placeholder.”**
It is not an approximation of the official logo. The editor uses the inherited
Tabler icons and existing plan artwork, with their notices retained. No company
photos, partner logos, proprietary catalogs or new font binaries were imported.
See [asset inventory](assets/creative/README.md).

## Color tokens

Authoritative implementation: [creative_theme.py](src/open_garden_planner/ui/creative_theme.py).
The dictionaries adapt the existing semantic theme roles. Unchanged roles inherit
their upstream defaults through `apply_theme(..., color_overrides=...)`.

| Proposed name | Light value | Intended role |
| --- | --- | --- |
| Creative Navy | `#123B63` | Primary actions, active controls, focus |
| Deep Navy | `#102B46` | Identity surface |
| Heritage Gold | `#B79A4C` | Decorative welcome rule; never small text on white |
| Warm Ivory | `#F7F6F1` | Application / welcome background |
| Panel White | `#FFFFFF` | Inputs and panels |
| Slate Ink | `#263441` | Main text |
| Muted Slate | `#596875` | Secondary and readable disabled text |
| Limestone | `#D8DDD9` | Outside canvas and supporting surfaces |
| Control Outline | `#71808B` | Essential boundaries |
| Lake Mist | `#E7EEF3` | Selection / hover surface |
| Landscape Green | `#42644C` | Success and planting support |
| Error Red | `#A33131` | Errors |

Supporting light status ink: warning `#8A4B08`, caution `#715A1D`.
Gold is not used as interaction focus or as ordinary text on a light surface.
Placeholder text on navy uses a separate, readable `#D8BC71`.

| Dark semantic role | Value |
| --- | --- |
| Background / panel | `#17232F` / `#1E2D3B` |
| Main / secondary / disabled text | `#F3F5F6` / `#BAC8D3` / `#A6B5C2` |
| Input / hover / selection | `#17232F` / `#304658` / `#304658` |
| Control outline | `#8295A5` |
| Active action / focus | `#8CC6FA`, with `#102B46` action text |
| Success / warning / caution / error | `#A3C7A9` / `#F2BC79` / `#D8BC71` / `#FFA5A5` |

Canvas background `#F7F7F4`, grid `#D5D9D6` / `#B4BDB7`, scale-bar ink
`#263441` and outside surface `#D8DDD9` remain light in both modes. Object
artwork, site images, selection handles and domain geometry are not inverted.
The synthetic sample lawn uses an existing solid fill; this does not change
any user's saved plans or the default object styles.

Calculated text and essential-control pairings are recorded in
[contrast.csv](docs/design/contrast.csv) and enforced by
[test_creative_contrast.py](tests/unit/test_creative_contrast.py). Tested text pairs
meet 4.5:1; tested control boundaries meet 3:1. This is **token-level evidence**,
not a certification of every inherited dialog, native glyph or composite image.

## Typography and density

- Proposed functional face: Source Sans 3, regular / semibold; 14 logical px.
  Installed-font fallbacks: Segoe UI, Helvetica Neue, DejaVu Sans, Qt default.
- Proposed limited heading face: Source Serif 4, semibold; welcome title 32 px.
  Fallbacks: Georgia, DejaVu Serif, Qt default.
- Cloud captures use **DejaVu Sans and DejaVu Serif**. Source fonts are not
  installed or bundled. No font network request occurs at startup.
- Measurements remain in the existing numeric widgets, right aligned. Native
  tabular-numeral behavior needs font/platform verification; it is not claimed.
- Compact density, 16–18 px panel-heading tuning and approved local font
  bundling are follow-up work after approval. Do not shrink fields to hide overflow.

## Components and interactions in the experiment

| Component | Actual implementation |
| --- | --- |
| Project bar | Labeled identity placeholder; actual file name and dirty state; shares existing New/Open/Save QAction objects and sun action. |
| Main tool row | Existing Select, Measure, Text, Callout, Journal and CAD constraints. Labels and tooltips retained. |
| Category row | All 11 existing categories, readable compact labels, original dropdowns and Ctrl+F global search. No invented commands. |
| Left dock | Compact 36 px thumbnails, category filter, text search, keyboard activation; items come from the existing gallery registry. Library and Layers tabs. |
| Layer tab | Second pure view of the existing scene. All mutations use the existing undoable layer handlers. Original accordion remains intact. |
| Right dock | Original contextual property panels, with labels above fields to avoid clipping. Content scrolls; original sidebar order and pin/peek behavior retained. |
| Workspace controls | View → dock toggles, Focus canvas, Reset workspace. Preview account remembers dock visibility/size. F11 fullscreen handles the added chrome. |
| Sun row | Existing date, time slider, Animate/play-pause and Hours of Sun heatmap; a concise geometric-model/computer-time-zone label. |
| Welcome | New/Open, real recents, file-modification dates, existing missing-file safeguards, Clear recent list, startup preference and Close. |

The welcome thumbnail in the capture is a **real canvas grab of the same saved
synthetic project**, injected by the capture runner. Automatic thumbnails for
arbitrary recent files are deferred, not an implemented cache. Recovery keeps its
existing startup sequence; no new recovery cards or template buttons are shown.

The current inherited sun controls use the **computer's local time zone**;
captures run with America/Detroit and show EDT. No project-time-zone control,
weather-adjusted radiation model or new solar engine is implied.

The editor capture measures 63.2% of horizontal width for the canvas at 1920×1080
with both docks open. This is slightly below the 65–75% target because existing
property controls need 485 px at the readable font size. Focus canvas hides both
docks. At 1280 px the two-dock workspace is crowded: use Focus canvas, then open
the needed dock. A denser essentials/advanced property layout is proposed for the
next increment rather than concealing controls or shrinking type in this review.

## Implementation boundary and fallback

This is the real `GardenPlannerApp` subclass, with the existing `CanvasView`,
scene, tools, ProjectManager, CommandManager, controllers, exports and dialogs.
It is entered only by [creative_design_preview.py](scripts/creative_design_preview.py).
The normal module entry point remains unchanged. No browser/UI framework or
parallel landscape model was introduced.

The shared theme extension supplies colors to the existing stylesheet/listener
pipeline. Additional styles target named preview components; a second enormous
application stylesheet is not introduced. Ordinary `apply_theme` restores the
upstream palette. A normal application restart / `--original` reference run uses
the existing interface. No project-format, internal-unit or package-ID change.

See [ADR-050](docs/09-architecture-decisions/README.md#adr-050-opt-in-creative-desktop-design-preview)
for isolation and the unchanged sidebar contract.

## After visual approval

Apply the approved direction incrementally to the real application entry point,
owned dialogs and preferences; finish essentials/advanced properties and responsive
layout; test all component states in light/dark, especially native dock glyphs and
disabled controls. Retain a theme fallback until visual regressions pass.

Approved company assets and font notices can then replace placeholders. Optional
export title blocks must follow the existing export architecture and preserve
scale, north, grayscale legibility and vectors. Imperial entry/display and native
Windows/macOS package QA remain separate required master-plan work. Build a new
Windows test installer only after this approval gate and relevant checks pass.
