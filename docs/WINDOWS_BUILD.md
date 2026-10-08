# Rebuild the Windows test download

Use a Windows x64 development account, Python 3.12 x64, Git and NSIS. End users
can use the prebuilt download without these tools. `.github/workflows/windows-prototype.yml`
is the complete executable build recipe. The application source and PyQt binding
sources accompany each test download; Qt source locations are in
`THIRD_PARTY_NOTICES.md`. All libraries are unmodified at this milestone.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -c installer/constraints-desktop.txt -e ".[dev]" pyinstaller
.venv/Scripts/python installer/build_installer.py --version 1.29.5 --skip-nsis
.venv/Scripts/python scripts/collect_desktop_notices.py --output dist/OpenGardenPlanner/licenses --binding-sources dist/binding-sources
.venv/Scripts/python installer/build_installer.py --version 1.29.5 --skip-pyinstaller
$p = Start-Process dist/OpenGardenPlanner/OpenGardenPlanner.exe -ArgumentList '--selftest' -Wait -PassThru
if ($p.ExitCode -ne 0) { throw 'Frozen self-test failed' }
.venv/Scripts/python scripts/desktop_baseline_smoke.py --exe dist/OpenGardenPlanner/OpenGardenPlanner.exe --output build/windows-smoke
```

The operational smoke script expects an isolated account with default API settings
and refuses an occupied port. It creates synthetic plans, invokes inherited
save/export tools, and stops only the child it starts. Never run it against an
existing live project. It does not enable editing. Existing pytest fixtures
isolate their settings in a separate test organization.

The constraints record the validated Python 3.12 baseline. Windows-specific
transitives and exact downloaded wheels/hashes are recorded by pip's
`build-dependencies.json` report in each artifact. To relink with modified Qt,
replace compatible shared DLLs in `_internal/PyQt6/Qt6/bin`, or build the Qt/PyQt
sources and freeze again using the supplied spec. No signature or activation
key restricts rebuilding. Changes must preserve the GPL and dependency notices.

The inherited upstream automatic release workflow is restricted to the upstream
repository. This fork's workflow uploads test artifacts only; it creates no tags,
publishes no production release, and merges no pull requests.
