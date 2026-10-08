"""Exercise the actual Creative GUI and reject stale/incorrect build evidence."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path


def run_check(executable: Path | None, output: Path, sample: Path | None = None) -> dict:
    """Launch outside the checkout; frozen mode requires native Windows Qt."""
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    result_file = output / "result.json"
    result_file.unlink(missing_ok=True)
    if sample is not None:
        shutil.copyfile(sample.resolve(), output / "approved-sample.ogp")
    run_id = str(uuid.uuid4())
    env = os.environ.copy()
    env["CREATIVE_PROBE_RUN_ID"] = run_id
    command = [str(executable.resolve())] if executable else [sys.executable, "-m", "open_garden_planner"]
    if executable:
        # Never let the headless source-test setting turn a native gate into
        # another offscreen source check.
        env.pop("QT_QPA_PLATFORM", None)
    command += ["--prototype-check", str(output)]
    # Frozen Windows GUI mode has no console handles, like Explorer launch.
    # Source mode retains a log for diagnosis; neither mode inherits stdin.
    with (output / "source-process.log").open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            command, cwd=output, env=env, stdin=subprocess.DEVNULL,
            stdout=None if executable else log, stderr=None if executable else log,
            close_fds=True,
            creationflags=subprocess.DETACHED_PROCESS if executable and os.name == "nt" else 0,
        )
        try:
            code = process.wait(timeout=120)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=15)
            raise RuntimeError("Creative workflow check timed out; see diagnostic evidence") from None
    if not result_file.is_file():
        raise RuntimeError(f"Application exited {code} without current-run result.json")
    report = json.loads(result_file.read_text(encoding="utf-8"))
    if code != 0 or report.get("run_id") != run_id or report.get("status") != "PASS":
        raise RuntimeError(f"Application workflow failed (exit {code}): {report}")
    if executable and (not report.get("frozen") or report.get("os") != "nt"
                       or report.get("platform_plugin") != "windows"):
        raise RuntimeError(f"Expected frozen native Windows application: {report}")
    for name in ("imperial-roundtrip.ogp", "physical.png", "physical.pdf", "physical.dxf",
                 "physical.csv", "editor.png", "sun-study.png", "welcome.png",
                 "imperial-properties.png"):
        if not (output / name).is_file() or (output / name).stat().st_size == 0:
            raise RuntimeError(f"Application evidence missing: {name}")
    print(f"PASS: {len(report['checks'])} actual Creative workflows ({report['platform_plugin']})")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", type=Path, help="Frozen Windows executable; omit for source validation")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sample", type=Path)
    args = parser.parse_args()
    run_check(args.exe, args.output, args.sample)


if __name__ == "__main__":
    main()
