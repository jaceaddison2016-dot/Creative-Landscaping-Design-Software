# First landscape planning prototype

The repository previously contained only a README. This adds an independent desktop-browser prototype with an editable 2D SVG plan, generic plant placement and size/height editing, dimensions in feet and inches, versioned `.clp` project save/load, undo/redo, and location/date/time-based approximate ground shadows.

Open Garden Planner was evaluated at version 1.29.5 before implementation. Its GPL-3.0-or-later Python/Qt application has Windows release packaging; equivalent macOS distribution was not established. The small independent implementation avoids importing upstream code/assets. The assessment and development dependency license notices are included.

## Try it without coding

1. Select branch **prototype/landscape-workspace**, then **Code → Download ZIP**.
2. Extract the ZIP and double-click **index.html**. Keep the four application files together.
3. Try the example or click **New plan**. Pick a plant, click the plan, select/edit it, and draw a dimension.
4. Expand **Site location & time zone**, set your location and UTC offset for the date, and change the date/time to explore shadows.
5. Click **Save project**, keep the downloaded `.clp` file, then use **Open** to reload it.

README includes screenshots, detailed instructions, and a server fallback if local HTML is blocked.

## Validation and limits

- Repeated locked install, syntax checks, formatting, and 12 unit tests passed.
- Linux Chromium passed nine functional browser groups covering placement/editing, dragging, dimensions, undo/redo, seasonal/night shadows, actual downloads and reloads, invalid files, replacement protection, and responsive rendering.
- Solar position meets a 0.5° tolerance against one published NREL reference example, plus seasonal/directional checks. It remains an approximate flat-ground study with solid plant footprints.
- Direct-file testing was blocked by cloud browser policy. Actual macOS/Windows execution, Safari/Firefox/Edge, native downloads/file associations, and the newly configured CI matrix remain unverified. No native installers are included.
- No autosave, species database, beds/structures, CAD integration, or Land F/X feature parity. No project-wide redistribution license has been selected for the original code.

See docs/VALIDATION.md and docs/FOUNDATION-EVALUATION.md for evidence and manual checks. This is a draft for first-prototype review.
