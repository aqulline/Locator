import json


class DatabaseFetch:

    def reg_list(self):
        with open("database/regions.json") as region:
            reg = json.load(region)

            return reg

    def city_links(self):
        with open("database/city_links.json") as region:
            reg = json.load(region)

            return reg

