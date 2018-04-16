import os
import pygeoip

DB_SEARCH_PATHS = [
    './',
    '/usr/share/GeoIP',
    '/usr/local/share/GeoIP'
]

DB_FILE = 'GeoLite2-City.mmdb'

ASN_DB_PATH = 'GeoIPASNum.dat'
ASN_DB_PATH2 = 'GeoLiteASNum.dat'
CITY_DB_PATH = 'GeoLiteCity.dat'

asndb = None
citydb = None

for p in DB_SEARCH_PATHS:
    if os.path.isfile(os.path.join(p, CITY_DB_PATH)):
        citydb = pygeoip.GeoIP(os.path.join(p, CITY_DB_PATH), pygeoip.MMAP_CACHE)
        break

for p in DB_SEARCH_PATHS:
    if os.path.isfile(os.path.join(p, ASN_DB_PATH2)):
        asndb = pygeoip.GeoIP(os.path.join(p, ASN_DB_PATH2), pygeoip.MMAP_CACHE)
        break