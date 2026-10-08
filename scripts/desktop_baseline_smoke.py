"""Exercise the real desktop process via its inherited loopback MCP interface.

Use only in an isolated development/CI account. Refuses an occupied API port;
never enables editing or supplies a token. Outputs contain synthetic data.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import csv
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parents[1]
PORT = 8765


def make_fixture(path: Path) -> None:
    """Save a small scene through the actual upstream serializer."""
    # WebEngine must be imported before QApplication, matching main.py.
    from PyQt6 import QtWebEngineWidgets  # noqa: F401
    from PyQt6.QtWidgets import QApplication

    from open_garden_planner.core.object_types import ObjectType
    from open_garden_planner.core.project import ProjectManager
    from open_garden_planner.ui.canvas.canvas_scene import CanvasScene
    from open_garden_planner.ui.canvas.items import CircleItem, RectangleItem

    app = QApplication.instance() or QApplication([])
    scene = CanvasScene(1200, 900)
    layer = scene.active_layer.id
    for item in (
        RectangleItem(100, 100, 300, 180, object_type=ObjectType.GARDEN_BED,
                      name="Baseline bed", layer_id=layer),
        RectangleItem(650, 100, 300, 250, object_type=ObjectType.HOUSE,
                      name="Baseline house", layer_id=layer),
        CircleItem(250, 650, 100, object_type=ObjectType.TREE,
                   name="Baseline tree", layer_id=layer),
        CircleItem(550, 650, 50, object_type=ObjectType.SHRUB,
                   name="Baseline shrub", layer_id=layer),
    ):
        scene.addItem(item)
    ProjectManager().save(scene, path)
    app.processEvents()


async def exercise(output: Path, *, export: bool) -> dict:
    async with (
        streamable_http_client(f"http://127.0.0.1:{PORT}/mcp") as (read, write, _),
        ClientSession(read, write) as session,
    ):
        await session.initialize()

        async def call(name: str, arguments: dict | None = None):
            result = await session.call_tool(name, arguments or {})
            if result.isError:
                raise RuntimeError(f"{name} failed: {result.content}")
            return result

        summary = (await call("get_plan_summary")).structuredContent
        expected = {"canvas_width_cm": 1200, "canvas_height_cm": 900,
                    "bed_count": 1, "plant_count": 2, "shape_count": 1}
        for key, value in expected.items():
            if not summary or summary.get(key) != value:
                raise RuntimeError(f"Loaded scene mismatch: {summary}; expected {expected}")
        tools = await session.list_tools()
        if any(tool.name in {"create_object", "move_object", "delete_object"}
               for tool in tools.tools):
            raise RuntimeError("Smoke account unexpectedly has editing enabled")
        if not export:
            return summary
        rendered = await call("render_canvas_image", {"image_width_px": 1024})
        png = next(c for c in rendered.content if c.type == "image")
        (output / "canvas.png").write_bytes(base64.b64decode(png.data))
        for name, suffix in (("save_plan", "ogp"), ("export_pdf", "pdf"),
                             ("export_dxf", "dxf"), ("export_csv", "csv")):
            path = output / f"roundtrip.{suffix}"
            result = await call(name, {"file_path": str(path)})
            if not result.structuredContent or result.structuredContent["format"] != suffix:
                raise RuntimeError(f"Wrong export response: {name}")
            if not path.is_file() or path.stat().st_size == 0:
                raise RuntimeError(f"Missing or empty export: {path}")
        return summary


def run_process(command: list[str], fixture: Path, output: Path, *, export: bool) -> dict:
    """Wait for startup, exercise exports, and stop only the child we started."""
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", PORT)) == 0:
            raise RuntimeError("API port occupied; close the existing app before this CI smoke")
    with (output / "process.log").open("ab") as log:
        # GUI exe gets no inherited console handles, matching double-click startup.
        process = subprocess.Popen(command + [str(fixture)], cwd=ROOT,
                                   stdout=log if os.name != "nt" else subprocess.DEVNULL,
                                   stderr=log if os.name != "nt" else subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 90
            while True:
                if process.poll() is not None:
                    raise RuntimeError(f"Desktop exited during startup: {process.returncode}")
                with socket.socket() as probe:
                    ready = probe.connect_ex(("127.0.0.1", PORT)) == 0
                if ready:
                    break
                if time.monotonic() >= deadline:
                    raise TimeoutError("Desktop MCP server did not start within 90 seconds")
                time.sleep(0.25)
            # Preserve the upstream 8-second startup gate, then verify real behavior.
            time.sleep(8)
            if process.poll() is not None:
                raise RuntimeError("Desktop failed the 8-second startup check")
            return asyncio.run(asyncio.wait_for(exercise(output, export=export), timeout=90))
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=15)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", type=Path, help="Frozen executable; omit for source app")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    fixture = output / "baseline.ogp"
    make_fixture(fixture)
    command = [str(args.exe.resolve())] if args.exe else [sys.executable, "-m", "open_garden_planner"]
    summary = run_process(command, fixture, output, export=True)
    if not (output / "canvas.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Invalid PNG")
    if not (output / "roundtrip.pdf").read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("Invalid PDF")
    import ezdxf

    drawing = ezdxf.readfile(output / "roundtrip.dxf")
    if len(drawing.modelspace()) < 4:
        raise RuntimeError("DXF is missing scene geometry")
    with (output / "roundtrip.csv").open(encoding="utf-8-sig", newline="") as csv_file:
        if not csv.DictReader(csv_file).fieldnames:
            raise RuntimeError("CSV is missing a header")
    saved = json.loads((output / "roundtrip.ogp").read_text(encoding="utf-8"))
    if len(saved["objects"]) != 4:
        raise RuntimeError("Save lost objects")
    reopened = run_process(command, output / "roundtrip.ogp", output, export=False)
    (output / "result.json").write_text(json.dumps({
        "status": "PASS", "command": command, "loaded": summary,
        "reopened": reopened, "exports": ["png", "pdf", "dxf", "csv", "ogp"],
        "interactive_mouse_checks": "not performed", "gpu_rendering": "not performed",
    }, indent=2), encoding="utf-8")
    print("DESKTOP BASELINE PASS: startup, scene load, render, exports, save and reopen")


if __name__ == "__main__":
    main()
