"""Reject missing/corrupt Windows download archives before uploading them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile


def verify_archive(path: Path, required: set[str]) -> set[str]:
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        if missing := required - names:
            raise RuntimeError(f"{path.name} is missing {sorted(missing)}")
        if corrupt := archive.testzip():
            raise RuntimeError(f"{path.name} contains corrupt member {corrupt}")
        return names


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    directory = args.directory
    installer = directory / "OpenGardenPlanner-v1.29.5-Setup.exe"
    with installer.open("rb") as executable:
        if executable.read(2) != b"MZ":
            raise RuntimeError("Installer is not a Windows executable")
    portable = verify_archive(directory / "OpenGardenPlanner-v1.29.5-Windows-x64-Portable.zip", {
        "OpenGardenPlanner/OpenGardenPlanner.exe", "OpenGardenPlanner/licenses/GPL-3.0.txt",
        "OpenGardenPlanner/licenses/dependency-manifest.json",
        "OpenGardenPlanner/licenses/data-attribution.json",
    })
    for suffix in ("qwindows.dll", "qt6core.dll", "qt63dcore.dll", "qtwebengineprocess.exe", ".qm"):
        if not any(name.lower().endswith(suffix) for name in portable):
            raise RuntimeError(f"Portable archive is missing runtime resource {suffix}")
    verify_archive(directory / "CreativeLandscapeStudio-Source.zip", {
        "LICENSE", "pyproject.toml", "UPSTREAM_PROVENANCE.md",
        "src/open_garden_planner/main.py", "installer/ogp.spec",
        "installer/build_installer.py", ".github/workflows/windows-prototype.yml",
    })
    sources_path = directory / "PyQt-Binding-Sources.zip"
    sources = verify_archive(sources_path, {"binding-sources/SOURCE_MANIFEST.json"})
    with ZipFile(sources_path) as archive:
        manifest = json.loads(archive.read("binding-sources/SOURCE_MANIFEST.json"))
    if len(manifest) != 4 or any("binding-sources/" + entry["file"] not in sources for entry in manifest):
        raise RuntimeError("Binding sources are incomplete")
    print("DOWNLOAD ARCHIVES PASS: installer, portable runtime, application source and binding sources")


if __name__ == "__main__":
    main()
