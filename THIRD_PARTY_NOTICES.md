# Third-party notices

The browser application (`index.html`, `styles.css`, `core.js`, `app.js`) contains original prototype code and browser-native APIs. It loads no third-party runtime libraries, fonts, plant artwork, or remote services. No Open Garden Planner source, assets, or data are included.

Development dependencies are installed by `npm ci` using the committed lockfile:

| Package                                                    | License    | Preserved notices                                                                                                                                                                                                                                                 |
| ---------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Playwright / playwright-core 1.61.1, Microsoft Corporation | Apache-2.0 | [License](docs/licenses/playwright-LICENSE.txt), [NOTICE](docs/licenses/playwright-NOTICE.txt), [Playwright third-party notices](docs/licenses/playwright-ThirdPartyNotices.txt), [core third-party notices](docs/licenses/playwright-core-ThirdPartyNotices.txt) |
| Prettier 3.8.3, James Long and contributors                | MIT        | [License and copyright](docs/licenses/prettier-LICENSE.txt)                                                                                                                                                                                                       |

The optional macOS development dependency fsevents 2.3.2 carries the MIT license, copyright Philipp Dunkel, Ben Noordhuis, Elan Shankar, and Paul Miller. Its [license and copyright](docs/licenses/fsevents-LICENSE.txt) are preserved.

The individual bundled dependency license sidecars from Playwright and playwright-core are preserved verbatim in [docs/licenses/playwright-bundles/](docs/licenses/playwright-bundles/). Package installation also retains the originals under `node_modules`; these tools are not bundled into the browser application.

Browser binaries installed for tests are separate third-party software and carry their own notices. This repository does not redistribute those binaries.

The solar formulas were implemented from NOAA's [General Solar Position Calculations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF), with an independent accuracy test against the [NREL Solar Position Algorithm report](https://www.nrel.gov/docs/fy08osti/34302.pdf). Mathematical sources are credited here and in the code/tests. This does not imply NOAA or NREL endorses the application.

Open Garden Planner's licensing and reuse implications are documented in [the foundation evaluation](docs/FOUNDATION-EVALUATION.md). Its GPL notices would be required if its code or assets are incorporated in a future version. No repository-wide redistribution license has been selected for this original prototype.
