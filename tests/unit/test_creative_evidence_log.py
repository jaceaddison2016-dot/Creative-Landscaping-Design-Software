"""Native evidence logging must transfer bytes intact and reject wrong builds."""

import base64
import hashlib
import json
import runpy
from pathlib import Path

import pytest


@pytest.mark.parametrize("fault", [None, "commit", "source", "handles", "platform", "image"])
def test_native_evidence_log_integrity_and_build_identity(tmp_path, monkeypatch, capsys, fault):
    root = Path(__file__).resolve().parents[2]
    record = runpy.run_path(str(root / "scripts/record_creative_evidence.py"))["record"]
    source_commit = "a" * 40
    monkeypatch.setenv("GITHUB_SHA", source_commit)
    report = {"status": "PASS", "frozen": True, "os": "nt", "platform_plugin": "windows",
              "native_standard_handles_inherited": False}
    if fault == "source":
        report["frozen"] = False
    if fault == "handles":
        report["native_standard_handles_inherited"] = True
    if fault == "platform":
        report["platform_plugin"] = "offscreen"
    (tmp_path / "result.json").write_text(json.dumps(report))
    info = tmp_path / "BUILD-INFO.json"
    info.write_text(json.dumps({"source_commit": "b" * 40 if fault == "commit" else source_commit}))
    image = (root / "docs/design/creative-preview/revised-small/editor.png").read_bytes()
    names = ("editor.png", "imperial-properties.png", "sun-study.png", "welcome.png")
    for name in names:
        (tmp_path / name).write_bytes(b"corrupt" if fault == "image" else image)
    if fault:
        with pytest.raises(RuntimeError):
            record(tmp_path, info)
        assert capsys.readouterr().out == ""  # Do not record partially validated evidence.
        return
    record(tmp_path, info)
    lines = capsys.readouterr().out.splitlines()
    metadata = json.loads(lines[0].removeprefix("CREATIVE_EVIDENCE_META "))
    chunks = [json.loads(line.removeprefix("CREATIVE_EVIDENCE_IMAGE ")) for line in lines[1:]]
    for name in names:
        parts = [part["data"] for part in chunks if part["name"] == name]
        restored = base64.b64decode("".join(parts), validate=True)
        assert restored == image
        assert len(parts) == metadata["images"][name]["parts"]
        assert hashlib.sha256(restored).hexdigest() == metadata["images"][name]["sha256"]
