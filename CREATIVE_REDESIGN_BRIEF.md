Creative Landscape Studio — master redesign prompt

Your assignment

Redesign the existing Open Garden Planner-derived Python/PyQt6 desktop application in this repository so it feels like Creative Landscaping & Design’s own professional landscape-design studio. Implement the redesign in the real application, not a separate website, browser demo, or static mockup presented as working software.

Read MASTER_PLAN.md, applicable AGENTS.md instructions, provenance, platform status and the existing UI architecture first. Work from the latest desktop-foundation branch, not the abandoned browser prototype. Preserve unrelated work and all existing functionality. This brief supplements the master plan; it does not cancel platform, imperial-unit, licensing or validation requirements.

The intended feeling is established, precise, calm, refined and grounded in southwest Michigan outdoor living. Think professional landscape architecture and beautifully built outdoor spaces—not a cartoon gardening app, a generic green startup dashboard, or a flashy marketing website.

Reference: https://www.creativelandscapinginc.com/portfolio

Brand evidence versus design proposals

The previously inspected company logo has a circular tree emblem and serif lettering. A website testimonial graphic uses navy text, muted gold stars and pale gray-blue backgrounds. These are useful visual references, not proof of the company’s exact official palette or typefaces. Verify website styles and owner-supplied brand files if available. Label extracted colors, verified specifications and proposed adaptations separately.

Use the proposed palette below as the starting design direction unless verified company specifications supersede it. Do not describe these exact hex values as official Creative brand colors.

Proposed color system

|Token          |Color  |Role                                                                               |
|---------------|-------|-----------------------------------------------------------------------------------|
|Creative Navy  |#123B63|Primary identity, active tools, primary actions, selected tab text                 |
|Deep Navy      |#102B46|Dark header, prominent brand surfaces                                              |
|Heritage Gold  |#B79A4C|Restrained highlights, sun-study accents, decorative rules; not small text on white|
|Warm Ivory     |#F7F6F1|Welcome screen and light application background                                    |
|Panel White    |#FFFFFF|Properties, library panels, dialogs                                                |
|Slate Ink      |#263441|Main text and numeric values                                                       |
|Muted Slate    |#596875|Secondary text and descriptive labels                                              |
|Limestone      |#D8DDD9|Quiet dividers and supporting surfaces, not sole control boundaries                |
|Control Outline|#71808B|Visible input/control outlines where needed; validate contrast                     |
|Lake Mist      |#E7EEF3|Hover and selected-row background with navy text                                   |
|Landscape Green|#42644C|Secondary natural accent, plant-related indicators and success states              |
|Error Red      |#A33131|Destructive/error status with icon and plain-language explanation                  |

Navy is the principal identity color. Gold is sparse. Green supports planting content; it must not dominate everything just because this is landscaping software. Avoid gradients on controls, excessive shadows, neon accents and glossy effects.

Keep the drawing surface neutral and independently configurable. Branding must never obscure grid lines, imported site images, plant symbols, dimensions, layers or selected geometry. Reserve canvas selection/focus colors for unambiguous interaction; never use the same treatment for selection and a purely decorative brand accent.

Create centralized semantic theme tokens rather than scattering literals across widgets. Support existing light/dark modes consistently. Define a genuine dark palette with tested contrasts; do not merely invert images or apply a dark background to unchanged widgets.

Typography

Retain the actual company logo artwork; do not approximate its wordmark by typing the company name in a vaguely similar font.

Proposed font pairing, not identified official website fonts:

• Source Serif 4, semibold: welcome-screen title, a small number of brand headings, and optional presentation/title-block headings.
• Source Sans 3, regular/semibold: menus, toolbars, panels, buttons, lists, dialogs, property fields, notifications and help.
• Use aligned/tabular numerals where supported for measurement columns and quantity tables. A separate monospace font is optional for coordinate readouts, not for the whole application.

Use dependable system fallbacks when fonts are unavailable. Source Serif 4 may fall back to Georgia or an available serif; Source Sans 3 may fall back to Segoe UI on Windows, the platform system sans-serif on Mac, or another tested sans-serif. Check availability and redistribution rights, retain font notices, bundle approved fonts locally if appropriate, and load them through the application’s existing resource/font mechanisms. Do not require an online font download at startup.

Default control text should be comfortably readable, approximately 13–14 logical pixels at normal scaling, with a compact density option. Use approximately 16–18 for panel headings and 28–34 for the welcome title. Treat these as starting sizes, test at OS scaling settings, and do not reduce text to tiny sizes to squeeze in features. Prefer sentence case, restrained weights and minimal letter spacing. Serif fonts do not belong in dimension fields, menus or dense tables.

Layout and interaction

Welcome and project opening

Create a useful Creative-branded start screen with New project, Open project and recent projects as primary actions. Show project thumbnails, names, last-edited information and recovery options where implemented. Include a restrained company photograph only when redistribution permission is confirmed. Without approved photography, use neutral placeholders—not invented photos labeled as company projects.

Offer project templates that connect to actual editor data. Proposed categories include Residential landscape, Patio & outdoor living, Planting renovation and Waterfront landscape. Do not display nonfunctional template buttons; label unavailable options clearly or omit them until implemented.

Main editor

The canvas is the main event. At a typical desktop size, aim for roughly 65–75% of horizontal space for drawing where practical, with collapsible docks rather than rigid oversized panels.

