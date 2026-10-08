Creative Landscape Studio — Codex master implementation plan

Prepared for Jace Addison, October 7, 2026. This is an implementation brief, not a claim that the software has already been built or validated.

1. Binding project direction

Build a standalone landscape-design desktop application for macOS and Windows by adapting the actual Open Garden Planner codebase. Preserve and extend its mature editor, project model, commands, drawing tools, exports, plant metadata, and solar functionality. Do not replace this direction with another independent HTML/JavaScript planting demo.

Product owner: Jace Addison, a nonprogrammer and landscape consultant at Creative Landscaping & Design in southwest Michigan. He can direct development from his iPhone; the finished design application is intended to run on Mac and Windows computers. Do not confuse mobile project management with a requirement to run the Python/Qt editor inside iPhone Safari.

Target repository: https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software

Upstream: https://github.com/cofade/open-garden-planner

Prior inspection baseline: version 1.29.5, commit cb4a71db8649cc4e48f85f0bef671bb0ac58dd16. This is a known reference, not a mandatory assumption about the latest release. Inspect current upstream, choose a stable baseline, and record the exact revision and rationale before importing it.

The existing branch prototype/landscape-workspace and draft PR #1 contain a small independent browser demo. Preserve them as historical work. Do not silently merge, delete, or build the new desktop architecture on top of that demo. Use a separate implementation branch based on the appropriate target repository baseline.

Success means a useful landscape-design workflow, not merely a polished screenshot or a long feature list.

2. Mandatory reuse and provenance

Import a traceable upstream baseline into this repository through a deliberate, documented fork/import process. Prefer preserving upstream history in the implementation branch where practical; if using a source snapshot, preserve attribution and record the upstream SHA and import procedure. The app must be runnable from this repository without manually retrieving an undocumented second project.

Before editing imported code, read all applicable AGENTS.md instructions and relevant upstream architecture/testing guidance. Do not weaken required review or safety policies. If inherited instructions require an unavailable reviewer or action outside current authority, report that specific limitation instead of fabricating compliance.

Create an upstream provenance document with repository URL, SHA, version, import date, license, subsequent changes, dependency notices, and update procedure. Keep customization commits distinct from the initial import. Avoid unnecessary package/module renaming until baseline behavior is proven; change user-facing branding separately.

Inspect and preserve LICENSE, copyright statements, bundled asset/data attribution, and dependency obligations. The inspected upstream declares GPL-3.0-or-later. This reuse strategy accepts preserving that licensing for the derived code; do not describe the result as proprietary or remove attribution. Document distribution/source obligations and review Qt, fonts, symbols, plant imagery, and datasets separately. If the owner later requires closed-source distribution, stop and revisit the architecture/licensing rather than concealing inherited code. Do not copy Land F/X code, proprietary catalogs, icons, documentation, or trade dress. Do not imply affiliation with either upstream or Land F/X.

Use this capability matrix before inventing replacement modules:

|Capability                                       |Required treatment                                                                            |
|-------------------------------------------------|----------------------------------------------------------------------------------------------|
|2D canvas, object model, selection, editing      |Reuse existing architecture and interactions; extend only where needed                        |
|Commands, undo/redo, snapping, precision drawing |Preserve existing tools and command behavior                                                  |
|Layers, reusable symbols, object library         |Preserve and adapt for landscape workflows                                                    |
|Image import and calibration                     |Preserve; make site-plan setup easy                                                           |
|Plant metadata and optional online search        |Reuse; add curated local data without depending on an API account                             |
|Project save/load, autosave and recovery         |Preserve; test compatibility and recovery                                                     |
|PDF/SVG/PNG/DXF and plant-list exports           |Verify current behavior before extending                                                      |
|Solar calculations, footprints, shade aggregation|Inspect and reuse existing implementation; do not create a parallel solar engine unnecessarily|
|3D viewer and growth features                    |Preserve if stable; accurately explain their present limitations                              |
|Windows packaging                                |Reuse the existing packaging path where suitable                                              |
|macOS packaging                                  |Investigate and implement; portability is not established merely because Qt supports macOS    |

For every proposed feature, classify it as working/reused, existing but needing verification, adapted, new, or deferred. Link reused capabilities to actual source modules and tests. Do not turn README claims into verified results.

3. Architecture and scope boundaries

Keep Python/PyQt6 and the existing graphics-scene architecture for the first desktop release. Do not port the application to Electron, a browser engine, another CAD kernel, or a new framework without explicit owner approval supported by a concrete blocker report.

