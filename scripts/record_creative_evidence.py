"""Record synthetic native screenshots in GitHub logs as well as the artifact.

This permits review through the GitHub API when an environment cannot access
Actions' external artifact-storage hostname. No arbitrary files are included.
"""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path

IMAGES = ("editor.png", "imperial-properties.png", "sun-study.png", "welcome.png")


def record(directory: Path, build_info: Path) -> None:
    result = json.loads((directory / "result.json").read_text(encoding="utf-8"))
    info = json.loads(build_info.read_text(encoding="utf-8-sig"))
    source_commit = os.environ.get("GITHUB_SHA")
    if (result.get("status") != "PASS" or not result.get("frozen")
            or result.get("os") != "nt" or not source_commit
            or result.get("platform_plugin") != "windows"
            or result.get("native_standard_handles_inherited", True)
            or info.get("source_commit") != source_commit):
        raise RuntimeError("Native evidence does not match this successful Windows build")
    encoded = {}
    inventory = {}
    for name in IMAGES:
        data = (directory / name).read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) > 5_000_000:
            raise RuntimeError(f"Invalid native screenshot: {name}")
        value = base64.b64encode(data).decode("ascii")
        parts = [value[index:index + 8192] for index in range(0, len(value), 8192)]
        inventory[name] = {"sha256": hashlib.sha256(data).hexdigest(), "parts": len(parts)}
        encoded[name] = parts
    print("CREATIVE_EVIDENCE_META " + json.dumps({"build_info": info, "result": result,
                                               "images": inventory}))
    for name, parts in encoded.items():
        for index, part in enumerate(parts):
            print("CREATIVE_EVIDENCE_IMAGE " + json.dumps({"name": name, "part": index, "data": part}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--build-info", type=Path, required=True)
    args = parser.parse_args()
    record(args.directory, args.build_info)


if __name__ == "__main__":
    main()
