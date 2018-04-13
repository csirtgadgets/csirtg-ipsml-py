#!/usr/bin/python

import sys
import os
import pygeoip
import arrow
from pprint import pprint
import csv

DB_SEARCH_PATHS = [
    './',
    '/usr/share/GeoIP',
    '/usr/local/share/GeoIP'
]

ENABLE_FQDN = os.getenv('CIF_GATHERER_GEO_FQDN')
DB_FILE = 'GeoLite2-City.mmdb'
DB_PATH = os.environ.get('CIF_GEO_PATH')

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

with open(sys.argv[1]) as FILE:
    for l in FILE.readlines():
        if l.startswith('#'):
            continue

        l = l.rstrip("\n")
        l = l.rstrip('"')
        l = l.lstrip('"')
        ts, indicator, = l.split(',')
        ts = arrow.get(ts).hour
        # week?
        asn = asndb.asn_by_addr(indicator)
        #pprint(asn)
        if asn:
            asn = asn.split()[0]
            _, asn = asn.split('AS')

        if asn is None:
            asn = 0

        city = citydb.record_by_addr(indicator)
        # pprint(indicator)
        # pprint(city)

        if not city:
            print("{},{},{},{},{},{},{},{}".format(
                ts,
                indicator,
                '0',
                '0',
                "NA",
                "NA",
                "0",
                '0'
            ))
            continue

        # hour, src, dest, client, tz, cc, success
        print("{},{},{},{},{},{},{},{}".format(
            ts,
            indicator,
            int(city['latitude']),
            int(city['longitude']),
            city['time_zone'],
            city['country_code'],
            asn,
            '0'
        ))