Follow existing separation of domain logic, graphics objects, commands, persistence, and UI. Keep new calculations independently testable. Route editing through the established undo/redo mechanism, and extend existing serialization compatibly. Avoid giant replacement files and unnecessary dependency additions.

Keep the existing internal physical units initially, normally centimeters in the inspected baseline. Add a centralized imperial input/display conversion layer. Do not scatter conversions across widgets or rewrite all coordinates to inches. Unit preferences must not change physical geometry.

Windows is required; macOS is required. Apple Silicon is a priority candidate, but confirm the owner’s actual Mac hardware before promising a matching installer. Intel Mac support is a separate target to investigate and report, not an automatic universal-binary claim.

Default to local/offline work. No mandatory account, subscription, remote upload, or plant API credential for ordinary editing. Optional online lookup must fail gracefully. Do not expose the embedded agent server to the network; inspect its existing authentication/loopback defaults and keep optional automation secure.

4. Milestone A — working upstream baseline and platform gate

Do this before a major visual redesign.

1. Inventory target branches and existing work; preserve unrelated changes.
2. Inspect upstream releases, source, instructions, dependency pins, packaging, and known platform issues. Choose a documented baseline.
3. Import actual source with required notices and provenance.
4. Install using the project’s supported dependency workflow. Respect matched Qt/Qt3D versions; do not arbitrarily upgrade or downgrade packages to make one import pass.
5. Launch the editor where the environment permits. Exercise drawing, selection, undo/redo, layers, image calibration, plant editing, save/reopen, export, and sun tools. Run the relevant upstream checks and record results, skipped tests, and failures.
6. Add reproducible CI for Linux, macOS, and Windows where runners and permissions are available. Include Qt imports, core tests, application startup, resource loading, and save/export smoke tests. Offscreen tests are useful but not equivalent to human desktop testing or 3D GPU validation.
7. Attempt macOS and Windows application bundles using their respective operating systems. Verify fonts, icons, plugins, WebEngine resources, Qt3D dependencies, file paths, and packaged startup. A Linux build is not proof of a working Mac app.
8. Provide a platform status table: source startup, automated tests, packaged startup, interactive smoke test, installer, and signing/notarization, each with evidence or “not verified.”

Acceptance: the full upstream-derived editor is present and runnable from this repository; its existing features remain accessible; available checks pass or have specific documented blockers; platform support is reported honestly.

If macOS is blocked, investigate the smallest targeted fix. Do not use this as permission to throw away the editor. Report the failing dependency/module, reproducible error, attempted safe fixes, and remaining native test. Ask the owner only for a decision that truly changes scope.

5. Milestone B — imperial precision and practical site setup

Implement feet/inches entry and display throughout coordinates, dimensions, object sizes, spacing, grids, snapping, calibrated images, scale bars, and applicable property dialogs. Support common entries such as 10' 6\", 10 ft 6 in, and decimal feet; define fractional-inch behavior consistently. Display areas in square feet, lengths in feet, and relevant volumes in cubic yards. Preserve metric mode and existing metric projects.

Test round-trip conversions, negative coordinates, fractional inches, large sites, project reopening, unit switching, exported dimensions, and area calculations. Establish accuracy tolerances suitable for landscape planning; conversions must not accumulate geometry drift.

Make site setup a short workflow: project name, units, site image/plan, two-point scale calibration, location, time zone, and true-north orientation. Location/time zone must support daylight-saving transitions without asking a nontechnical user to maintain a UTC offset manually. Prefer an address-assisted optional lookup plus manual latitude/longitude and offline setup. Store location and orientation explicitly.

Provide understandable validation messages and a first-run sample. Do not load private company files or client imagery into a public repository.

Acceptance: a user can import a site plan, calibrate a known 20-foot distance, draw and dimension a 10-foot-6-inch feature, save/reopen it, and export a plan without unit changes or scale errors.

6. Milestone C — complete small landscape design

Prioritize one real workflow: an existing house, property outline, patio, walkway, retaining wall, curved beds, trees/shrubs/perennials, labels, dimensions, quantities, and an exported plan.

Adapt upstream tools for rectangles, polygons, arcs/curves, paths, walls, fences, building footprints and beds. Keep existing object libraries and parametric symbols. Add missing object types only after verifying their absence. Support precise movement, duplication, rotation, numeric size editing, sensible snap behavior, layer visibility/locking, multi-selection, and undo/redo.

Offer useful layer presets: survey/background, existing conditions, demolition, hardscape, planting, dimensions/labels, and sun study. Keep advanced controls available without forcing beginner users through every option.