• Compact top bar: modest logo/identity, project name, save state, common file actions and view controls. Retain discoverable full menus.
• Clearly grouped tools: Select/Edit, Site & structures, Hardscape, Planting, Dimensions/labels, Sun study and Export. Map groups to actual existing commands; adding a category does not authorize pretending a new feature exists.
• Left dock: searchable object/plant library and layers, with sensible tabs and density.
• Right dock: contextual properties for the selection, with dimensions and essential fields first and advanced properties expandable.
• Bottom status bar: current tool guidance, coordinates, snap state, units, zoom and background task status where supported.
• Remember dock visibility, widths and workspace preferences. Provide Reset workspace and Focus canvas actions.

Use a single coherent icon family compatible with the existing icon license. Avoid emoji and unrelated decorative symbols. Every unfamiliar icon needs an understandable tooltip; primary tool groups should have text labels. Preserve shortcuts and provide visible active, hover, disabled and keyboard-focus states.

Libraries and properties

Present plants with useful names and compact previews, rather than enormous decorative cards. Maintain existing metadata and online/offline behavior. Keep layer visibility and locking easy to operate. Show selection count and compatible common properties for multiple objects where supported. Avoid moving frequent actions behind unnecessary extra clicks.

Sun-study workspace

Make the existing sun/shade functionality discoverable through a focused workspace: location/time zone, date, time scrubber, play/pause if implemented, seasonal presets if implemented, shadow display and heatmap controls. Use gold sparingly for sun-related indicators. Keep the active model assumptions visible in concise language. Clearly distinguish direct geometric sunlight from weather-adjusted exposure or advanced 3D radiation modeling.

Do not promise continuous animation or new calculations through UI styling alone. Wire controls to the actual upstream systems; add missing behavior with tests or label it as deferred. Keep heavy calculations cancellable and show stale-result/progress states.

Dialogs and feedback

Apply the design system to preferences, file-related dialogs under application control, plant editing, layer editing, export, warnings, progress, About and recovery screens. Respect native OS file dialogs instead of replacing them solely for visual uniformity.

Use short, task-specific instructions. Distinguish save success, unsaved changes, errors and unfinished computation. Do not show marketing copy such as “A little shade, a little color” inside a professional editing panel. No fake success notifications or hidden data-loss warnings.

Client outputs

Provide optional Creative-branded PDF/title-block styling with the approved logo, project title, date, revision, designer, scale and north indicator where existing export architecture supports them. Keep graphic identity separate from measured scale. Printed output must remain legible in grayscale and preserve vector geometry where appropriate. Do not stamp company identity over the drawing or add decorative imagery to construction sheets.

Asset, license and implementation boundaries

The repository is public. Do not automatically scrape and commit company portfolio photos, client information, partner logos or restricted fonts. Website visibility is not redistribution permission. Request approved asset files or use placeholders and an asset inventory listing approval status. Never add third-party vendor logos merely because the website displays them.

Preserve Open Garden Planner’s copyright, GPL notices, dependency notices and attribution. User-facing Creative branding is allowed only with company authorization; it does not erase upstream authorship. Keep package/module identifiers unchanged unless a tested migration is actually needed. No Land F/X branding or proprietary assets.

Use Qt palettes, targeted styles, resources and existing widgets/components. Avoid one enormous global stylesheet with broad selectors that break native controls, graphics items, dialogs or accessibility. Reuse existing theme infrastructure where present. Separate visual changes from unit, domain and serialization changes. No framework rewrite.

Execution order and approval gate

1. Audit current UI/theme modules and capture genuine before screenshots. Record functionality and shortcuts that must remain intact.
2. Create a reusable token/font/component system and an asset-approval inventory.
3. Produce two representative previews: the real main editor with a credible populated plan, and the proposed welcome screen. Explain which elements are actual running Qt UI and which are design-only previews.
4. Pause for owner approval of the visual direction before applying a broad application-wide redesign. Targeted experimental work may remain on the feature branch; do not publish a new installer or merge while awaiting approval.
5. After approval, apply the system to the real editor and dialogs in reviewable increments. Preserve a fallback to the existing theme until visual regression testing passes.
6. Update export styling and application branding where authorized. Rebuild native test packages only after relevant tests pass and under the repository’s existing release controls.

If approved source branding is missing, show a clearly identified text placeholder rather than inventing an official logo. Do not let optional photography block work on layout and component quality.

Quality gates

• Before/after screenshots at common desktop sizes; inspect narrow layouts and 100%, 150% and 200% scaling where environments allow.
• Keyboard navigation, clear focus, readable disabled controls, tooltips and accessible names. Aim for WCAG AA-style contrast targets: 4.5:1 for ordinary text, 3:1 for large text and essential non-text controls. Calculate relevant pairings rather than asserting compliance from appearance.
• Light/dark coverage of menus, docks, popups, tables, inputs, sliders, date/time controls, progress and warnings.
• Regression checks for drawing, selection, dragging, snapping, numeric editing, undo/redo, layers, save/reopen, autosave/recovery, sun/shade controls and exports.
• No private assets leaked, no attribution removed, no project-format changes caused by styling.
• Verify packaged fonts/icons on Windows and Mac when packages exist. Cloud screenshots do not prove native font rendering or GPU behavior.

Deliver BRAND_DESIGN_SYSTEM.md, approved assets or documented placeholders, implementation source changes, genuine before/after screenshots, tests/results and a draft PR. Report visual changes separately from new functionality and unverified platform behavior.

First task

Begin with the audit, design tokens and the two representative previews. Save this brief as CREATIVE_REDESIGN_BRIEF.md in the project. Ask for visual approval at the stated gate, not a sequence of technical design questions the owner cannot reasonably answer.

The goal is immediately recognizable Creative identity and a substantially more usable professional workspace, while retaining the full upstream-derived application underneath.