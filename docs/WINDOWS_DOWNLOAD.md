# Try the Windows desktop test build

This is Creative Landscape Studio's first desktop baseline, built from Open
Garden Planner 1.29.5. The window and installer still say **Open Garden Planner**.
It uses **centimeters/meters**; feet and inches are the next milestone.

## Download and start

1. Open the successful **Windows prototype download** run linked in the draft
   pull request. Sign in to GitHub if needed, scroll to **Artifacts**, and click
   **Creative-Landscape-Studio-Windows-x64-test**.
2. Right-click the downloaded ZIP and select **Extract All**.
3. Open **OpenGardenPlanner-v1.29.5-Setup.exe** and follow the installer. Start
   **Open Garden Planner** from the Start menu.

You do not need Python, a terminal, or coding. This build is for **64-bit Windows**
on Intel/AMD PCs. Windows ARM is not verified. The installer is unsigned;
Windows may show a publisher or SmartScreen warning. If security software blocks
it, keep protection enabled and report the message in the draft pull request.

For an option without installation, extract
**OpenGardenPlanner-v1.29.5-Windows-x64-Portable.zip** too, then open
**OpenGardenPlanner/OpenGardenPlanner.exe**. Keep the whole extracted folder
together, including **_internal** and **licenses**.

## Five-minute check

1. Create a new plan. Use the drawing tools to add a rectangle and a garden bed.
2. Drag a tree or shrub from the plant gallery onto the plan. Select and move it.
3. Undo the move, then redo it. Try changing its size and switching layers.
4. Use **File > Save As** to save a `.ogp` file in Documents. Close and reopen it.
5. Try an export and confirm the resulting image/PDF shows your objects.
6. For the inherited sun/shade controls, set the garden location and choose a
   date/time. Change the time and inspect the shadow overlay. Results are a
   planning approximation; building/tree heights and location affect them.

The download also contains **portable-check/baseline.ogp**, a tiny synthetic
four-object plan used by the automated checks. Use **File > Open** to try it.
Save your own work outside the application installation/extracted folder.

## What this download establishes

The workflow tests the actual frozen and installed editor: startup, bundled Qt3D
imports, loopback server, opening a plan, canvas rendering, PNG/PDF/DXF/CSV
output, saving, and reopening. `BUILD-INFO.json` identifies its exact source
commit. Evidence is in **portable-check**, **installed-check**, and the test XML.

Interactive mouse use on your PC, GPU rendering, installer upgrades/uninstall,
printing, antivirus acceptance, and code signing still need manual testing.
The local automation server is on by default at `127.0.0.1:8765`; other local
programs can read/export/save through it. Editing tools require explicit opt-in
and a token. Disable the server in Preferences if you do not need automation.

The source ZIP, PyQt binding source ZIP, license folder, notices, dependency
manifest and checksums accompany the download. Keep them when sharing this GPL
test build. Actions downloads expire after 90 days; this is not a production
release. There is no Mac download in this milestone.
