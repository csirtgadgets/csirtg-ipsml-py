
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import numpy as np
from pprint import pprint
import sys
from .geo import asndb, citydb
import ipaddress
from sklearn import preprocessing

me = os.path.dirname(__file__)
CC_FILE = "%s/../data/cc.txt" % me
CC = []


TZ_FILE = "%s/../data/timezones.txt" % me
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


def extract_features(indicator):
    import arrow
    ts = arrow.utcnow()
    ts = arrow.get(ts).hour

    if ',' in indicator:
        indicator, ts = indicator.split(',')
        ts = int(ts)
        # ts = arrow.get(ts).hour

    # week?
    asn = asndb.asn_by_addr(indicator)
    # pprint(asn)
    if asn:
        asn = asn.split()[0]
        _, asn = asn.split('AS')

    if asn is None:
        asn = 0

    city = citydb.record_by_addr(indicator)
    # pprint(indicator)
    # pprint(city)

    if city is None:
        yield [ts, indicator, 0, 0, 'NA', 'NA', 0]

    else:
        if not asn:
            asn = 0

        tz = city['time_zone']
        if tz is None:
            tz = 'NA'

        cc = city['country_code']
        if cc is None:
            cc= 'NA'

        # hour, src, dest, client, tz, cc, success
        yield [ts, indicator, int(city['latitude']), int(city['longitude']), tz, cc, int(asn)]


def fit_features(i):
    for l in i:
        l[1] = int(ipaddress.ip_address(l[1]))

        l[4] = tz_data.transform([l[4]])[0]
        l[5] = cc_data.transform([l[5]])[0]

        yield l


def predict(i, classifier):
    feats = extract_features(i)
    feats = list(fit_features(f for f in feats))
    pprint(feats)
    feats = np.array(feats, dtype=int)
    return classifier.predict(feats)


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $ cat data/training.csv | csirtg-ipsml -i 128.205.1.1
                '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-ipsml'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('--good', action="store_true", default=False)

    args = p.parse_args()

    for l in sys.stdin:
        l = l.strip('"')
        l = l.split(',')

        ff = extract_features(l)

        if args.good:
            ff.append(0)
        else:
            ff.append(1)

        ff = [str(f) for f in ff]
        out = ','.join(ff)
        print(out)


if __name__ == '__main__':
    main()
