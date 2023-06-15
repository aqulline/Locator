import requests


class Weather:
    city = "Dar es salaam"

    def get_weather(self, location):
        api_key = "18ae72529c924ea34141ce37862480d4"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = data['main']['temp']

            data = self.kelvin_to_celsius(weather)

            return str(data)
        else:
            return "Weather data not found"

    def kelvin_to_celsius(self, kelvin):
        celsius = kelvin - 273.15
        return int(celsius)
