from data.entries import TravelEntry, Location
from data.sidebar import dict_to_entry, entry_to_dict


def test_add_location_appends_to_entry():
    entry = TravelEntry(
        name="Test trip",
        country="Denmark",
        year=2025,
        days=4,
        locations=[],
    )

    entry.add_location(Location("Copenhagen", 55.6761, 12.5683))

    assert len(entry.locations) == 1
    assert entry.locations[0].cname == "Copenhagen"
    assert entry.locations[0].x_coord == 55.6761
    assert entry.locations[0].y_coord == 12.5683


def test_entry_serialization_uses_year_and_days():
    entry = TravelEntry(
        name="Test trip",
        country="Denmark",
        year=2025,
        days=4,
        locations=[],
    )

    serialized = entry_to_dict(entry)
    restored = dict_to_entry(serialized)

    assert serialized["year"] == 2025
    assert serialized["days"] == 4
    assert "start_date" not in serialized
    assert "end_date" not in serialized
    assert restored.year == 2025
    assert restored.days == 4


def test_legacy_date_data_is_loaded_as_year_and_days():
    entry = dict_to_entry({
        "name": "Legacy trip",
        "country": "Denmark",
        "start_date": "2025-01-01",
        "end_date": "2025-01-05",
    })

    assert entry.year == 2025
    assert entry.days == 4
