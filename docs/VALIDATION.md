# Validation record

Executed October 7, 2026 in the Linux cloud environment. Node.js v24.19.0, npm 11.9.0, Playwright 1.61.1, system Chromium 151.0.7922.173. This record applies to the first prototype in this pull request.

## Completed

| Check                                                                        | Result                                                                         |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `npm ci --cache /tmp/creative-npm-cache --no-audit --no-fund`                | Passed using committed lockfile; repeated installation completed               |
| `npm run check`                                                              | JavaScript syntax checks passed; **12 unit tests passed, 0 failed, 0 skipped** |
| `npm run format:check`                                                       | Passed                                                                         |
| `TEST_HTTP_ONLY=1 BROWSER_EXECUTABLE=/usr/bin/chromium npm run test:browser` | Passed all nine functional groups; no browser page errors                      |
| `git diff --check`                                                           | Passed                                                                         |

The browser workflow exercised:

1. Example plan rendering and all ten shadow polygons.
2. Plant placement, imperial name/diameter/height editing, dragging, undo, redo.
3. Two-point dimensions with an independently expected 40-foot result and selection.
4. Changing date/time changes shadows; midnight hides them; shadow toggle works.
5. A real `.clp` download, JSON validation, and reload preserving plants, sizes, dimensions, site, and project name.
6. Invalid JSON and a resize placing plants outside the plot reject the change and preserve the existing plan.
7. Deletion, undo, and confirmation/cancellation when replacing unsaved work.
8. Imported plant names stay text, with no injected HTML; 390-pixel viewport has no horizontal document overflow.
9. The documented Node development server starts and serves the functional application.

Unit checks additionally cover feet/inches parsing and exact round-trips, diagonal measurement geometry, version/schema/coordinate validation, duplicate IDs, file/object limits, calendar dates, leap days, fractional UTC offsets and date boundaries, seasons, polar day/night, southern-hemisphere sunlight, east/west sun direction, and shadow orientation/length.

The solar engine was compared against the published **NREL SPA example** (2003-10-17 12:30:30 UTC−7, latitude 39.742476°, longitude −105.1786°). The prototype gave elevation 40.09787° and azimuth 194.47719°, compared with 39.88838° and 194.34024° in that example. Both meet the 0.5° test tolerance. This validates one reference case and physical expectations, **not a universal accuracy guarantee** for all locations/dates. The prototype uses a simpler NOAA fractional-year approximation, not the full SPA algorithm.

A screenshot captured from the passing browser run is included in [the README](../README.md). Browser-generated fixtures/screenshots under `test-results/` are ignored.

## Could not test here

- **Direct-file launch:** the cloud's managed Chromium returns `ERR_BLOCKED_BY_ADMINISTRATOR` for `file://` navigation. Its enforced URL policy was left in place. The complete functional suite ran over the loopback HTTP server; the `TEST_HTTP_ONLY` flag explicitly marks direct-file launch unrun. No claim that the file route passed is made.
- **Actual macOS and Windows:** only Linux was available. File association, extraction, downloads, keyboard/platform conventions, system font rendering, and desktop browser policies require native checks.
- **Safari, Firefox, and Edge:** not available for this run. Chromium does not prove compatibility with those browsers.
- **GitHub Actions:** the workflow includes Ubuntu, Windows, and macOS jobs, but defining a workflow does not establish a CI pass. Check the actual runs once the branch/PR is available.
- **Native installers:** none are implemented or tested. This is a desktop browser application.
- **Open Garden Planner runtime/tests:** source and licensing were evaluated; the upstream application and test suite were not run.

## Beginner manual check on both target platforms

1. Download the branch ZIP, extract it, and double-click `index.html`. Confirm the example plants and their shadows appear.
2. Make a new plan. Add one plant from each palette choice. Select and move one; set height to `10' 6"` and canopy diameter to `5`.
3. Draw a dimension across the plot, change plot size, undo/redo, and try deleting/recovering a plant.
4. Set your location and UTC offset for a summer date. Compare 9 AM, noon, and 4 PM; shadows should change direction and length. Compare winter. Set midnight and confirm shadows disappear. Remember to change the offset if daylight saving changes.
5. Save, locate the `.clp` download, close the tab, reopen `index.html`, and use **Open** to load the file. Confirm dimensions, plants, and site/date/time settings are restored.
6. Check the same sequence in your intended browser. Record OS/browser versions and any failures before describing that platform as verified.
