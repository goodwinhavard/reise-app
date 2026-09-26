from datetime import date

from data.entries import TravelEntry, Location


def test_add_location_appends_to_entry():
    entry = TravelEntry(
        name="Test trip",
        country="Denmark",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 5),
        locations=[],
    )

    entry.add_location(Location("Copenhagen", 55.6761, 12.5683))

    assert len(entry.locations) == 1
    assert entry.locations[0].cname == "Copenhagen"
    assert entry.locations[0].x_coord == 55.6761
    assert entry.locations[0].y_coord == 12.5683
