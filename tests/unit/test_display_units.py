"""Independent physical references and input rules for display-only units."""

import pytest

from open_garden_planner.core.units import (
    IMPERIAL,
    METRIC,
    DisplayUnits,
    LengthFormat,
    UnitSystem,
    format_area,
    format_length,
    format_volume,
    parse_length,
)


@pytest.mark.parametrize(("text", "cm"), [
    ('10\' 6"', 320.04), ('10 ft 6 in', 320.04), ('10.5', 320.04),
    ('-1\' 6 1/2"', -46.99), ('3/8 in', .9525), ('2\' 11 15/16"', 91.28125),
    ('20 ft', 609.6), ('100 cm', 100), ('1.2 m', 120), ('250 mm', 25),
])
def test_parse_imperial_physical_references(text, cm):
    assert parse_length(text, IMPERIAL) == pytest.approx(cm, abs=1e-10)


@pytest.mark.parametrize("text", ['', 'nan', 'inf', '1/0 in', '10 ft -6 in', '1,234', '1 yard', '2/3/4 in'])
def test_invalid_lengths_are_rejected(text):
    with pytest.raises(ValueError):
        parse_length(text, IMPERIAL)


def test_display_carry_negative_fraction_and_decimal_feet():
    assert format_length(320.04, IMPERIAL) == '10\' 6"'
    assert format_length(-46.99, IMPERIAL) == '-1\' 6 1/2"'
    assert format_length(30.47999, IMPERIAL) == '1\' 0"'
    decimal = DisplayUnits(UnitSystem.IMPERIAL, LengthFormat.DECIMAL_FEET)
    assert format_length(320.04, decimal) == '10.5000 ft'
    assert parse_length('100', METRIC) == 100
    assert format_area(92903.04, IMPERIAL) == '100.00 ft²'
    assert format_volume(764554.857984, IMPERIAL) == '1.000 yd³'


def test_missing_preferences_preserve_legacy_metric():
    assert DisplayUnits.from_dict(None) == METRIC
    assert DisplayUnits.from_dict({'system': 'bad'}) == METRIC
    assert DisplayUnits.from_dict(IMPERIAL.to_dict()) == IMPERIAL


def test_unicode_negative_sign_and_positional_project_compatibility():
    from open_garden_planner.core.project import ProjectData
    assert parse_length("−3/8 in", IMPERIAL) == pytest.approx(-.9525)
    objects = [{"type": "rectangle"}]
    assert ProjectData(500, 300, objects).objects is objects
