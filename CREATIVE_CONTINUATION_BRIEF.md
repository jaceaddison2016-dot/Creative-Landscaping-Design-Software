Continue improving the actual Creative Landscape Studio desktop application. Read MASTER_PLAN.md, CREATIVE_REDESIGN_BRIEF.md, applicable repository instructions, and the current PR #3 changes first. Preserve the Open Garden Planner foundation, existing functionality, project compatibility, licensing, and unrelated work.

I approve the navy/ivory/gold color direction, but the current layout needs another pass. This is approval to implement the improvements below—not approval to merge or publish a production release.

1. Simplify the editor layout

Reduce the stacked toolbar rows. Organize frequent actions into compact, labeled groups: Select/Edit, Site & Structures, Hardscape, Planting, Dimensions, Sun Study, and Export.

Keep advanced tools accessible through menus or expandable groups; do not remove functionality. Show sun-study controls when that workspace is active rather than permanently consuming drawing space.

Make the drawing canvas dominant. Narrow the properties dock, make both side docks collapsible and resizable, and remember workspace preferences. Group properties into Essentials, Appearance, and Advanced. Keep names, dimensions, positions, and layer assignment easy to find.

2. Make the application landscape-first

Prioritize landscape design over gardening administration. Move Planting Calendar, Seed Inventory, Harvest, and similar tools into an optional Gardening workspace or menu without deleting them.

Use familiar landscape terminology and coherent icons with tooltips. Preserve keyboard shortcuts, clear selection states, and undo/redo behavior.

3. Strengthen Creative’s identity

Retain the approved color direction and proposed typography from the redesign brief. Use readable sans-serif fonts for controls and measurements; reserve serif typography for brand headings.

Replace the identity placeholder only when an approved company logo is available. Do not invent an official logo or commit website photographs, client data, or restricted assets without permission.

Improve the welcome screen with balanced spacing, prominent New/Open actions, compact recent-project cards, and useful thumbnails. Avoid a huge empty list box. Only include templates that actually work.

4. Improve the drawing’s presentation

Offer a clean architectural-symbol style for plants alongside the existing detailed symbols. Make material textures subtler and independently adjustable. Preserve object geometry, metadata, exports, and existing symbol options.

Use a credible sample landscape with a house, patio, walkway, curved planting beds, varied plants, dimensions, and shadows. It must be editable project data, not a flattened illustration.

5. Implement feet and inches before calling this usable for Creative

Complete the imperial-unit work in the actual desktop application—not the abandoned browser demo.

Cover drawing input, coordinates, dimensions, rulers, grids, snapping, object sizes, property fields, calibration, scale bars, relevant reports, and exports. Display areas in square feet and relevant volumes in cubic yards.

Make imperial the default for new Creative projects while retaining metric mode. Preserve existing centimeter-based internal geometry and metric-project compatibility.

Support feet/inches and decimal feet with explicit, consistent input rules. Test fractional inches, negative coordinates, unit switching, save/reopen, exported measurements, and conversion drift. Clearly disclose any remaining metric-only surfaces.

6. Resolve the testing/performance blocker

Investigate the reported full-suite slowdown and retained Qt widgets. Determine whether the cause is test cleanup, widget ownership, repeated styling, or production behavior. Record evidence and fix the actual cause.

Do not delete tests, suppress failures, or simply increase timeouts to claim success. Run focused checks first, then the full relevant suite. Report passed, failed, skipped, and interrupted checks separately.

Protect drawing, editing, snapping, undo/redo, layers, persistence, autosave, sun/shade functionality, and exports with regression checks.

7. Show real results before packaging

Provide actual screenshots of the revised running desktop application: welcome screen, populated editor, imperial properties/dimensions, and sun-study workspace. Include light/dark and smaller-screen checks.

Clearly identify remaining placeholders and unimplemented features. Ask me to approve the revised visual direction before broadening the redesign further.

8. Deliver an updated test download after approval and validation

After visual approval and successful validation, create a new Windows test installer containing these exact changes. Verify packaged startup, fonts/icons, drawing, imperial input, save/reopen, and exports on a Windows runner.

Keep macOS support in scope. Report its packaging status separately; do not describe source imports as a working Mac installer.

Commit and push the changes to the appropriate development branch and update the draft PR. Do not merge or create a production release.

At handoff, provide:

* Branch, commit SHA, and PR link.
* Genuine before/after screenshots.
* Test results and unresolved limitations.
* A direct test-download link, if a new build exists.
* The commit used to build that download.
* Simple installation instructions requiring no coding.

Work in reviewable stages. If a stage is blocked, explain the specific blocker instead of claiming completion. The goal is a cleaner, genuinely Creative-branded landscape-design tool with feet/inches—not merely a recolored preview.