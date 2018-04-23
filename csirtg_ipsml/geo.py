import os
import pygeoip

DB_SEARCH_PATHS = [
    './',
    '/usr/share/GeoIP',
    '/usr/local/share/GeoIP',
]

DB_PATH = 'GeoLite2-City.mmdb'
ASN_DB_PATH = 'GeoLite2-ASN.mmdb'

asndb = None
citydb = None

for p in DB_SEARCH_PATHS:
    if os.path.isfile(os.path.join(p, DB_PATH)):
        citydb = pygeoip.GeoIP(os.path.join(p, DB_PATH), pygeoip.MMAP_CACHE)
        break

for p in DB_SEARCH_PATHS:
    if os.path.isfile(os.path.join(p, ASN_DB_PATH)):
        asndb = pygeoip.GeoIP(os.path.join(p, ASN_DB_PATH), pygeoip.MMAP_CACHE)
        break