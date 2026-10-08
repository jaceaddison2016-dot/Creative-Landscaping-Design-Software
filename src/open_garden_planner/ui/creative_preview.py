"""Experimental widgets attached to the real editor, awaiting owner approval."""

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from open_garden_planner.app.settings import get_settings
from open_garden_planner.core.tools import ToolType
from open_garden_planner.ui.creative_theme import heading_font
from open_garden_planner.ui.dialogs.welcome_dialog import WelcomeDialog
from open_garden_planner.ui.widgets.gallery_data import (
    GalleryItem,
    build_toolbar_categories,
    refresh_icon_thumbnails,
)


def _tr(text: str) -> str:
    return QCoreApplication.translate("CreativePreview", text)


def subtitle(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("CreativeSubtitle")
    label.setWordWrap(True)
    return label


def identity(*, compact: bool = False) -> QFrame:
    """Plain identity placeholder, deliberately not a fabricated company logo."""
    frame = QFrame()
    frame.setObjectName("CreativeIdentity")
    layout = QVBoxLayout(frame)
    if compact:
        layout.setContentsMargins(14, 7, 14, 7)
        frame.setFixedWidth(280)
    else:
        layout.setContentsMargins(20, 15, 20, 15)
    title = QLabel(_tr("Creative Landscape Studio"))
    font = title.font()
    font.setBold(True)
    title.setFont(font)
    title.setWordWrap(True)
    layout.addWidget(title)
    pending = QLabel(_tr("Identity placeholder") if compact else _tr("Text placeholder · identity approval pending"))
    pending.setObjectName("CreativePlaceholder")
    pending.setWordWrap(True)
    layout.addWidget(pending)
    return frame


class CreativeLibrary(QWidget):
    """Compact, searchable view of the existing placeable-object registry."""

    tool_selected = pyqtSignal(ToolType)
    item_selected = pyqtSignal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.categories = build_toolbar_categories()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 10, 10)
        self.search = QLineEdit()
        self.search.setPlaceholderText(_tr("Search objects and plants"))
        self.search.setAccessibleName(_tr("Search objects and plants"))
        self.search.setClearButtonEnabled(True)
        self.search.setToolTip(_tr("Filter the built-in object library"))
        layout.addWidget(self.search)
        self.category = QComboBox()
        self.category.setAccessibleName(_tr("Object category"))
        self.category.addItem(_tr("All objects"))
        self.category.addItems([category.name for category in self.categories])
        layout.addWidget(self.category)
        self.items = QListWidget()
        self.items.setObjectName("CreativeLibrary")
        self.items.setIconSize(QSize(36, 36))
        self.items.setAccessibleName(_tr("Placeable objects"))
        self.items.setToolTip(_tr("Choose an object, then place it on the canvas"))
        layout.addWidget(self.items)
        layout.addWidget(subtitle(_tr("Choose an object, then place it on the canvas")))
        self.search.textChanged.connect(self._populate)
        self.category.currentIndexChanged.connect(self._populate)
        self.items.itemClicked.connect(self._activate)
        self.items.itemActivated.connect(self._activate)
        self._populate()

    def _populate(self) -> None:
        self.items.clear()
        query = self.search.text().casefold()
        selected = self.category.currentIndex()
        for index, category in enumerate(self.categories, start=1):
            if selected not in (0, index):
                continue
            for item in category.items:
                if query not in item.name.casefold():
                    continue
                row = QListWidgetItem(item.name)
                if item.thumbnail is not None:
                    row.setIcon(QIcon(item.thumbnail))
                row.setData(Qt.ItemDataRole.UserRole, item)
                row.setToolTip(item.name)
                self.items.addItem(row)

    def _activate(self, row: QListWidgetItem) -> None:
        item = row.data(Qt.ItemDataRole.UserRole)
        if isinstance(item, GalleryItem):
            self.tool_selected.emit(item.tool_type)
            self.item_selected.emit(item)

    def refresh_theme_icons(self) -> None:
        refresh_icon_thumbnails(self.categories)
        self._populate()


