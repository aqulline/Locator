import random
import string


class Fire_Base:
    bus_stop = {}
    detail = {}
    track = {}
    current_pos = {}

    def get_bus_id(self, number):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                    initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                    ref = db.reference('LocatorDriver').child("BusId").child(number)

                    return ref.get()
            except:

                return False

    def fetch(self, number):
        data = self.get_bus_id(number)
        print("data=", data)
        if data:
            Fire_Base.bus_stop = data['BusStops']
            Fire_Base.track = data['Tracker']
            Fire_Base.detail = data['Details']
            Fire_Base.current_pos = data['current_location']

            return True
        else:

            return False

    def notifier(self, phone, location, user_phone):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("BusId").child(phone).child("Notifier").child(location).child(
                    user_phone)
                ref.set({
                    "phone": user_phone,
                })

    def track_loc(self, idd, lan, lon):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("Self_track").child(idd)
                ref.set({
                    "lat": lan,
                    "lon": lon
                })

    def get_loc(self, idd):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("Self_track").child(idd)

                return ref.get()

    def id_generator(self):

        num = string.digits
        letter = string.ascii_letters

        rr = num + letter

        z = random.choice(rr)
        a = random.choice(rr)
        v = random.choice(rr)
        f = random.choice(rr)
        t = random.choice(rr)
        w = random.choice(rr)

        return z + a + v + f + t + w


Fire_Base.track_loc(Fire_Base(), "02A6wO", 45.92847, -72.07159)
