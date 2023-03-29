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
        if data:
            Fire_Base.bus_stop = data['BusStops']
            Fire_Base.track = data['Tracker']
            Fire_Base.detail = data['Details']
            Fire_Base.current_pos = data['current_location']

            return True
        else:

            return False