Reuse plant records and labels. Start with a small clearly sourced editable local catalog, not thousands of invented records. Include botanical/common names, cultivar, container size, spacing, mature dimensions, light requirement, and source/verification status where available. Support favorites, groups/rows, consistent spacing and a counted planting schedule. Company inventory and prices must be imported only from owner-provided authoritative data with permission; do not invent them.

Calculate patio/bed area, path/wall length, plant counts, and material quantities using tested geometry and explicit units. Show waste allowances separately from measured quantities. Do not introduce business pricing or labor assumptions in this milestone.

Acceptance: the sample landscape can be created using real editor tools, modified precisely, reopened, and exported with a consistent object count and quantities. Test a moderately complex site, not just two trees on an empty rectangle.

7. Milestone D — extend the existing sun and shade system

The inspected upstream already includes solar calculation, 2D shadow geometry, shade aggregation, and a 3D viewer. Reuse those systems first. The desired innovation is an easy, trustworthy site-wide study, not merely adding a “sun” checkbox.

Required workflow:

• Location, time zone, date and true-north controls with clear defaults.
• Building, wall, fence, pergola and tree height properties connected to footprint-based shadows where supported or newly implemented.
• Date/time scrubbing and playback with responsive updates.
• Seasonal presets and comparison of morning/noon/evening.
• Daily direct-sunlight hours heatmap with an explicit daylight interval, sampling step, resolution, units, legend and calculation progress.
• Select a point or bed to inspect exposure; compare that result with a plant’s sourced light requirement without presenting it as a guarantee of plant success.
• Export a sun-study view and a concise report of assumptions.

Treat geometric shadowing separately from foliage transparency, weather/clouds, reflected light, terrain and annual radiation. Flat-ground/opaque-footprint calculations must be labeled as such. A 3D directional light is not proof that 3D object shadows work. Terrain-aware ray casting and advanced canopy models belong behind later validation gates.

Validation must include multiple locations, dates and time zones, daylight-saving changes, high/low sun, night, north orientation, known building-height/shadow-length examples, overlapping shadows, and daily integration convergence. Compare solar positions against independent authoritative reference data, not just the existing code’s own expected outputs. Record tolerances and limitations.

Make expensive heatmap work cancellable and avoid blocking the editor. Preserve responsiveness during edits; document recalculation behavior and stale-result indicators.

Acceptance: a building and tree cast directionally correct changing shadows, a daily heatmap includes both occluders, saved site settings reproduce the study, and an exported report identifies exactly which physical effects are modeled.

8. Milestone E — professional workspace and deliverables

Improve the actual Qt editor, not just a marketing page. Use a large central canvas, compact toolbars, collapsible libraries/properties, coherent icons, readable imperial measurements, contextual editing and discoverable keyboard shortcuts. Avoid decorative text and permanently oversized side panels. Offer a beginner workspace and advanced controls without removing upstream capability.

Create a realistic furnished landscape example with a house, paths, hardscape, curved beds, varied plant symbols and dimensions. Provide screenshots from the real application, including selected-object editing and sun-study results. Mockups must be identified as mockups.

Reuse exports; extend them for page sizes, print scale, north arrow, scale bar, title block, legend, plant schedule and optional quantity/sun-study sheets. Test text readability, PDF geometry, margins and exported scale. Distinguish PDF/SVG/DXF support from DWG support; do not promise native DWG unless a separately evaluated compatible implementation exists.

Acceptance: export a legible scaled PDF and plant schedule suitable for a client design discussion. Native app remains useful offline, with working autosave and recovery.

9. Milestone F — Mac and Windows delivery

Produce downloadable versioned application builds, not instructions that require Jace to install Python and execute commands.

Windows: reuse/adapt existing installer tooling, Start Menu shortcut, optional file association, clean uninstall and upgrade behavior. macOS: deliver a tested .app bundle and practical distribution package such as DMG or ZIP, with correct resources and writable user-data locations. Build for confirmed hardware architectures and document minimum supported OS versions based on dependencies and tests.

Provide checksums and corresponding source/notice materials. Validate opening/saving/exporting in the packaged app and a clean-user environment. Signing, Apple notarization and Windows code signing may require owner accounts, certificates and costs: report these as release requirements, never claim they are complete without evidence. Do not instruct users to disable security protections blindly.

Separate automatic build success, packaged launch, interactive functionality, and signed public-release readiness. Label early downloads as test builds.

