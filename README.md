![Open Garden Planner Banner](src/open_garden_planner/resources/icons/banner.png)

# Creative Landscape Studio

A desktop landscape planning prototype based on the actual
[Open Garden Planner](https://github.com/cofade/open-garden-planner) editor.
The current draft adds a compact landscape workspace, project-aware feet and
inches, architectural plant symbols, independent material texture strength,
and an editable sample plan. It preserves the inherited drawing, plants,
layers, undo/redo, `.ogp` save/load, autosave, exports, Gardening tools and
date/time sun simulation. Canonical geometry stays in centimeters.
See the owner's [master plan](MASTER_PLAN.md),
[continuation brief](CREATIVE_CONTINUATION_BRIEF.md), and
[actual desktop screenshots](docs/design/README.md).

## Trying the current prototype

The owner approved the [revised editor and welcome](docs/design/README.md).
The matching Windows installer is now undergoing native packaged validation.

The [available Windows foundation download](docs/WINDOWS_DOWNLOAD.md) was
built from `439e486414070161d9fea58a6123644e8d0afdc3`. It contains the older
Open Garden Planner interface and metric-only foundation, **not these revised
screenshots or imperial features**. No Windows download includes this
continuation yet, and no verified Mac installer is established.
See [current validation](docs/design/CONTINUATION_VALIDATION.md) and
[platform evidence](PLATFORM_STATUS.md).

Developers can run the current source with
`.venv/bin/python -m open_garden_planner`; `--classic` opens the inherited shell.
The [source checklist and sample launcher](docs/design/README.md#trying-the-source)
explain how to inspect the draft. The pull request stays a draft; no merge or
production release is authorized.

## Project records

- [Upstream assessment and exact provenance](UPSTREAM_PROVENANCE.md)
- [Feature reuse matrix](FEATURE_REUSE_MATRIX.md) and [roadmap](ROADMAP.md)
- [Current continuation validation](docs/design/CONTINUATION_VALIDATION.md) and [historical foundation checks](VALIDATION.md)
- [License and asset/data attribution](THIRD_PARTY_NOTICES.md)
- [Windows rebuild instructions](docs/WINDOWS_BUILD.md)
- [Original upstream README](docs/upstream/README.md) and [architecture docs](docs/05-building-block-view/README.md)

The full source remains in `src/open_garden_planner`, with upstream tests and
resources. The older browser experiment remains in draft PR #1 on its separate
branch; its `.clp` projects are unrelated to `.ogp`.

## Development in the cloud

Use Python 3.12 and the supported pyproject editable install.
Do not use the inherited, outdated requirements files.

```bash
UV_CACHE_DIR=/tmp/creative-uv-cache uv venv --allow-existing --python python3 .venv
UV_CACHE_DIR=/tmp/creative-uv-cache uv pip install --python .venv/bin/python -c installer/constraints-desktop.txt -e '.[dev]' pyinstaller
mkdir -p build/cloud-state/config build/cloud-state/data build/cloud-state/cache
export XDG_CONFIG_HOME="$PWD/build/cloud-state/config"
export XDG_DATA_HOME="$PWD/build/cloud-state/data"
export XDG_CACHE_HOME="$PWD/build/cloud-state/cache"
QT_QPA_PLATFORM=offscreen .venv/bin/python -m open_garden_planner --selftest
QT_QPA_PLATFORM=offscreen .venv/bin/python scripts/desktop_baseline_smoke.py --output build/source-smoke
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest tests/ -q
.venv/bin/python -m ruff check src/ tests/ scripts/
.venv/bin/python -m bandit -r src/ --severity-level high
.venv/bin/python scripts/check_agent_context.py
.venv/bin/python scripts/check_no_secrets.py
```

The offscreen smoke checks real application behavior through inherited loopback
MCP, using synthetic plans and editing disabled. Use an isolated development
account with no other app on port 8765. It cannot establish human usability or GPU
rendering. Processes must restart in each cloud task.

## License

Open Garden Planner is copyright its upstream contributors. This derived
application remains **GPL-3.0-or-later**; see [LICENSE](LICENSE).
Data and dependencies keep their respective licenses and notices.
This project has no Land F/X affiliation and claims no professional feature parity.

## Creative visual direction

The [desktop editor and welcome captures](docs/design/README.md) show the actual
Qt application opened by the normal entry point. See the
[design system](BRAND_DESIGN_SYSTEM.md), [redesign brief](CREATIVE_REDESIGN_BRIEF.md)
and [continuation brief](CREATIVE_CONTINUATION_BRIEF.md). Identity text is an
explicit placeholder. Visual approval is recorded; native Windows validation
remains necessary before the next test installer is uploaded.
