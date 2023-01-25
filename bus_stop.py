from database_ft import DatabaseFetch as DF

import requests
from bs4 import BeautifulSoup


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