Acceptance: owner can download, extract/install, launch, edit, save/reopen and export without a development environment. Mac and Windows results must have their own evidence.

10. Longer-term Land F/X-style roadmap

These are planned areas, not features achieved by forking upstream. Track them in a source-grounded gap matrix; prioritize with the owner after the first usable release.

1. Planting documentation: richer schedules, details, symbol libraries, specification fields, batch substitutions and favorites.
2. Hardscape documentation: patterns, materials, hatches, detail libraries, takeoffs and construction sheets.
3. Irrigation: equipment data, zones, heads, coverage, pipe routing, flow/pressure calculations and schedules. Hydraulic design requires manufacturer data and domain validation; do not ship plausible-looking unvalidated engineering calculations.
4. Terrain/grading/drainage: elevations, contours, slopes, cut/fill and terrain-aware shadows. Validate numerical methods before construction use.
5. 3D/presentation: improve the existing viewer, materials and model export before attempting a photorealistic renderer.
6. CAD/interoperability: strengthen DXF workflows and coordinate preservation; separately investigate exchange with AutoCAD/SketchUp. Do not equate a simple DXF export with complete CAD interoperability.
7. Estimating integration: design quantities into company-authoritative catalogs and rates. Keep measured quantities, waste, company cost and selling price distinct. Company rules include no automatic 10% labor increase and daily equipment rates; verify current rules/data before implementation.
8. Business integration: Google Drive, CRM/production handoff and later LMN/Bigin replacement belong to a separate authorized integration phase, not the core design editor.

Never claim complete Land F/X parity without an enumerated, verified capability comparison. This is a multi-milestone engineering program; no single prompt guarantees it is finished in one session.

11. Execution, testing and reporting rules

Work sequentially through milestones. Finish and verify a bounded milestone before moving to the next; continue automatically within authorized scope while feasible, but do not conceal blockers or mark unfinished work complete. Preserve working functionality, use reviewable commits and draft PRs, and never merge or publish production releases without owner direction.

Maintain these project documents using existing equivalents where available:

• MASTER_PLAN.md: this brief and approved changes.
• UPSTREAM_PROVENANCE.md: source lineage and licensing.
• FEATURE_REUSE_MATRIX.md: reused modules, changes and evidence.
• PLATFORM_STATUS.md: Mac/Windows capability and release evidence.
• VALIDATION.md: exact commands, results, fixtures, screenshots and untested behavior.
• ROADMAP.md: milestone statuses, next task and blockers.

Protect project data: safe saves, crash recovery, backward-compatible migration or explicit compatibility boundaries, backups before migration, invalid-file handling, and no silent data loss. Existing .ogp projects are the primary compatibility target. .clp import from the discarded browser prototype is optional later work, not a prerequisite for the desktop foundation.

Run the relevant unit, integration, Qt UI and packaging checks. Report failures rather than deleting tests or relaxing assertions to get green results. Set reasonable test/runtime limits; distinguish skipped checks from passing ones. Keep network-dependent tests separate. Test performance with hundreds of objects and heatmap workloads; record environment and timings instead of inventing benchmarks.

At each handoff tell Jace, in plain language: what he can now do; what actual upstream code was reused; what changed; what was tested on each operating system; what still does not work; how to try it without coding; and the next milestone. Do not substitute extensive planning documents for implemented working software.

12. First Codex task

Execute Milestone A only, then report results and the next implementation task. The immediate deliverable is the actual upstream-derived desktop editor in this repository, with provenance, retained functionality, baseline tests, and honest Mac/Windows status. Do not spend this task rebuilding the editor, styling another browser demo, or claiming unavailable native testing.

If repository writes or CI configuration are blocked, stop at that permission boundary and explain the required authorized next step. If a native test cannot run in the cloud, prepare the reproducible package/check and identify the remaining hardware test rather than pretending it passed.

The product direction is settled: reuse Open Garden Planner, preserve its breadth, make it imperial and cross-platform, then improve the landscape workflow and sun studies.

Reference sources

The prior baseline was inspected locally; Codex must recheck the selected revision before implementation.

• Upstream repository: https://github.com/cofade/open-garden-planner
• Inspected README: https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/README.md
• Dependencies/license declaration: https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/pyproject.toml
• Upstream roadmap: https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/docs/roadmap.md
• Existing browser prototype review: https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/pull/1

Implementation steering received after this plan: prioritize a Windows download. Milestone A retains the desktop editor and metric baseline; Windows x64 test artifacts are immediate, Mac bundles/signing remain later work. No Mac hardware selected.
