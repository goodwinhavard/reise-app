class TravelEntry:
    def __init__(self, name, country, start_date, end_date, locations, text=None, photos=None):
        self.name = name
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.locations = locations
        self.text = text
        self.photos = photos or []  # list of relative file paths

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name

    def get_country(self):
        return self.country
    def set_country(self, country):
        self.country = country

    def get_start_date(self):
        return self.start_date
    def set_start_date(self, start_date):
        self.start_date = start_date

    def get_end_date(self):
        return self.end_date
    def set_end_date(self, end_date):
        self.end_date = end_date

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