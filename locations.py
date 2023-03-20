import geocoder
from geopy.geocoders import Nominatim


class Location:

    data_adress = {}

    def my_loc(self):
        g = geocoder.ip('me')

        return g.latlng

    def get_address(self):
        locator = Nominatim(user_agent="myGeocoder")
        coordinates = self.my_loc()[0], self.my_loc()[1]
        location = locator.reverse(coordinates)
        address_data = location.raw

        return address_data

    def save_data(self):
        Location.data_adress = self.get_address()

    def get_spec_add(self, name):

        return Location.data_adress["address"][name]


Location.save_data(Location())

x = Location.data_adress