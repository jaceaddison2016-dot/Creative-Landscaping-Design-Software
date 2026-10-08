"""Private local previews generated from the user's real canvas on save."""

import hashlib
import logging
from pathlib import Path

from PyQt6.QtCore import QStandardPaths, Qt


def thumbnail_path(project: Path) -> Path:
    key = hashlib.sha256(f"{project.resolve()}:{project.stat().st_mtime_ns}".encode()).hexdigest()
    base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    if not base:
        raise OSError("No local application-data directory")
    return Path(base) / "project-thumbnails" / f"{key}.png"


def save_thumbnail(view, project: Path) -> None:
    try:
        target = thumbnail_path(project)
        target.parent.mkdir(parents=True, exist_ok=True)
        pixmap = view.viewport().grab().scaled(320, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
        if not pixmap.save(str(target)):
            raise OSError("Could not write project thumbnail")
    except OSError:
        logging.getLogger(__name__).warning("Project saved; its optional local thumbnail could not be cached")
