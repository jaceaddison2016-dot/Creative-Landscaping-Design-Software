# Platform status — Milestone A

Evidence as of 2026-10-08 UTC. Windows x64 is the immediate download target by owner
direction. No Mac was selected. Automated results are scoped to their runners;
manual use, signing, and supported OS versions require separate QA.

| Capability | Linux cloud | Windows x64 | macOS Apple Silicon | macOS Intel |
| --- | --- | --- | --- | --- |
| Supported dependency install | Pass: Python 3.12.14, matched Qt/Qt3D 6.11.0 | Pass native CI | Pass native macos-14 | Pass native macos-15-intel |
| Qt3D/runtime/API self-test | Pass source | Pass frozen | Pass source | Pass source |
| Inherited automated tests | Pass: 7,590 passed, 36 headless/platform skips, zero failures | Selected editor tests pass | Not run beyond self-test | Not run beyond self-test |
| Normal editor/save/export | Pass offscreen actual process | Pass portable and installed processes | Not verified | Not verified |
| Application package | Not a delivery target | Pass PyInstaller bundle and NSIS installer | Deferred by Windows-first direction | Deferred by Windows-first direction |
| Packaged startup/resources/exports | Not verified | Pass both copies; ZIP runtime/license/source contents and CRC checked | Not verified | Not verified |
| Installer execution | Not applicable | Pass silent installation on native runner | Not verified | Not verified |
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

The completed [Windows run 37707747601](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37707747601)
built commit `4419983e60d1037d8ec763b4a95d0e8268defdeb`. All build, self-test,
portable/installed smoke, archive-integrity and upload steps succeeded.
[Download its Windows x64 test artifact](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37707747601/artifacts/11520149105)
(about 436 MiB; GitHub sign-in may be required). Later commits change documentation
only; the runtime, resources, scripts and packaging match that recorded build.

Optional plant APIs, weather and satellite services were not exercised. WebEngine
and Qt3D imports are checked; interactive map display and 3D view quality are not.
There is no signing certificate in this task.
