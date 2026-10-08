# Validation evidence — Milestone A

Baseline: upstream cb4a71db8649cc4e48f85f0bef671bb0ac58dd16, version 1.29.5.
Runtime source and resources remain unchanged. Operational scripts/workflows and
two hermetic test corrections are separate fork changes. See provenance and
platform records for scope and limits.

## Linux cloud evidence

Python 3.12.14; PyQt6, Qt6, PyQt6-3D and Qt3D all 6.11.0.
Supported editable install plus PyInstaller succeeded and repeated installation
with recorded constraints passed. `uv pip check` reports all 71 installed packages
compatible. Installation is not a GPU guarantee.

| Check | Result |
| --- | --- |
| Actual source self-test | Pass: six Qt3D imports, matching runtime version, real loopback API server |
| Normal app process | Pass: 8-second startup, fixture summary, rendered PNG, PDF/DXF/CSV, .ogp save and second-process reopen |
| Output checks | PNG/PDF signatures; DXF geometry via ezdxf; CSV header; saved/reloaded object counts |
| Ruff src/tests/scripts | Baseline pass; final check before PR |
| Bandit HIGH severity | Baseline pass, zero HIGH results; final check before PR |
| Context parity / tracked secret scan | Pass; final check before PR |
| Notice/source collector | Pass: 70 dependency metadata/notice sets and all four exact PyQt/sip source archives with verified PyPI SHA-256 |
| First full suite | 7,586 passed, 36 skipped, 4 failed, 42 warnings; 7,626 collected; 743.07 seconds |

First-run failures were investigated, not suppressed:

- Two frozen command inventory failures came from new documentation/workflow command
  copies. Docs now cite ogp-change-control section 2.8; a reusable PowerShell helper
  executes the subsystem check for both bundles. The unchanged gate tests pass 54/54.
- A Windows detection test mocked sys.platform on Linux, causing Python 3.12's real
  shutil.which to call absent _winapi. It now isolates executable discovery and
  home paths, as neighboring tests do. Configuration assertions remain intact.
- The fallback-path test created directories in the actual read-only cloud home.
  It now patches Path.home to pytest's temporary directory and also verifies
  directory creation. Production path behavior and assertions were not removed.

The two corrected test files pass 56/56. A fresh full suite is required after these
changes and will be recorded before completing the draft PR. Earlier redirection
failures did not execute tests and are not suite runs. Logs/XML are in ignored
build/milestone-a; persistent CI evidence is linked in the PR.

All 36 headless skips are retained, including GPU/3D-dependent cases; exact reasons
are in JUnit. The 42 warnings concern inherited deprecated MCP client transport
names. No UI strings, translations, engine code or .ogp schema changed.

## Native evidence

The Windows workflow builds the actual PyInstaller executable and NSIS installer.
It runs inherited drawing, selection, resize, undo, layers, item round-trips,
species, sun/shadow, autosave and export tests. The subsystem helper waits for the
GUI child and rejects nonzero exits without console pipes. Real portable and
installed processes must render/save/export/reopen before upload. A PID or open
port alone cannot pass. The download carries evidence and exact source/build records.
Windows final installer results remain pending until CI finishes.

Native Intel and Apple Silicon Mac dependency installs and source self-tests passed
in run 37706636013 without changing Qt pins. Mac package/manual QA is deferred by
the owner's Windows-first steering. There is no verified Mac download.

## Limits and review

Use docs/WINDOWS_DOWNLOAD.md for the owner checklist. Human interaction, screen
scaling/fonts, printing, real-site solar accuracy, GPU 3D, WebEngine maps, upgrades/
uninstall, antivirus acceptance, signing and Mac packaging are not verified.
Optional credentials were not needed for ordinary editing or included in artifacts.

Inherited instructions request Context7, but no Context7 tool is available here.
Installed source/metadata and upstream build instructions provided the evidence.
Independent senior review is required before opening the draft PR; the PR remains
draft/unmerged until the owner confirms manual testing. This does not complete B–F.
