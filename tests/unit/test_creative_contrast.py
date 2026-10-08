"""Measured proposed token pairs; this does not certify the entire inherited UI."""

import pytest

from open_garden_planner.ui.creative_theme import CHROME, DARK, LIGHT


def contrast(first: str, second: str) -> float:
    def luminance(color: str) -> float:
        channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                  for value in channels]
        return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722), strict=True))
    bright, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (bright + 0.05) / (dark + 0.05)


TEXT_PAIRS = [
    ("text_primary", "surface"), ("text_primary", "background"),
    ("text_secondary", "surface"), ("text_secondary", "background"),
    ("text_secondary", "selection"), ("text_disabled", "input_disabled"),
    ("accent_text", "accent"), ("text_primary", "button_pressed"),
    ("success", "success_bg"), ("warning", "warning_bg"),
    ("error", "error_bg"), ("info", "info_bg"), ("caution", "surface"),
]


@pytest.mark.parametrize("palette", [LIGHT, DARK], ids=["light", "dark"])
@pytest.mark.parametrize(("foreground", "background"), TEXT_PAIRS)
def test_text_tokens_meet_aa(palette, foreground, background):
    assert contrast(palette[foreground], palette[background]) >= 4.5


@pytest.mark.parametrize("palette", [LIGHT, DARK], ids=["light", "dark"])
@pytest.mark.parametrize("foreground", ["border", "border_focus"])
@pytest.mark.parametrize("background", ["surface", "input", "background"])
def test_essential_control_boundaries(palette, foreground, background):
    assert contrast(palette[foreground], palette[background]) >= 3


def test_identity_and_placeholder_text():
    assert contrast(CHROME["on_identity"], CHROME["identity"]) >= 4.5
    assert contrast(CHROME["placeholder"], CHROME["identity"]) >= 4.5
