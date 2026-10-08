# Platform status — Creative desktop prototype

Evidence as of **2026-10-08 UTC**. Windows x64 is the owner's immediate download
target. The approved Creative layout and imperial changes have a matching
[Windows test download](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773267264/artifacts/11549062663),
built from **`7c07a3220f0178f28ab7cf1b38a356cc6ff2aff1`**.
Later documentation/evidence commits do not change that built application.

| Capability | Linux cloud | Windows x64 | macOS Apple Silicon | macOS Intel |
| --- | --- | --- | --- | --- |
| Dependency install | Python 3.12.14, Qt/Qt3D 6.11.0 passed | Native runner passed | Earlier foundation probe passed | Earlier foundation probe passed |
| Qt3D/runtime/API self-test | Source passed | Both frozen copies passed, no inherited console handles | Earlier source probe passed | Earlier source probe passed |
| Automated regression | **7,726 passed / 36 skipped / 42 warnings** on build source | **282 passed**, native Qt Windows plugin | Continuation not run | Continuation not run |
| Actual editor/save/reopen/exports | Source offscreen workflows passed | Portable and installed normal-process/MCP and real Qt key/mouse workflows passed | Not verified | Not verified |
| Approved Creative interface/imperial input | Source workflows and light/dark/small captures | Both packaged copies passed; installed screenshots recorded | Not verified | Not verified |
| Application package | Not a delivery target | PyInstaller portable + NSIS installer passed; source/notices/ZIP CRC checked | No verified installer | No verified installer |
| Installer execution | Not applicable | Silent installation on native runner passed | Not verified | Not verified |
| Human usability | Not tested | Owner test pending | Not tested | Not tested |
| GPU 3D / printing | Not verified; platform/render skips | Not verified | Not verified | Not verified |
| Code signing / notarization | Not applicable | Unsigned | Not verified | Not verified |

[Windows run 37773267264](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773267264)
completed successfully. Both portable and installed apps passed normal startup,
subsystem checks, drawing, mouse plant placement, fractional-inch edits, undo/redo,
save/reopen, physical PNG/PDF/DXF/CSV exports, font glyphs, icons and live sun/shade.
[Actual native captures](docs/design/windows-verified/README.md) include exact build
identity, results and capture hashes. The constrained runner overview shows label
overlap; manual scaling/usability remains open. See [full evidence](docs/design/CONTINUATION_VALIDATION.md)
and [no-coding installation instructions](docs/WINDOWS_DOWNLOAD.md).

Windows ARM, older OS versions, native dialogs, real display scaling, accessibility,
security-software acceptance, printing, upgrades/uninstall and human user permissions
still need manual verification. Optional plant/weather/satellite services and GPU
3D rendering were not exercised. Import checks do not establish interactive 3D quality.

## Earlier foundation evidence

[Mac probe run 37706636013](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37706636013)
installed inherited dependencies and passed the actual source self-test on both
architectures without altering Qt pins. This establishes import/loopback viability,
not a verified .app, DMG, universal binary or interactive editor. Mac packaging
remains in scope and is deferred following the owner's Windows request.

The earlier [Windows foundation run 37707747601](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37707747601)
built `4419983e60d1037d8ec763b4a95d0e8268defdeb` and passed its foundation checks.
It and the later foundation build `439e486414070161d9fea58a6123644e8d0afdc3`
precede the approved Creative continuation. Use the new download above to try
the current interface and imperial features.
