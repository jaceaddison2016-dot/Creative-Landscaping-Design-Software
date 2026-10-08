# Platform status — Milestone A

Evidence as of 2026-10-08 UTC. Windows x64 is the immediate download target by owner
direction. No Mac was selected. Automated results are scoped to their runners;
manual use, signing, and supported OS versions require separate QA.

| Capability | Linux cloud | Windows x64 | macOS Apple Silicon | macOS Intel |
| --- | --- | --- | --- | --- |
| Supported dependency install | Pass: Python 3.12.14, matched Qt/Qt3D 6.11.0 | Pass native CI | Pass native macos-14 | Pass native macos-15-intel |
| Qt3D/runtime/API self-test | Pass source | Pass frozen | Pass source | Pass source |
| Inherited automated tests | Full suite rerun pending; see VALIDATION | Selected editor tests pass | Not run beyond self-test | Not run beyond self-test |
| Normal editor/save/export | Pass offscreen actual process | Pass portable actual process | Not verified | Not verified |
| Application package | Not a delivery target | PyInstaller pass; NSIS running | Deferred by Windows-first direction | Deferred by Windows-first direction |
| Packaged startup/resources/exports | Not verified | Pass portable; installed check pending | Not verified | Not verified |
| Installer execution | Not applicable | Pending | Not verified | Not verified |
| Human mouse/keyboard smoke | Not verified | Owner test pending | Not verified | Not verified |
| GPU 3D rendering | Not verified; offscreen skips | Not verified | Not verified | Not verified |
| Code signing / notarization | Not applicable | Unsigned | Not verified | Not verified |

[Mac probe run 37706636013](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37706636013)
installed inherited dependencies and passed the actual source self-test on both
architectures without altering Qt pins. This establishes import/loopback viability,
not a verified .app, DMG, universal binary or interactive editor. No workaround was
needed for these probes. Mac packaging remains required before promising a download;
it is deferred following the owner's Windows request.

Windows packaging uses the inherited spec and NSIS recipe. The workflow tests
the extracted bundle and a silently installed copy, preserves notices/source,
and uploads an artifact only after these pass. Windows ARM, older OS versions,
security software acceptance, upgrades, uninstall and real user permissions need
manual verification.

Optional plant APIs, weather and satellite services were not exercised. WebEngine
and Qt3D imports are checked; interactive map display and 3D view quality are not.
There is no signing certificate in this task.
