import datetime

import requests
from bs4 import BeautifulSoup


# enter city name


class BusLists:
    all_cities = {"68": "ARUSHA", "214": "BABATI", "215": "BAGAMOYO", "340": "BAHI", "216": "BARIADI", "514": "BASUTU",
                  "634": "BEREKO", "217": "BIHARAMULO", "367": "BOMA NG'OMBE", "211": "BOMA\/HAI", "511": "BONGA",
                  "733": "BORENGA", "718": "BUGOJI", "467": "BUGUNDA", "433": "BUHEMBA", "715": "BUKIMA",
                  "318": "BUKOBA",
                  "510": "BUKULU", "597": "BUKUNDI", "662": "BULAMATA", "432": "BUMANGI", "320": "BUNDA",
                  "418": "BUSEKELA",
                  "430": "BUTIAMA", "445": "BWAI", "384": "BWANGA", "394": "Bwiko", "213": "CHALINZE", "645": "CHAMAI",
                  "385": "CHATO", "391": "Chekereni", "365": "CHEMBA", "507": "CHIKUYU", "648": "CHINANGALI",
                  "548": "CHUNYA", "513": "CMSC", "218": "DAR ES SALAAM", "512": "DAWARI", "472": "DIGODIGO",
                  "212": "DODOMA", "651": "DOSIDOSI", "329": "DUMILA", "470": "ENGARUKA", "652": "ENGESERO",
                  "219": "GAIRO",
                  "220": "GEITA", "442": "GENTAMOME", "530": "GUMANGA", "455": "GUSUI", "679": "GUTA", "398": "HALE",
                  "223": "HANDENI", "515": "HAYDOM", "372": "HEDARU", "224": "HIMO", "646": "HOGORO", "435": "HUNYARI",
                  "532": "IBAGA", "225": "IFAKARA", "482": "IFUNDA", "221": "IGAWA", "368": "IGUGUNO", "107": "IGUNGA",
                  "451": "IKIZU", "440": "ILAMBA", "551": "ILONGERO", "484": "INYONGA", "486": "IPOLE", "229": "IRAMBA",
                  "302": "IRINGA", "502": "ISAKA", "547": "ISANGAWANA", "349": "ISMANI", "533": "ISUNA", "378": "ITAJA",
                  "465": "ITETE", "304": "ITIGI", "588": "ITILIMA", "350": "IZAZI", "632": "KABILA", "519": "KABUKU",
                  "719": "KABURABURA", "582": "KAGONGWA", "230": "KAHAMA", "231": "KAKONKO", "407": "KAKUKURU",
                  "546": "KAMBI KATOTO", "564": "KANG'ATA", "753": "KANYARA", "540": "KARANGASI", "235": "KARATU",
                  "411": "KASAMWA", "584": "KASOLI", "338": "KASULU", "336": "KATESHI", "383": "KATORO",
                  "710": "KELEMA",
                  "449": "KEMGESI", "439": "KENYAMONTA", "361": "KIA", "376": "KIABAKARI", "256": "KIBAHA",
                  "332": "KIBAIGWA", "388": "KIBAONI", "408": "KIBARA", "728": "KIBONDO", "574": "KIBRASHI",
                  "516": "KIDARAFA", "261": "KIDATU", "563": "KIDEREKO", "258": "KIGOMA", "542": "KIGWA",
                  "550": "KIJOTA",
                  "308": "KIJUNGU", "446": "KILOLELI", "252": "KILOMBERO", "259": "KILOSA", "360": "KILWA",
                  "573": "KIMBE",
                  "508": "KINTINKU", "339": "KIOMBOI", "364": "KIRANJERANGE", "390": "Kisangara", "450": "KISANGWA",
                  "636": "KISIMA", "404": "KISORYA", "529": "KISULUIGA", "526": "KITETO", "531": "KIZIGO",
                  "633": "KOLO",
                  "327": "KONDOA", "428": "KONGOTO", "293": "KOROGWE", "717": "KUSENYI", "521": "KWA DELO",
                  "566": "KWA LUGURU", "568": "KWEDIBOMA", "416": "KWIKUBA", "567": "KWINJI", "427": "KYAGATA",
                  "703": "KYAWAZALU", "315": "KYELA", "675": "LALAGO", "237": "LAMADI", "392": "Lembeni",
                  "238": "LINDI",
                  "456": "LINGW'ANI", "424": "LOLIONDO", "422": "LUHAFE", "410": "LULEMBELA", "505": "LUNAZI",
                  "503": "LUNZEWE", "464": "LUPILO", "504": "LUSAUNGA", "316": "LUSHOTO", "479": "MABESHI",
                  "459": "MABURI",
                  "362": "MACHAME RD", "454": "MACHOMWELU", "241": "MAFINGA", "257": "MAFISA", "581": "MAGANZO",
                  "387": "MAGARINI", "243": "MAGU", "366": "MAGUGU", "615": "MAHAHA", "244": "MAHENGE",
                  "441": "MAJI MOTO",
                  "246": "MAKAMBAKO", "373": "MAKANYA", "248": "MAKONGOROSI", "255": "MAKUTANO", "334": "MAKUYUNI",
                  "397": "Makuyuni-Mombo", "400": "MALAMPAKA", "345": "MALINYI", "434": "MALIWANDA", "369": "MALUGA",
                  "706": "MANEKE", "396": "Manga", "326": "MANYONI", "381": "MARANGU", "425": "MASANZA KONA",
                  "457": "MASINKI", "570": "MASISTA", "409": "MASUMBWE", "426": "MASURURA", "401": "MASWA",
                  "713": "MAUNDO",
                  "704": "MAYANI", "330": "MBANDE", "309": "MBEYA", "541": "MBUMBULI", "395": "Mbuta", "374": "MBUYUNI",
                  "375": "MDORI", "249": "MEATU", "393": "Mgagao", "543": "MGANDU", "415": "MGANGO", "386": "MGANZA",
                  "413": "MGETA", "331": "MIGOLI", "436": "MIKOMALILO", "251": "MIKUMI", "353": "MINJINGU",
                  "253": "MISIGIRI", "254": "MISUNGWI", "382": "MKATA", "554": "MKOKA", "399": "Mkumbara",
                  "730": "MLALO",
                  "716": "MLANGI", "640": "MLOWA", "431": "MLYAZA", "371": "MOMBO", "522": "MONDO", "572": "MONDULI",
                  "262": "MOROGORO", "263": "MOSHI", "313": "MPANDA", "523": "MRIJO", "288": "MSATA", "356": "MTAMA",
                  "544": "MTENDENI", "335": "MTERA", "466": "MTIMBILA", "552": "MTINKO", "468": "MTO WA MBU",
                  "414": "MUGANZA", "265": "MUGUMU", "266": "MUHEZA", "267": "MULEBA", "268": "MUSOMA",
                  "325": "MVOMERO",
                  "347": "MVUMI", "380": "MWAHU", "600": "MWAKASUMBI", "528": "MWANDO", "599": "MWANDOYA",
                  "282": "MWANGA",
                  "517": "MWANGA\/", "84": "MWANZA", "587": "MWIGUMBI", "283": "MWIKA", "592": "NAKO",
                  "475": "NAMANYERE",
                  "351": "NANGURUKURU", "527": "NDUGUTI", "674": "NDUGUTI", "565": "NEGERO", "269": "NEWALA",
                  "471": "NGARASERO", "612": "NGHAYA", "586": "NGULIATI", "322": "NJIA PANDA-HIMO", "323": "NJOMBE",
                  "525": "NJORO", "518": "NKALANKALA", "463": "NKUNGI", "598": "NYAHAA", "412": "Nyakaboja",
                  "337": "NYAKANAZI", "419": "NYAKITONO", "611": "NYAMONGO", "447": "NYAMSWA", "453": "NYANG'ALANGANA",
                  "348": "NYANG'OLO", "661": "NYARUGUSU", "377": "NYASHIMO", "752": "NYEHUNGE", "150": "NZEGA",
                  "520": "PAHI", "729": "POLI", "549": "PUMBULI", "275": "RAMADI", "458": "REMUNG'ORORI",
                  "228": "RIBIRASHI", "280": "ROMBO", "389": "RUNAZI", "545": "RUNGWA", "402": "RUNZEWE",
                  "354": "SADALA",
                  "379": "SAGARA", "421": "SALAGANA", "452": "SALAMA A", "663": "SALANDA", "284": "SAME",
                  "474": "SAMUNGE",
                  "437": "SANZATI", "286": "SEGERA", "469": "SELELA", "285": "SENGEREMA", "352": "SHELUI",
                  "86": "SHINYANGA", "303": "SIKONGE", "438": "SILORI SIMBA", "92": "SINGIDA", "306": "SIRARI",
                  "363": "SOMANGA", "649": "SONGA", "647": "SONGAMBELE", "571": "SONGE", "344": "SONGWE", "370": "SONI",
                  "506": "SORYA", "307": "SUMBAWANGA", "312": "TABORA", "289": "TANDAHIMBA", "290": "TANGA",
                  "291": "TARIME", "705": "TEGELUKA", "292": "TINDE", "294": "TUNDUMA", "539": "TURA", "295": "TURIANI",
                  "406": "UKARA", "405": "UKEREWE", "296": "URAMBO", "702": "USA RIVER", "297": "USHIROMBO",
                  "537": "USINGE", "300": "UVINZA", "473": "WASO", "429": "WEGERO", "650": "ZOISA"}
    bus_names = []
    routes = []
    license = []
    price = []
    seats = []

    def get_city_code(self, city_name):
        for code, name in self.all_cities.items():
            if name.lower() == city_name.lower():
                return code
        return None

    def two_morrow(self):
        today = datetime.datetime.today()

        now_day = today + datetime.timedelta(days=2)

        day = now_day.day
        month = now_day.month
        year = now_day.year

        two_day = f"{day}-{month}-{year}"

        return two_day

    def get_bus_list(self, from_city, to_city):
        idfrom = self.get_city_code(from_city)
        idto = self.get_city_code(to_city)
        # creating url and requests instance
        url = f"https://www.busbora.co.tz/search-buses?from={idfrom}&to={idto}&date={self.two_morrow()}&srcType=1"
        html = requests.get(url).content

        # getting raw data
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find_all('div', attrs={'class': 'bus_name'})
        price = soup.find_all('h3', attrs={'class': 'price'})
        seats = soup.find_all("p", attrs={'class': 'mb-2 d-block'})


        for p in price:
            BusLists.price.append(p.text)
        for s in seats:
            BusLists.seats.append(s.text)
        names = [elem.text.strip() for elem in name]
        BusLists.bus_names = [n.split('\n')[0] for n in names]
        BusLists.routes = [n.split('\n')[1] for n in names]
        BusLists.license = [n.split('\n')[2] for n in names]
