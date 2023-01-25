from kivy.core.window.window_x11 import EventLoop
from kivy.properties import NumericProperty, StringProperty, DictProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from database_ft import DatabaseFetch as DF
from wearth import Weather as WE
from kivy.core.window import Window
from kivy.clock import Clock
from kivy import utils
from kivy_garden.mapview import MapView, MapMarker

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class MainApp(MDApp):
    size_x, size_y = Window.size

    # screen
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # Map
    lat = NumericProperty(-6.8235)
    lon = NumericProperty(39.2695)
    gppp = []
    zoom = NumericProperty(15)
    weather = StringProperty("")
    w_icon1 = StringProperty("")
    w_icon2 = StringProperty("")
    location_name_to = StringProperty("Select Location")
    location_name_from = StringProperty("")

    # database
    regions = DictProperty(DF.reg_list(DF()))

    def on_start(self):
        self.keyboard_hooker()
        self.location()
        self.weath()

    def weath(self):
        self.weather = WE.current_wth(WE(), self.location_name_from)[0]
        let1, let2 = self.weather[0], self.weather[1]
        self.w_icon1 = f"numeric-{let1}"
        self.w_icon2 = f"numeric-{let2}"

    def location(self):
        import geocoder
        g = geocoder.ip('me')
        print(g.latlng)

        self.lat, self.lon = g.latlng
        # import module
        from geopy.geocoders import Nominatim

        # initialize Nominatim API
        geolocator = Nominatim(user_agent="geoapiExercises")

        # Latitude & Longitude input

        location = geolocator.reverse(str(self.lat) + "," + str(self.lon))

        address = location.raw['address']

        # traverse the data
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        code = address.get('country_code')
        zipcode = address.get('postcode')

        self.location_name_from = city

    def keyboard_hooker(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)

    def callback_for_menu_items(self, y, z, var):
        toast(y)
        self.data_name = y
        self.data_icon = z

        if var == "to":
            self.location_name_to = y
        else:
            self.location_name_from = "Dar Es salaam"

    def category_sheet(self, data, var):
        bottom_sheet_menu = MDListBottomSheet()
        vimbweta = data
        count = 1
        for i in vimbweta.items():
            bottom_sheet_menu.add_item(
                i[0],
                lambda x, y=i[0], z=i[1]: self.callback_for_menu_items(y, z, var),
                icon=i[1],
            )
            count += 1

        bottom_sheet_menu.radius_from = 'top'
        bottom_sheet_menu.open()

    def build(self):
        pass


MainApp().run()
