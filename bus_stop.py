from database_ft import DatabaseFetch as DF

import requests
from bs4 import BeautifulSoup

import time
import googlemaps


class BusStop:
    name_stop = []
    cord_stop = []
    url = ""

    def get_loc(self, city):

        if city == "arusha":
            self.url = DF.city_links(DF())["arusha".capitalize()]
        elif city == "dar es salaam":
            self.url = DF.city_links(DF())["Dar Es salaam"]
        elif city == "kilimanjaro":
            self.url = DF.city_links(DF())["kilimanjaro".capitalize()]
        elif city == "morogoro":
            self.url = DF.city_links(DF())["morogoro".capitalize()]
        elif city == "mbeya":
            self.url = DF.city_links(DF())["mbeya".capitalize()]
        elif city == "dodoma":
            BusStop.url = DF.city_links(DF())["dodoma".capitalize()]
        elif city == "tanga":
            self.url = DF.city_links(DF())[city]

        html = requests.get(self.url).content

        soup = BeautifulSoup(html, 'html.parser')

        temp = soup.find_all('div', attrs={'class': 'info-place'})
        name = soup.find_all('h2', attrs={'class': 'name'})
        for res in range(temp.__len__()):
            print(name[res].text.strip())
            long = temp[res].text.strip()

            word, cord = long.strip().split(":")

            print(cord.strip())

            self.name_stop.append(name[res].text.strip())
            self.cord_stop.append(cord.strip())


class GoogleBusStop:
    name_stop = []
    cord_stop = []

    API_KEY = 'AIzaSyBTG2Z2tCQyE4MiqIw6Cafil_TaVZaVON4'
    map_client = googlemaps.Client(API_KEY)

    def miles_to_meters(self, miles):
        try:
            return miles * 1_609.344
        except:
            return 0

    def GetBusStop(self, address):

        #address = address  # 'Gamex, Makutano Road, Jitegemee, Mabibo, Ubungo Municipal, Dar es Salaam, Coastal Zone, 21493, Tanzania'
        geocode = self.map_client.geocode(address=address)
        (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

        search_string = 'Bus Company'
        distance = self.miles_to_meters(2)
        business_list = []

        response = self.map_client.places_nearby(
            location=(lat, lng),
            keyword=search_string,
            radius=distance
        )

        business_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')

        while next_page_token:
            time.sleep(2)
            response = self.map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance,
                page_token=next_page_token
            )
            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

        for i in range(10):
            self.name_stop.append(business_list[i]["name"])
            cord = f'{business_list[i]["geometry"]["location"]["lat"]},{business_list[i]["geometry"]["location"]["lng"]}'.strip()
            self.cord_stop.append(cord)
            print(business_list[i]["name"])
            print(cord)
