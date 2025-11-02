class TravelEntry:
    def __init__(self, name, country, start_date, end_date):
        self.name = name
        self.country = country
        self.start_date = start_date
        self.end_date = end_date

        self.places = []


    def add_places(self, name, x_coordinate=None, y_coordinate=None, date=None):
            
        place = {
            "name": name,
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
            "date": date
        }
        self.places.append(place)


class Location:
    def __init__(self, name, x_coord, y_coord):
        self.cname = name
        self.x_coord = x_coord
        self.y_coord = y_coord