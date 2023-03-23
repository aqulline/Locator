from kivy.base import EventLoop
from kivy.properties import NumericProperty, StringProperty, DictProperty, ListProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.clock import mainthread
from plyer import gps
from kivy.utils import platform

from beem import sms as SM
from database_ft import DatabaseFetch as DF
from bus_stop import GoogleBusStop as BS
from wearth import Weather as WE
from locations import Location as LC

from kivy.core.window import Window
from kivy.clock import Clock
from kivy import utils
from kivy_garden.mapview import MapMarker, MapMarkerPopup



Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class RowCard(MDCard):
    icon = StringProperty("")
    name = StringProperty("")


class MainApp(MDApp):
    size_x, size_y = Window.size
    counter_bus_stop = 0
    gps_location = StringProperty("")
    gps_status = StringProperty("")

    # LOCATION
    city = StringProperty("------------------")
    region = StringProperty("------------------")
    city_district = StringProperty("------------------")
    sub_ward = StringProperty("------------------")
    sub_urb = StringProperty("------------------")
    road = StringProperty("------------------")

    # screen
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # Map
    lat, lon = NumericProperty(-6.8059668), NumericProperty(39.2243981)
    gppp = []
    zoom = NumericProperty(15)
    weather = StringProperty("")
    w_icon1 = StringProperty("")
    w_icon2 = StringProperty("")
    location_name_to = StringProperty("Select Location")
    location_name_from = StringProperty("")

    # loc
    cordinates = ListProperty([lat, lon])

    address = StringProperty("")

    # database
    regions = DictProperty(DF.reg_list(DF()))

    def on_start(self):
        self.keyboard_hooker()
        self.gps_init()
        self.location()
        self.weath()

        """
            KEYBOARD HOOKERS
        
        """

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

        """
            WEATHER FUNCTIONS
        """

    def weath(self):
        self.weather = WE.current_wth(WE(), self.location_name_from)[0]
        let1, let2 = self.weather[0], self.weather[1]
        self.w_icon1 = f"numeric-{let1}"
        self.w_icon2 = f"numeric-{let2}"

        """
        BUS STATION LOCATION
        """

    def add_item(self):
        names = BS.name_stop
        cor = BS.cord_stop
        for i in names:
            pos = names.index(i)
            self.root.ids.customers.data.append(
                {
                    "viewclass": "RowCard",
                    "icon": "google-maps",
                    "name": i,
                    "id": cor[pos]
                }
            )
            self.root.ids.customer.data.append(
                {
                    "viewclass": "RowCard",
                    "icon": "google-maps",
                    "name": i,
                    "id": cor[pos]
                }
            )

    def bus_station(self):
        if self.counter_bus_stop == 0:
            BS.GetBusStop(BS(), self.address)

            cor = BS.cord_stop
            station_name = BS.name_stop

            map = self.root.ids.map

            for i in cor:
                pos = cor.index(i)
                lat, lon = i.strip().split(",")
                mark = MapMarkerPopup(lat=lat, lon=lon)
                mark.add_widget(MDRaisedButton(text=station_name[pos]))
                map.add_widget(mark)
                map.center_on(float(lat), float(lon))
                self.zoom = 10
            self.add_item()
            self.counter_bus_stop = 1

    def location(self):
        from geopy.geocoders import Nominatim

        geolocator = Nominatim(user_agent="geoapiExercises")

        location = geolocator.reverse(str(self.lat) + "," + str(self.lon))

        self.fetch_location()

    def callback_for_menu_items(self, y, z, var):
        toast(y)
        self.data_name = y
        self.data_icon = z

        print("hello")

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

    def bus_stop_specific(self, data):
        map = self.root.ids.map
        lat, lon = data.strip().split(",")
        map.add_widget(MapMarker(lat=lat, lon=lon))
        map.center_on(float(lat), float(lon))

    """
            MY LOCATION FUNCTIONS
    """

    def fetch_location(self):

        cordinates = [self.lat, self.lon]
        LC.save_data(LC(), cordinates)
        self.city = LC.get_spec_add(LC(), "city")

        self.region = LC.get_spec_add(LC(), "region")

        self.city_district = LC.get_spec_add(LC(), "city_district")

        self.sub_ward = LC.get_spec_add(LC(), "subward")

        self.sub_urb = LC.get_spec_add(LC(), "suburb")

        self.road = LC.get_spec_add(LC(), "road")

        self.address = LC.get_address(LC(), cordinates)["display_name"]

    def send_txt(self, phone, sms):

        if SM.send_sms(phone, sms):
            toast("send successful")
        else:
            toast("check number!")

    """
    
        screen functions
    
    """

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


        """
                                        GPS INTERPRETATION
        
        """

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)

    def gps_init(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)

        except NotImplementedError:
            import traceback
            traceback.print_exc()
            gps_status = 'GPS is not implemented for your platform'

            return gps_status

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)



    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

        self.lat = float(kwargs["lat"])
        self.lon = float(kwargs["lon"])
        self.location()
        self.weath()



    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)



    def build(self):
        pass


MainApp().run()
