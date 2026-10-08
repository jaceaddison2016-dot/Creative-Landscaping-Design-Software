"""Fault injection for native evidence and Windows launch-handle contracts."""

import json
import runpy
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.mark.parametrize("fault", [None, "stale", "handles", "source", "exit"])
def test_frozen_driver_has_no_inherited_streams_and_rejects_false_evidence(tmp_path, monkeypatch, fault):
    script = Path(__file__).resolve().parents[2] / "scripts/run_packaged_creative_check.py"
    driver = runpy.run_path(str(script))["run_check"]

    def spawn(command, **kwargs):
        # CPython's Windows all-None path avoids duplicating parent console
        # handles. DEVNULL mixed with None would make this contract fail.
        assert kwargs["stdin"] is kwargs["stdout"] is kwargs["stderr"] is None
        assert kwargs["close_fds"] is True
        assert kwargs["cwd"] == tmp_path.resolve()
        assert "QT_QPA_PLATFORM" not in kwargs["env"]
        report = {
            "status": "PASS", "run_id": kwargs["env"]["CREATIVE_PROBE_RUN_ID"],
            "frozen": True, "os": "nt", "platform_plugin": "windows",
            "native_standard_handles_inherited": False, "checks": ["synthetic fault injection"],
        }
        if fault == "stale":
            report["run_id"] = "previous-run"
        elif fault == "handles":
            report["native_standard_handles_inherited"] = True
        elif fault == "source":
            report["frozen"] = False
        (tmp_path / "result.json").write_text(json.dumps(report))
        for name in ("imperial-roundtrip.ogp", "physical.png", "physical.pdf", "physical.dxf",
                     "physical.csv", "editor.png", "sun-study.png", "welcome.png",
                     "imperial-properties.png"):
            (tmp_path / name).write_bytes(b"test evidence")
        return SimpleNamespace(wait=lambda **_kwargs: 2 if fault == "exit" else 0)

    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    monkeypatch.setattr(subprocess, "Popen", spawn)
    if fault:
        with pytest.raises(RuntimeError, match="workflow failed|Expected frozen native"):
            driver(tmp_path / "OpenGardenPlanner.exe", tmp_path)
    else:
        assert driver(tmp_path / "OpenGardenPlanner.exe", tmp_path)["status"] == "PASS"
