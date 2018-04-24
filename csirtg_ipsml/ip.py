
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import numpy as np
import sys
import ipaddress
import arrow
from pprint import pprint
import re

from sklearn import preprocessing
from csirtg_ipsml.geo import asndb, citydb

me = os.path.dirname(__file__)
CC_FILE = "%s/../data/cc.txt" % me

if os.path.exists(os.path.join(sys.prefix, 'csirtg_ipsml', 'data', 'cc.txt')):
    CC_FILE = os.path.join(sys.prefix, 'csirtg_ipsml', 'data', 'cc.txt')

elif os.path.exists(os.path.join('usr', 'local', 'csirtg_ipsml', 'data', 'cc.txt')):
    CC_FILE = os.path.join('usr', 'local', 'csirtg_ipsml', 'data', 'cc.txt')

elif os.path.exists(("%s/data/cc.txt" % me)):
    CC_FILE = "%s/data/cc.txt" % me

CC = []

TZ_FILE = "%s/../data/timezones.txt" % me

if os.path.exists(os.path.join(sys.prefix, 'csirtg_ipsml', 'data', 'timezones.txt')):
    TZ_FILE = os.path.join(sys.prefix, 'csirtg_ipsml', 'data', 'timezones.txt')

elif os.path.exists(os.path.join('usr', 'local', 'csirtg_ipsml', 'data', 'timezones.txt')):
    TZ_FILE = os.path.join('usr', 'local', 'csirtg_ipsml', 'data', 'timezones.txt')

elif os.path.exists(("%s/data/timezones.txt" % me)):
    TZ_FILE = "%s/data/timezones.txt" % me

TZ = []

with open(CC_FILE) as F:
    for l in F.readlines():
        l = l.strip("\n")
        l = l.split(";")
        CC.append(l[1])

with open(TZ_FILE) as F:
    for l in F.readlines():
        TZ.append(l.rstrip("\n"))

cc_data = preprocessing.LabelEncoder()
cc_data.fit(CC)

tz_data = preprocessing.LabelEncoder()
tz_data.fit(TZ)


def extract_features(indicator, ts):
    # week?
    try:
        asn = asndb.asn(indicator)
    except:
        asn = None

    if asn:
        asn = asn.autonomous_system_number

    if asn is None:
        asn = 0

    try:
        city = citydb.city(indicator)
    except:
        city = None

    if city is None:
        yield [ts, indicator, 0, 0, 'NA', 'NA', 0]

    else:
        if not asn:
            asn = 0

        tz = city.location.time_zone
        if tz is None:
            tz = 'NA'

        cc = city.country.iso_code
        if cc is None:
            cc = 'NA'

        # hour, src, dest, client, tz, cc, success
        yield [ts, indicator, int(city.location.latitude), int(city.location.longitude), tz, cc, int(asn)]


def fit_features(i):
    for l in i:
        try:
            l[1] = int(ipaddress.ip_address(l[1]))
        except:
            l[1] = int(ipaddress.ip_address(l[1].decode('utf-8')))

        l[4] = tz_data.transform([l[4]])[0]
        l[5] = cc_data.transform([l[5]])[0]

        yield l


def predict(i, ts, classifier):
    feats = extract_features(i, ts)
    feats = list(fit_features(f for f in feats))
    feats = np.array(feats, dtype=int)
    return classifier.predict(feats)


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                  $ cat data/blacklist.csv | python csirtg_ipsml/ip.py > tmp/blacklist.csv
                  $ cat data/whitelist.csv | python csirtg_ipsml/ip.py --good > tmp/whitelist.csv
                  $ cat tmp/blacklist.csv tmp/whitelist.csv | gshuf > tmp/training.csv
                  $ cat data/training.csv | csirtg-ipsml -i 128.205.1.1
                '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-ipsml/ip.py'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('--good', action="store_true", default=False)

    args = p.parse_args()

    for l in sys.stdin:
        l = l.rstrip("\n")
        l = l.rstrip("\r")
        l = re.sub('"', '', l)
        l = l.split(',')

        # ff = [f for f in extract_features(l[1], ts=l[0])]
        # ff = ff[0]
        ts = arrow.get(l[0])
        l[0] = ts.strftime('%H')

        if args.good:
            l.append(0)
        else:
            l.append(1)

        l = [str(f) for f in l]
        out = ','.join(l)
        print(out)


if __name__ == '__main__':
    main()
