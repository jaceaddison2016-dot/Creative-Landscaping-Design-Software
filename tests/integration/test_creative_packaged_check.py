"""Exercise the production entry point's opt-in GUI check in a fresh process."""

import json
import os
import subprocess
import sys
from pathlib import Path


def test_actual_entrypoint_exercises_imperial_gui_and_exports(tmp_path, qtbot):
    root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    platform = "windows" if os.name == "nt" else "offscreen"
    env.update({"QT_QPA_PLATFORM": platform, "XDG_CONFIG_HOME": str(tmp_path / "config"),
                "XDG_DATA_HOME": str(tmp_path / "data"), "XDG_CACHE_HOME": str(tmp_path / "cache")})
    sample = root / "docs/design/creative-preview/revised-light/Southwest Michigan - sample landscape.ogp"
    original = sample.read_bytes()
    result = subprocess.run(
        [sys.executable, str(root / "scripts/run_packaged_creative_check.py"),
         "--output", str(tmp_path / "check"), "--sample", str(sample)],
        env=env, capture_output=True, text=True, timeout=150, check=False,
    )
    report = json.loads((tmp_path / "check/result.json").read_text())
    assert result.returncode == 0, result.stdout + result.stderr + str(report)
    assert report["status"] == "PASS"
    assert report["frozen"] is False  # This test does not establish a native Windows build.
    assert report["platform_plugin"] == platform
    assert report["imperial_width_cm"] == 321.31
    assert report["icons"] and report["control_font"]
    assert report["human_manual_test"] == "not performed"
    assert sample.read_bytes() == original


def test_prototype_check_rejects_extra_project_arguments(tmp_path, qtbot):
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    result = subprocess.run(
        [sys.executable, "-m", "open_garden_planner", "--prototype-check",
         str(tmp_path), "client-project.ogp"],
        env=env, capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 2
    assert not (tmp_path / "result.json").exists()


def test_direct_diagnostic_preserves_existing_untitled_recovery(tmp_path, qtbot):
    system_temp = tmp_path / "system-temp"
    system_temp.mkdir()
    recovery = system_temp / "~autosave_untitled.ogp"
    sentinel = b"synthetic recovery sentinel: never delete another account's work"
    recovery.write_bytes(sentinel)
    env = os.environ.copy()
    env.update({"QT_QPA_PLATFORM": "windows" if os.name == "nt" else "offscreen", "TMPDIR": str(system_temp),
                "TEMP": str(system_temp), "TMP": str(system_temp),
                "XDG_CONFIG_HOME": str(tmp_path / "config"),
                "XDG_DATA_HOME": str(tmp_path / "data"), "XDG_CACHE_HOME": str(tmp_path / "cache")})
    result = subprocess.run(
        [sys.executable, "-m", "open_garden_planner", "--prototype-check", str(tmp_path / "check")],
        env=env, capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert recovery.exists(), "Diagnostic deleted another account's untitled recovery"
    assert recovery.read_bytes() == sentinel
