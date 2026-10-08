"""Preserve installed dependency notices and exact PyQt binding source archives.

Run inside the build environment before NSIS so notices accompany both bundles.
Downloads use PyPI's published SHA-256, with normal HTTPS verification enabled.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import sysconfig
import urllib.request
from importlib.metadata import distributions
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "src" / "open_garden_planner" / "resources"


def download_binding_source(name: str, version: str, destination: Path) -> dict:
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=60) as response:
        metadata = json.load(response)
    source = next(f for f in metadata["urls"] if f["packagetype"] == "sdist")
    target = destination / source["filename"]
    with urllib.request.urlopen(source["url"], timeout=120) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest != source["digests"]["sha256"]:
        target.unlink()
        raise RuntimeError(f"Source checksum mismatch: {name} {version}")
    return {"name": name, "version": version, "file": target.name,
            "url": source["url"], "sha256": digest}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--binding-sources", type=Path,
                        help="Also download exact GPL PyQt/sip sources into this directory")
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "LICENSE", output / "GPL-3.0.txt")
    shutil.copy2(ROOT / "THIRD_PARTY_NOTICES.md", output / "THIRD_PARTY_NOTICES.md")
    for path in RESOURCES.rglob("*"):
        if path.is_file() and (path.name.startswith("LICENSE") or path.name == "PROVENANCE.md"):
            destination = output / "upstream-assets" / path.relative_to(RESOURCES)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
    data_notices = {}
    for path in (RESOURCES / "data").rglob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            notices = {k: data[k] for k in ("license", "attribution", "sources", "source", "description") if k in data}
            if notices:
                data_notices[str(path.relative_to(RESOURCES))] = notices
    (output / "data-attribution.json").write_text(json.dumps(data_notices, indent=2), encoding="utf-8")
    python_license = next((p for p in (
        Path(sys.base_prefix) / "LICENSE.txt",
        Path(sysconfig.get_path("stdlib")) / "LICENSE.txt",
    ) if p.is_file()), None)
    if not python_license:
        raise RuntimeError("Python's license file was not found; do not package without it")
    shutil.copy2(python_license, output / "Python-LICENSE.txt")
    installed = {}
    for dist in distributions():
        name = dist.metadata["Name"]
        key = re.sub(r"[-_.]+", "-", name).lower()
        installed[key] = dist
    inventory = []
    sources = []
    if args.binding_sources:
        args.binding_sources.mkdir(parents=True, exist_ok=True)
    for key, dist in sorted(installed.items()):
        name, version = dist.metadata["Name"], dist.version
        if key == "open-garden-planner":
            continue  # The application's full source archive and GPL are supplied separately.
        directory = output / "dependencies" / f"{key}-{version}"
        directory.mkdir(parents=True, exist_ok=True)
        # Preserve raw metadata: serializing the parsed email object rejects
        # valid older multiline Description headers (e.g. altgraph's wheel).
        metadata_text = dist.read_text("METADATA") or dist.read_text("PKG-INFO")
        if metadata_text is None:
            raise RuntimeError(f"Distribution metadata is missing: {name}")
        (directory / "METADATA.txt").write_text(metadata_text, encoding="utf-8")
        notices = []
        for path in dist.files or []:
            if any(word in path.name.lower() for word in ("license", "copying", "notice", "copyright")):
                source = Path(dist.locate_file(path))
                if source.is_file():
                    # Keep relative package paths; reject any metadata path escaping the notice dir.
                    relative = Path(*[part for part in path.parts if part not in ("..", ".")])
                    destination = directory / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
                    notices.append(str(relative))
        inventory.append({"name": name, "version": version,
                          "license_expression": dist.metadata.get("License-Expression"),
                          "license": dist.metadata.get("License"),
                          "project_urls": dist.metadata.get_all("Project-URL", []),
                          "home_page": dist.metadata.get("Home-page"), "notice_files": notices})
        if args.binding_sources and key in {"pyqt6", "pyqt6-3d", "pyqt6-webengine", "pyqt6-sip"}:
            sources.append(download_binding_source(name, version, args.binding_sources))
    (output / "dependency-manifest.json").write_text(json.dumps({
        "python": sys.version, "platform": sys.platform, "packages": inventory,
    }, indent=2), encoding="utf-8")
    if args.binding_sources:
        (args.binding_sources / "SOURCE_MANIFEST.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
        if len(sources) != 4:
            raise RuntimeError("Expected all four PyQt/sip binding source archives")
    print(f"Preserved {len(inventory)} dependency metadata/notice sets and {len(sources)} source archives")


if __name__ == "__main__":
    main()
