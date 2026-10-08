# Third-party notices for this desktop baseline

Creative Landscape Studio's Milestone A test build derives from **Open Garden
Planner**, copyright its upstream contributors, by cofade:
https://github.com/cofade/open-garden-planner.
The application remains **GPL-3.0-or-later**, as declared by its upstream
`pyproject.toml`. The full GPL text remains in `LICENSE`. There is no warranty.
You may use, study, modify, and redistribute it under that license. No additional
restriction on modifying or reverse engineering the included libraries is imposed.

The Windows test download includes the exact application source and build scripts,
the build commit ID, dependency versions, and this notice. PyQt6, PyQt6-3D,
PyQt6-WebEngine, and PyQt6-sip binding source archives are supplied beside it,
downloaded from their exact PyPI versions with published SHA-256 verification.
The `licenses/` directory inside the installed and portable app preserves installed
distribution license files and metadata, Python's license, and upstream asset
provenance. Build tools are included in the inventory even when not shipped.

## Qt and PyQt

The free PyQt bindings use GPL terms; no commercial PyQt license is asserted.
Qt libraries use their respective LGPL/GPL and third-party terms, preserved from
the installed wheels. The bundle uses shared Qt DLLs, which can be replaced with
interface-compatible modified versions. Rebuilding is also possible from the
supplied application and binding sources; see `docs/WINDOWS_BUILD.md`.

Exact unmodified Qt sources and associated third-party notices are available from
the Qt project's source archive directories (source versions are also recorded in
`licenses/dependency-manifest.json`):

- Qt 6.11.0 base modules and Qt3D:
  https://download.qt.io/archive/qt/6.11/6.11.0/submodules/
- Qt WebEngine 6.10.2 and its corresponding Chromium third-party sources/notices:
  https://download.qt.io/archive/qt/6.10/6.10.2/submodules/
- Qt source licensing documentation:
  https://doc.qt.io/qt-6/licensing.html

These are upstream source locations, not a claim of an independent legal audit of
every library. Preserve the accompanying notices and source access when redistributing.

## Assets and plant data

Upstream images, textures, icons, and data remain unchanged. Their existing
`PROVENANCE.md` files are preserved in the source, frozen resources, and license
bundle. Tabler UI icons retain `LICENSE-tabler-icons.txt` (MIT).

The bundled `plant_species.json` declares **CC BY-SA 4.0**:
https://creativecommons.org/licenses/by-sa/4.0/.
Its attribution names RHS, Cornell Cooperative Extension, Royal Botanic Gardens
Kew, USDA/GRIN, University of Minnesota Extension, and Oregon State University
Extension. The upstream data describes derived curated horticultural references,
not verbatim copies. Its license and attribution metadata remain intact, and are
also copied into `licenses/data-attribution.json`. Other datasets retain their
own provenance. No newly sourced commercial landscape assets are included.

Online plant providers, satellite imagery, and weather services have their own
terms. No API keys, purchased imagery, or provider results are bundled. These
optional services were not verified for redistribution or commercial use here.
Land F/X is a reference for the future workflow only; this project has no
affiliation with Land F/X and includes none of its code or assets.
