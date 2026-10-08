# Try the Creative Landscape Studio Windows test build

[Download the Windows x64 test bundle](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773267264/artifacts/11549062663)
— **444.6 MiB**, built from `7c07a3220f0178f28ab7cf1b38a356cc6ff2aff1`.
The [native build and checks passed](https://github.com/jaceaddison2016-dot/Creative-Landscaping-Design-Software/actions/runs/37773267264).
This download contains the approved Creative interface and imperial features.
The Actions artifact expires **2027-01-06 UTC**; GitHub sign-in may be required.

This guide accompanies the approved Creative desktop test bundle. The window
opens **Creative Landscape Studio**, with feet and inches as the default for
new projects. Installer filenames and the Start menu shortcut retain **Open
Garden Planner** to preserve the inherited installer identity. Check
**BUILD-INFO.json** for the exact source commit used to build your download.
The old foundation build at `439e486414070161d9fea58a6123644e8d0afdc3` has the
earlier interface and metric-only foundation; it cannot demonstrate this work.
Use the successful test download linked above.

## Download and start

1. Open the **Windows test download** link above. Sign in
   to GitHub if needed and download **Creative-Landscape-Studio-Windows-x64-test**.
2. Right-click the downloaded ZIP and select **Extract All**.
3. Open **OpenGardenPlanner-v1.29.5-Setup.exe** and follow the installer. Start
   **Open Garden Planner** from the Start menu; the Creative workspace opens.

You do not need Python, a terminal, or coding. This build is for **64-bit Windows**
on Intel/AMD PCs. Windows ARM is not verified. The installer is unsigned;
Windows may show a publisher or SmartScreen warning. If security software blocks
it, keep protection enabled and report the message in the draft pull request.

For an option without installation, extract
**OpenGardenPlanner-v1.29.5-Windows-x64-Portable.zip** too, then open
**OpenGardenPlanner/OpenGardenPlanner.exe**. Keep the whole extracted folder
together, including **_internal** and **licenses**.

## Five-minute check

1. Use **Open Project** to open **Southwest Michigan - sample landscape.ogp**
   from the download. This editable sample contains a house, patio, walk, curved
   bed, plants and dimensions. Save your work in Documents using **File > Save As**.
2. Select the patio and edit its width. Try `10' 6 1/2"`. Undo with **Ctrl+Z**
   and redo with **Ctrl+Y**. Bare numbers mean feet; explicit cm/m work too.
3. Create a new plan and draw an object or place a plant from the library.
   **Dimensions > Project units** also offers decimal feet and metric.
4. Save, close, reopen the `.ogp` file and try **File > Export**.
5. Choose **Sun Study** in the workspace selector and change the date/time.
   The sample has a Michigan location. Times use your computer's time zone;
   shade is a geometric planning approximation that depends on object heights.

Save your own projects outside the installation/extracted app folder. The
company identity text remains a placeholder until an approved logo is supplied.

## What the automated Windows checks establish

The download is uploaded only after the actual portable and installed app pass
startup, Qt subsystem/server checks and real Qt key/mouse interaction: drawing,
plant placement, fractional-inch editing, undo/redo, save/reopen, physical
PNG/PDF/DXF/CSV exports, font glyphs, bundled icons and live sun/shade. Native screenshots
and JSON results are in **portable-creative-check** and **installed-creative-check**.
The older API smoke evidence is in **portable-check** and **installed-check**;
the source regression results are in **windows-editor-tests.xml**.

Human use on your PC, GPU rendering, installer upgrades/uninstall, printing,
native file dialogs, accessibility, display scaling and antivirus acceptance
still need manual testing. The local automation server is on by default at
`127.0.0.1:8765`; local programs can read/export/save through it. Editing tools
require explicit opt-in and a token. Disable it in Preferences if unused.

The source ZIP, PyQt binding source ZIP, license folder, notices, dependency
manifest and checksums accompany the download. Keep them when sharing this
**GPL-3.0-or-later** test build. Actions downloads expire after 90 days. The PR
remains a draft; no production release or merge is authorized. macOS remains
in scope, but there is no verified Mac installer for these changes.
