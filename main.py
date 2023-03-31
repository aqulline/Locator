import threading
import time

from kivy.base import EventLoop
from kivy.properties import NumericProperty, StringProperty, DictProperty, ListProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.clock import mainthread
from kivymd.uix.tab import MDTabsBase
from plyer import gps
from kivy.utils import platform

from beem import sms as SM
from database_ft import DatabaseFetch as DF
from bus_stop import GoogleBusStop as BS
from wearth import Weather as WE
from locations import Location as LC
from bus_list import BusLists as BL
from fire_base import Fire_Base as FB

from kivy.core.window import Window
from kivy.clock import Clock
from kivy import utils
from kivy_garden.mapview import MapMarker, MapMarkerPopup

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class Tab(MDBoxLayout, MDTabsBase):
    pass


class Emerge(MDBoxLayout):
    pass


class BusInfo(MDBoxLayout):
    name = StringProperty("")
    route = StringProperty("")
    lcn = StringProperty("")
    price = StringProperty("")
    seats = StringProperty("")


class RowCard(MDCard):
    icon = StringProperty("")
    name = StringProperty("")


class MainApp(MDApp):
    size_x, size_y = Window.size
    counter_bus_stop = 0
    gps_location = StringProperty("")
    gps_status = StringProperty("")
    url_bus = StringProperty("")
    thread = None
    prgres = StringProperty("0")
    bus_prog = StringProperty("0")

    # LOCATION
    city = StringProperty("------------------")
    region = StringProperty("------------------")
    city_district = StringProperty("------------------")
    sub_ward = StringProperty("------------------")
    sub_urb = StringProperty("------------------")
    road = StringProperty("------------------")

    # Tracker
    bus_stop = DictProperty({})
    detail = DictProperty({})
    track = DictProperty({})
    current_pos = DictProperty({})

    # Tracker.tracker
    user_phone = StringProperty("")
    user_track_location = StringProperty("")
    Bname = StringProperty("")
    Bnumber = StringProperty("")
    Bicon = StringProperty("")
    Bbool = BooleanProperty(False)
    bus_current_loc = StringProperty("")
    bus_prev_loc = StringProperty("")
    bus_lat, bus_lon = NumericProperty(0), NumericProperty(0)

    # Tracker.location
    Bcity = StringProperty("")
    Bregion = StringProperty("")
    B_city_district = StringProperty("")
    B_sub_ward = StringProperty("")
    B_sub_urb = StringProperty("")
    Broad = StringProperty("")

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
        """self.keyboard_hooker()
        self.plat_check()"""
        Clock.schedule_once(lambda x: self.starta(), .1)

        """
            KEYBOARD HOOKERS
        
        """

    @mainthread
    def progress_watch(self, value):
        print(value.value)
        self.prgres = str(value.value)
        if value.value == 100:
            Clock.schedule_once(lambda x: self.screen_capture("home"), .6)

    def starta(self):
        prg = self.root.ids.prg
        prg.value = 3
        self.progress_watch(prg)
        self.gps_init()
        self.thread = threading.Thread(target=self.coleer)
        self.thread.start()

    def coleer(self, *args):
        self.keyboard_hooker()
        self.plat_check()

    def plat_check(self, ):
        if platform == "android":
            self.location()
            self.weath()
        else:
            self.location()
            self.weath()

    def keyboard_hooker(self, *args):
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
            self.back_page()
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    def back_page(self):

        if platform == "android":
            from beem import call as CL
            print("step 4")
            if CL.Actions.quit_screens(CL.Actions()):
                print("step 4.1")
                Clock.schedule_once(self.quit_screen, 0)

    @mainthread
    def quit_screen(self, *args):
        print("step 5")
        app = MDApp.get_running_app()
        app.root.switch_screen()
        print("step 5.1")

        """
            WEATHER FUNCTIONS
        """

    def weath(self):
        prg = self.root.ids.prg
        prg.value = 80
        self.progress_watch(prg)
        self.weather = WE.current_wth(WE(), self.location_name_from)[0]
        let1, let2 = self.weather[0], self.weather[1]
        self.w_icon1 = f"numeric-{let1}"
        self.w_icon2 = f"numeric-{let2}"

        prg = self.root.ids.prg
        prg.value = 100
        self.progress_watch(prg)

        """        if platform == "android":
            self.stop()"""

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
        bst = self.root.ids.bst
        bst.value = 100

    def bus_station(self, *args):
        if self.counter_bus_stop == 0:
            bst = self.root.ids.bst
            bst.value = 65
            time.sleep(2)
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
            bst = self.root.ids.bst
            bst.value = 76
            time.sleep(2)
            self.add_item()
            self.counter_bus_stop = 1

    def location(self):
        from geopy.geocoders import Nominatim

        geolocator = Nominatim(user_agent="geoapiExercises")

        location = geolocator.reverse(str(self.lat) + "," + str(self.lon))

        prg = self.root.ids.prg
        prg.value = 25
        self.progress_watch(prg)

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

        prg = self.root.ids.prg
        prg.value = 50
        self.progress_watch(prg)

    def send_txt(self, phone, sms):

        if SM.send_sms(phone, sms):
            toast("send successful")
        else:
            toast("check number!")

    """
        BUS LIST FUNCTION
    """

    def get_list(self, city_name):
        BL.get_bus_list(BL(), self.city, city_name)
        print("pass")
        self.add_bus()
        print("done")

    def add_bus(self):
        names = BL.bus_names
        print(names, "name")
        self.url_bus = BL.link
        routes = BL.routes
        license = BL.license
        price = BL.price
        seats = BL.seats
        self.root.ids.bus_data.data = {}
        if not names:
            self.root.ids.bus_data.data.append(
                {
                    "viewclass": "BusInfo",
                    "name": "No Cars Yet!",
                    "route": "",
                    "lcn": "",
                    "price": "",
                    "seats": ""
                }
            )
        else:
            for i in names:
                pos = names.index(i)
                self.root.ids.bus_data.data.append(
                    {
                        "viewclass": "BusInfo",
                        "name": i,
                        "route": routes[pos],
                        "lcn": license[pos],
                        "price": price[pos],
                        "seats": f"seats available {seats[pos]}"
                    }
                )

    def view_page(self, link):
        from beem import call as CL

        CL.Actions.url = link

        import webbrowser
        webbrowser.open(link)

    """
            EMERGENCY
    """

    def call_emergency(self, phone):
        from beem import call as CL

        CL.Actions.call(CL.Actions(), phone)

    """"
            OPTIMIZATIONS FUNCTIONS
    """

    def bus_monitor(self, *args):
        print("caled")
        if self.bus_prog == "60":
            self.bus_station()
            Clock.unschedule(self.bus_monitor)

    def bus_station_caller(self):
        if self.counter_bus_stop == 0:
            Clock.schedule_interval(self.bus_monitor, .1)
            bst = self.root.ids.bst
            bst.value = 10
            self.bus_prog = str(bst.value)
            Clock.schedule_once(lambda x: self.bus(), .1)

    def bus(self):
        bst = self.root.ids.bst
        bst.value = 29
        self.bus_prog = str(bst.value)
        self.thread = threading.Thread(target=BS.GetBusStop, args=(BS(), self.address))
        self.thread.start()
        self.thread.join()
        bst = self.root.ids.bst
        bst.value = 60
        self.bus_prog = str(bst.value)

    """
            TRACKING FUNCTIONS
    
    """

    def fetch(self, Pnumber):

        if FB.fetch(FB(), Pnumber):
            self.bus_stop = FB.bus_stop
            self.detail = FB.detail
            self.track = FB.track
            self.current_pos = FB.current_pos
            layout = self.root.ids.bus_detail
            bus_layout = Emerge()
            bus_layout.pos_hint = {"center_x": .5, "center_y": .9}
            self.Bname = self.detail['car_name']
            self.Bnumber = self.detail['car_plate_number']
            self.bus_current_loc, self.bus_prev_loc = self.current_pos["current"], self.current_pos["prev"]
            self.bus_lat, self.bus_lon = self.track["lat"], self.track["lon"]
            self.Bicon = "arrow-right-drop-circle"
            if not self.Bbool:
                layout.add_widget(bus_layout)
                self.Bbool = True
        else:
            layout = self.root.ids.bus_detail
            bus_layout = Emerge()
            bus_layout.pos_hint = {"center_x": .5, "center_y": .9}
            self.Bname = "Not available"
            self.Bnumber = ""
            self.Bicon = ""
            if not self.Bbool:
                layout.add_widget(bus_layout)
                self.Bbool = True

    def bus_tracker_stop(self):

        Clock.schedule_once(self.bus_tracker_stop_callable, .1)

    tracker_sensor = 0

    def bus_tracker_stop_callable(self, *args):
        data = self.bus_stop
        if self.tracker_sensor == 0:
            self.tracker_sensor = 1
            for i, y in data.items():
                self.root.ids.tracker_stops.data.append(
                    {
                        "viewclass": "Stops",
                        "name": i,
                        "icon": y,
                        "phone": "",
                        "fsize": "16",
                        "pos_x": .27,
                        "pos_y": .5,
                        "isize": "30sp",
                        "call": "android-messages",
                    }
                )
            self.Bfetch_location()

    def Bfetch_location(self):

        cordinates = [self.bus_lat, self.bus_lon]
        LC.save_data(LC(), cordinates)

        self.Bcity = LC.get_spec_add(LC(), "city")

        self.Bregion = LC.get_spec_add(LC(), "region")

        self.B_city_district = LC.get_spec_add(LC(), "city_district")

        self.B_sub_ward = LC.get_spec_add(LC(), "subward")

        self.B_sub_urb = LC.get_spec_add(LC(), "suburb")

        self.Broad = LC.get_spec_add(LC(), "road")

    @mainthread
    def sms_schedule(self, phone):
        user_phone = SM.phone_repr(phone)
        print(user_phone)
        if user_phone:
            FB.notifier(FB(), self.Bnumber, self.user_track_location, user_phone)
        else:
            toast("check your phone number!")

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
                             Permission.ACCESS_FINE_LOCATION, Permission.CALL_PHONE], callback)

    @mainthread
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

    @mainthread
    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    @mainthread
    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

        self.lat = float(kwargs["lat"])
        self.lon = float(kwargs["lon"])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def build(self):
        pass


MainApp().run()
