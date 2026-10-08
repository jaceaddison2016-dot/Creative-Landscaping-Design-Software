# Open Garden Planner import and foundation assessment

Inspected 2026-10-07/08 UTC for Creative Landscape Studio Milestone A.

| Record | Value |
| --- | --- |
| Upstream | https://github.com/cofade/open-garden-planner |
| Latest observed release | v1.29.5, published 2026-10-07 |
| Release tag commit | `db38aad7ab2e3a653c934613f3dfce962042282e` |
| Selected source commit | `cb4a71db8649cc4e48f85f0bef671bb0ac58dd16` |
| Exact upstream tree | `425ce5a7377dabc4c451092bab60a662a8b57788` |
| Target import commit | `cb188d8deb6376a9be7f508ebeb26db4b2d3e44d` |
| Target parent | original `main`, `3a2a21fb73d1b15c3cddecac901f0176d4a0847c` |
| Upstream declared license | GPL-3.0-or-later; full GPL text retained in `LICENSE` |

The release tag still has 1.29.4 project metadata because upstream CI calculates
the release number before its follow-up version synchronization. The selected
HEAD synchronizes 1.29.5 and issue/context records. Comparing the release to HEAD
showed no editor behavior change beyond the version constant. It is a traceable
released-code baseline, not an invented version number.

## Import method and isolation

Cloned upstream, inspected its instructions, pyproject, packaging, release and
current source, then extracted `git archive` of the selected commit into a new
feature branch based on this repository's original `main`. The import commit's
Git tree was checked for exact equality with upstream **before customization**.
Two upstream-tracked skill files ignored by an upstream case mismatch were
explicitly included to retain that equality. The source snapshot does not import
upstream commit history; the recorded repository/commit identifies that history.

The earlier independent browser prototype remains on
`prototype/landscape-workspace`, draft PR #1. It is not the desktop foundation
and its `.clp` files are not claimed compatible with `.ogp`. No main merge, tag,
or production release was made. All subsequent fork changes are separate commits.

Verification:

```bash
git rev-parse cb188d8^{tree}
# 425ce5a7377dabc4c451092bab60a662a8b57788
git diff --stat cb188d8..HEAD
```

## Suitability

**Use this foundation for the staged prototype.** It already has a full PyQt6
desktop editor, QGraphicsScene/View workspace, CAD tools, species gallery, layers,
command-based undo/redo, image scaling, `.ogp` persistence, autosave, several export
formats, solar geometry, shadow overlays, shade aggregation, and substantial tests.
Replacing it with a new browser canvas would lose working editing infrastructure.

The internal length unit is centimeters; scene +x is east and +y north, with a
view transform to display Y upward. Imperial units should be a centralized
input/display layer later. Preserve `CommandManager` mutations and the existing
project serializer (`FILE_VERSION = "1.4"`), including legacy/additive loading.
The Python package/module name stays `open_garden_planner` to avoid needless
serialization, resource and packaging churn.

## Updating this snapshot safely

1. Create a feature branch from the current fork and preserve local edits. Clone
   upstream into a separate temporary directory; use an ordinary clone, not a Git
   worktree. Fetch tags/history needed to compare the recorded baseline above to
   the proposed new commit. Read the new release notes, AGENTS/skills, dependency
   pins and license/provenance changes before choosing the candidate.
2. Compare the two upstream trees and inspect the behavioral delta. Generate a
   binary patch from **old upstream to new upstream**, rather than copying a new
   snapshot over the customized fork. Apply with Git's three-way support on the
   feature branch and resolve conflicts deliberately. Handle the upstream README
   separately in `docs/upstream/README.md`; retain this fork's root README. Preserve
   fork workflows, release repository restriction, notices and owner plan records.
3. Use the original import commit plus fork commit history to distinguish inherited
   changes from customization. Review command/serialization/unit/security changes
   and resource additions carefully. Re-read new agent instructions and keep both
   context libraries synchronized. Do not invent compatibility or change Qt/Qt3D
   micro pins independently to bypass a failed import.
4. Record the new upstream URL/tag/SHA/tree, comparison range, selected rationale
   and update commit in this document. Refresh the constraints and third-party
   inventory against an actual installation; preserve new data/asset attribution.
   Review any dependency licensing or source-distribution changes before shipping.
5. Repeat full pytest, lint, security, context/citation/secret gates, real source
   smoke, and native packaged subsystem/startup/save/export checks. Regenerate
   source/binding archives and verify download integrity at the new build commit.
   Mac source probes do not replace Mac package QA. Obtain independent senior
   review and keep the update PR draft until owner manual testing passes.

No direct snapshot replacement, automatic upstream merge, manual tag, production
release or reset of owner work is part of this update procedure. Source snapshots
share blob/tree identity with upstream but do not supply upstream merge ancestry.

This is a precision garden editor, not a validated replacement for professional
Land F/X workflows. The large application/controller surface, fast upstream
changes, Qt3D/runtime ABI pins, dynamic frozen MCP dependencies, optional online
providers, and GPU-dependent 3D rendering need continued maintenance. The full
editor remains accessible in A; a landscape-focused interface is a later change.

## Platforms and legal obligations

Upstream explicitly classifies Windows, and its native release recipe is
PyInstaller plus NSIS on Windows. Linux is the supported headless development/CI
path. There was no inspected upstream Mac installer or universal-binary recipe.
Native Mac dependency probes are separate evidence, not proof of packaged UI.
See `PLATFORM_STATUS.md` for this fork's measured results.

GPL and dependency license obligations apply to the redistributed desktop code.
The import retains copyright/license notices, asset provenance, Tabler's MIT
notice, and CC BY-SA data metadata. Windows downloads carry source, notices and
dependency inventory. See `THIRD_PARTY_NOTICES.md`; no proprietary ownership or
exclusive asset rights are claimed. No Land F/X code, assets or affiliation.

The inherited automation server binds loopback only. Reads and file-producing
exports/save are available to local clients by default; scene editing requires
the preference **and** a configured token. Main-thread bridging and network
guards remain untouched. Ordinary local editing needs no account or API keys.
Optional provider lookup/weather/map behavior is not verified here.

## Creative visual-preview customization

The `feature/creative-design-preview` branch starts at desktop-foundation
`439e486414070161d9fea58a6123644e8d0afdc3`. It adds an opt-in Qt editor/welcome
experiment and a shared theme override seam, without changing the source import,
license notices, dependencies, package identifiers, schema or internal units.
Company assets remain placeholders. See BRAND_DESIGN_SYSTEM.md and
docs/design/VALIDATION.md for scope/evidence; this branch is not a new installer.