class CreativeWelcomeDialog(WelcomeDialog):
    """Proposed welcome, reusing the upstream opening/recents signal contract."""

    def _setup_ui(self) -> None:
        self.setWindowTitle(_tr("Creative design preview"))
        self.setMinimumSize(820, 540)
        self.setMaximumSize(1300, 900)
        self.resize(1080, 660)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        body = QHBoxLayout()
        body.setSpacing(0)
        rail = identity()
        rail.setFixedWidth(250)
        rail.layout().addStretch()
        note = QLabel(_tr("A workspace for landscape planning"))
        note.setWordWrap(True)
        rail.layout().addWidget(note)
        body.addWidget(rail)
        content = QWidget()
        content.setObjectName("CreativeWelcomeContent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(36, 30, 36, 24)
        layout.setSpacing(16)
        title = QLabel(_tr("Start a project"))
        title.setFont(heading_font())
        layout.addWidget(title)
        layout.addWidget(subtitle(_tr("Create a landscape plan or return to your work.")))
        actions = QHBoxLayout()
        self.new_button = QPushButton(_tr("New project"))
        self.new_button.setProperty("buttonRole", "primary")
        self.new_button.setToolTip(_tr("Create a new landscape plan"))
        self.new_button.clicked.connect(self._on_new_project)
        self.open_button = QPushButton(_tr("Open project…"))
        self.open_button.setToolTip(_tr("Open an existing .ogp project"))
        self.open_button.clicked.connect(self._on_open_project)
        actions.addWidget(self.new_button)
        actions.addWidget(self.open_button)
        actions.addStretch()
        layout.addLayout(actions)
        line = QFrame()
        line.setObjectName("CreativeRule")
        line.setFixedHeight(2)
        layout.addWidget(line)
        layout.addWidget(QLabel(_tr("Recent projects")))
        self._recent_list = QListWidget()
        self._recent_list.setObjectName("CreativeRecents")
        self._recent_list.setAccessibleName(_tr("Recent projects"))
        self._recent_list.setIconSize(QSize(130, 85))
        self._recent_list.itemDoubleClicked.connect(self._on_recent_double_clicked)
        self._recent_list.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self._recent_list, 1)
        row = QHBoxLayout()
        self._open_selected_btn = QPushButton(_tr("Open selected"))
        self._open_selected_btn.setEnabled(False)
        self._open_selected_btn.clicked.connect(self._on_open_selected)
        row.addWidget(self._open_selected_btn)
        clear = QPushButton(_tr("Clear recent list"))
        clear.clicked.connect(self._on_clear_recent)
        row.addWidget(clear)
        row.addStretch()
        layout.addLayout(row)
        layout.addWidget(subtitle(_tr("Built on Open Garden Planner · GPL-3.0-or-later")))
        self._setup_footer(layout)
        body.addWidget(content, 1)
        outer.addLayout(body)
        self._populate_recent_files()

    def add_project_thumbnail(self, path: Path, pixmap: QPixmap) -> None:
        """Use a real plan capture, never an unapproved portfolio photograph."""
        for index in range(self._recent_list.count()):
            row = self._recent_list.item(index)
            if row.data(Qt.ItemDataRole.UserRole) == str(path):
                row.setIcon(QIcon(pixmap))
                row.setSizeHint(QSize(400, 112))

    def _populate_recent_files(self) -> None:
        super()._populate_recent_files()
        for index, file_path in enumerate(get_settings().recent_files):
            path = Path(file_path)
            if path.is_file():
                edited = datetime.fromtimestamp(path.stat().st_mtime).strftime("%b %d, %Y")
                row = self._recent_list.item(index)
                row.setText(_tr("{name}\nModified {date}").format(name=path.stem, date=edited))
