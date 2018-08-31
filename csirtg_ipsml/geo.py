import os
import geoip2.database

DB_SEARCH_PATHS = [
    './',
    '/var/lib/GeoIP',
    '/usr/local/share/GeoIP',
    '/usr/local/var/GeoIP',
    '/usr/share/GeoIP',
]

DB_PATH = 'GeoLite2-City.mmdb'
ASN_DB_PATH = 'GeoLite2-ASN.mmdb'

asndb = None
citydb = None

for p in DB_SEARCH_PATHS:
    if os.path.isfile(os.path.join(p, DB_PATH)):
        citydb = geoip2.database.Reader(os.path.join(p, DB_PATH))
        break

for p in DB_SEARCH_PATHS:
    if os.path.isfile(os.path.join(p, ASN_DB_PATH)):
        asndb = geoip2.database.Reader(os.path.join(p, ASN_DB_PATH))
        break
