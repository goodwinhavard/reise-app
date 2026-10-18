class TravelEntry:
    def __init__(self, name, country, year, days, locations, text=None, photos=None):
        self.name = name
        self.country = country
        self.year = year
        self.days = days
        self.locations = locations or []
        self.text = text
        self.photos = photos or []  # list of relative file paths

    def add_location(self, location):
        self.locations.append(location)

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name

    def get_country(self):  
        return self.country
    def set_country(self, country):
        self.country = country

    def get_year(self):
        return self.year
    def set_year(self, year):
        self.year = year

    def get_days(self):
        return self.days
    def set_days(self, days):
        self.days = days

    def get_locations(self):
        return self.locations
    def set_locations(self, locations):
        self.locations = locations

    def get_text(self):
        return self.text
    def set_text(self, text):
        self.text = text

    def get_photos(self):
        return self.photos
    def set_photos(self, photos):
        self.photos = photos


class Location:
    def __init__(self, name, x_coord, y_coord):
        self.cname = name
        self.x_coord = x_coord
        self.y_coord = y_coord