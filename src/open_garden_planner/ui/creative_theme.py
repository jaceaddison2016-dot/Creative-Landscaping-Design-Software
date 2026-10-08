"""Approved Creative color direction for the derived desktop workspace.

The owner approved this palette; no official logo/font asset is supplied. Reuse the existing theme's
component styles and notification hooks; do not replace the canvas or data model.
"""

from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication

from open_garden_planner.ui.theme import ThemeColors, ThemeMode, apply_theme

LIGHT = {
    "background": "#F7F6F1", "background_alt": "#E7EEF3",
    "surface": "#FFFFFF", "surface_alt": "#E7EEF3",
    "text_primary": "#263441", "text_secondary": "#596875",
    "text_disabled": "#596875", "border": "#71808B",
    "border_focus": "#123B63", "accent": "#123B63",
    "accent_hover": "#102B46", "accent_pressed": "#102B46",
    "accent_text": "#FFFFFF", "button": "#FFFFFF",
    "button_hover": "#E7EEF3", "button_pressed": "#D8DDD9",
    "input": "#FFFFFF", "input_disabled": "#F7F6F1",
    "selection": "#E7EEF3", "selection_inactive": "#E7EEF3",
    "section_header": "#E7EEF3", "success": "#42644C",
    "warning": "#8A4B08", "caution": "#715A1D",
    "error": "#A33131", "info": "#123B63", "on_status": "#FFFFFF",
    "success_bg": "#EAF1E9", "warning_bg": "#FAEFDA",
    "error_bg": "#FBEAEA", "info_bg": "#E7EEF3",
    "canvas_background": "#F7F7F4", "canvas_outside": "#D8DDD9",
    "grid_line": "#D5D9D6", "grid_line_major": "#B4BDB7",
    "canvas_border": "#71808B", "scale_bar_fg": "#263441",
    "scale_bar_outline": "#FFFFFF",
    "overlay_border": "rgba(110, 180, 245, 220)",
    "overlay_field_border": "rgba(110, 180, 245, 180)",
}

DARK = {
    **LIGHT,
    "background": "#17232F", "background_alt": "#233444",
    "surface": "#1E2D3B", "surface_alt": "#304658",
    "text_primary": "#F3F5F6", "text_secondary": "#BAC8D3",
    "text_disabled": "#A6B5C2", "border": "#8295A5",
    "border_focus": "#8CC6FA", "accent": "#8CC6FA",
    "accent_hover": "#B4DAFC", "accent_pressed": "#70AFE5",
    "accent_text": "#102B46", "button": "#233444",
    "button_hover": "#304658", "button_pressed": "#36536C",
    "input": "#17232F", "input_disabled": "#233444",
    "selection": "#304658", "selection_inactive": "#233444",
    "section_header": "#304658", "success": "#A3C7A9",
    "warning": "#F2BC79", "caution": "#D8BC71",
    "error": "#FFA5A5", "info": "#8CC6FA", "on_status": "#102B46",
    "success_bg": "#233E30", "warning_bg": "#473722",
    "error_bg": "#492B32", "info_bg": "#233E55",
}

# Additional chrome-only roles. Gold is decoration, never ordinary body text.
CHROME = {"identity": "#102B46", "on_identity": "#FFFFFF", "gold": "#B79A4C", "placeholder": "#D8BC71"}


def font_family(*candidates: str) -> str:
    """Select an installed font without an online or bundled-font dependency."""
    available = set(QFontDatabase.families())
    return next((name for name in candidates if name in available), QApplication.font().family())


def heading_font() -> QFont:
    font = QFont(font_family("Source Serif 4", "Georgia", "DejaVu Serif"))
    font.setPixelSize(32)
    font.setWeight(QFont.Weight.DemiBold)
    return font


def apply_creative_theme(app: QApplication, mode: ThemeMode) -> None:
    """Opt in explicitly; calling ordinary apply_theme restores upstream colors."""
    resolved = ThemeColors.detect_system_theme() if mode == ThemeMode.SYSTEM else mode
    colors = DARK if resolved == ThemeMode.DARK else LIGHT
    font = QFont(font_family("Source Sans 3", "Segoe UI", "Helvetica Neue", "DejaVu Sans"))
    font.setPixelSize(14)
    if app.font() != font:
        app.setFont(font)
    # Only these named preview components get additional styling. The inherited
    # stylesheet continues to own menus, native-ish inputs and existing panels.
    component_stylesheet = f"""
        QFrame#CreativeIdentity {{ background: {CHROME['identity']}; }}
        QFrame#CreativeIdentity QLabel {{ background: transparent; color: {CHROME['on_identity']}; }}
        QFrame#CreativeIdentity QLabel#CreativePlaceholder {{ color: {CHROME['placeholder']}; }}
        QFrame#CreativeRule {{ background: {CHROME['gold']}; border: none; }}
        QLabel#CreativeSubtitle {{ color: {colors['text_secondary']}; background: transparent; }}
        QListWidget#CreativeLibrary::item {{ padding: 5px 3px; min-height: 34px; }}
        QListWidget#CreativeRecents::item {{ padding: 14px; }}
        QDockWidget#CreativeLibraryDock::title, QDockWidget#CreativePropertiesDock::title {{
            padding: 7px; background: {colors['surface']}; color: {colors['text_primary']};
        }}
        QWidget#CreativeWelcomeContent {{ background: {colors['background']}; }}
        QListWidget#CreativeLibrary:focus, QListWidget#CreativeRecents:focus {{
            border: 2px solid {colors['border_focus']};
        }}
    """
    apply_theme(app, resolved, color_overrides=colors, component_stylesheet=component_stylesheet)
