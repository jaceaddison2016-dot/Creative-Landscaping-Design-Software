# Open Garden Planner foundation evaluation

Evaluated on October 7, 2026, before implementing this prototype. The actual upstream checkout was inspected read-only at commit [`cb4a71db8649cc4e48f85f0bef671bb0ac58dd16`](https://github.com/cofade/open-garden-planner/tree/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16), reporting version **1.29.5**. Conclusions apply to this revision, not every future release.

## What is there today?

[Open Garden Planner](https://github.com/cofade/open-garden-planner) is a substantial desktop application, not a small starter kit. Its README and implementation describe a metric, CAD-oriented garden planner with plant metadata, layers, snapping, image calibration, JSON `.ogp` project files, export, garden management, and a newer 3D/solar feature set.

Inspected sources:

- [README](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/README.md): functionality, source installation, Windows distribution.
- [pyproject.toml](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/pyproject.toml): Python ≥3.11, PyQt6, Qt WebEngine/Qt3D, NumPy, Pillow, pyclipper, DXF/MCP dependencies, GPL-3.0-or-later metadata. Four Qt runtime/binding packages are pinned together to address a documented binary mismatch.
- [Solution strategy](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/docs/04-solution-strategy/README.md): QGraphicsView canvas, PyInstaller/NSIS packaging.
- [Solar engine](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/src/open_garden_planner/core/solar.py) and [shadow geometry](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/src/open_garden_planner/core/shadow_geometry.py): timezone-aware NOAA solar calculations, geometric elevation, footprint extrusion and clipping in centimeters. These are useful architectural reference points; none of their code was copied or translated into this prototype.
- [CI](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/.github/workflows/ci.yml) and [release workflow](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/.github/workflows/release.yml): Linux offscreen testing and Windows release packaging. Presence of tests is not evidence that those tests were run in this evaluation.

## Platforms

| Platform | Evidence in inspected revision                                                                 | Implication                                                                                                                                            |
| -------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Windows  | Windows 10+ x64 installer documented; `windows-latest` release job; Windows packaging metadata | Strongest supported distribution path; installer not installed or tested here                                                                          |
| macOS    | README source-install activation example includes Linux/Mac; Python/Qt are generally portable  | Potential source execution, but no macOS installer/release job or equivalent validation found in inspected workflows; compatibility is not established |
| Linux    | Ubuntu CI with Qt offscreen test execution                                                     | Useful development/test support; not equivalent to testing macOS or Windows                                                                            |

A fork would inherit extensive functionality, but also its metric-centric interaction model, dependency and packaging surface, and ongoing maintenance burden. Imperial entry/display and macOS packaging would require dedicated investigation, changes, and native testing. A fork is viable if the long-term product intentionally adopts GPL and the Qt architecture; it is not the smallest route to this requested prototype.

## Licensing

The upstream package metadata declares **GPL-3.0-or-later**; its repository includes the full [GPLv3 license](https://github.com/cofade/open-garden-planner/blob/cb4a71db8649cc4e48f85f0bef671bb0ac58dd16/LICENSE). Redistribution of a modified/derived application would require preserving copyright/license notices, marking modifications, complying with GPL source-delivery obligations, and licensing the covered combined work consistently with the GPL. Bundled Qt, Python packages, fonts, data, and other assets would need their own notice/license review too. Merely changing branding would not remove those obligations.

The upstream code, assets, datasets, and license file are **not bundled** in this prototype. Therefore this prototype does not claim to be an Open Garden Planner fork and does not relabel any GPL code. The solar implementation uses the separately published NOAA mathematical specification, not the upstream implementation. [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) preserves notices for the development dependencies actually used. No project-wide redistribution license was selected on the repository owner's behalf; that is a decision for a later public release.

## Decision for version 0.1

Implement a small, independent HTML/CSS/JavaScript application with SVG rendering and a versioned JSON file format. It requires no runtime packages, accounts, plant API credentials, or build step. Modern browsers on macOS and Windows are the target delivery route. This is a browser prototype, **not a native desktop installer**.

Keep calculations and file validation separate from UI code so a future desktop wrapper or more advanced workspace can reuse them. Use whole inches as the canonical length unit; include latitude, longitude, date, local time, and explicit UTC offset in saved projects. Native installers, `.ogp` import, real plant databases, beds/buildings, terrain, 3D, irrigation, estimating, CAD integration, and Land F/X parity are outside this first version.

This was source and documentation evaluation, not an upstream runtime audit. Open Garden Planner was not installed and its test suite was not executed. No claims of upstream runtime correctness or macOS compatibility are made.
