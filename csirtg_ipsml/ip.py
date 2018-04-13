
from csirtg_domainsml.utils import entropy
import os
import re
import editdistance
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import socket
import sys
import numpy as np
from pprint import pprint
import re
import sys

me = os.path.dirname(__file__)

WHITELIST_PATH = '%s/../data/whitelist.txt' % me
if os.path.exists(os.path.join(sys.prefix, 'csirtg_domainsml', 'data', 'whitelist.txt')):
    WHITELIST_PATH = os.path.join(sys.prefix, 'csirtg_domainsml', 'data', 'whitelist.txt')

with open(WHITELIST_PATH) as F:
    GOOD = set(l.strip('\n') for l in F.readlines())


# see notes.txt
def _is_non_std(u):
    if u.count('.') < 12:
        return -1

    if u.count('.') < 19:
        return 0

    return 1


def _has_subdomains(u):
    uu = re.sub(r'\.[a-zA-Z]{2}$', '', u)
    uu = re.sub(r'^www\.', '', uu)

    if uu.count('.') < 3:
        return -1

    if uu.count('.') < 4:
        return 0

    return 1


def _has_high_entropy(u):
    e = entropy(u)

    if e < 3.1:
        return -1

    if e < 3.5:
        return 0

    return 1


def _has_close_distance(u):
    l = []
    if u in GOOD:
        return -1

    bits = False
    if u.count('.') == 2:
        bits = u.split('.')
        bits.pop(0)
        bits = '.'.join(bits)

    for g in GOOD:
        if u.endswith('.%s' % g):
            return -1

        if bits and bits in g:
            return -1

        d = editdistance.eval(u, g)

        l.append(int(d))

    l.sort()

    if l[0] < 10:
        return 1

    if l[0] < 20:
        return 0

    return -1


def _has_hyphens(u):
    if '-' not in u:
        return -1

    if u.count('-') < 3:
        return 0

    return 1


def _is_secure(u):
    for e in ['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin', 'bank']:
        if re.search(e, u):
            return 1
    return -1


def _is_ip(u):
    try:
        socket.inet_aton(u)
    except Exception:
        return -1

    return 1


def _is_edu(u):
    if re.match(r'.edu$', u):
        return 1

    return -1


def _is_common_tld(u):
    if re.match(r'.[com|net|org|edu]$', u):
        return 1

    return -1


def _has_low_length(u):
    uu = re.sub(r'\.[a-zA-Z]{2}$', '', u)
    uu = re.sub(r'^www\.', '', uu)

    l = len(uu)
    if l < 6:
        return -1

    if l < 12:
        return 0

    return 1


def _has_high_length(u):
    uu = re.sub(r'\.[a-zA-Z]{2}$', '', u)
    uu = re.sub(r'^www\.', '', uu)

    l = len(uu)
    if l < 15:
        return -1

    if l < 17:
        return 0

    return 1


FEATURES = [
    _is_non_std,
    _has_high_length,
    _has_low_length,
    _has_close_distance,
    _has_high_entropy,
    _has_hyphens,
    _has_subdomains,
    _is_secure,
    _is_ip,
    _is_edu,
    _is_common_tld,
]


def _extract_features(u):
    feats = []

    for f in FEATURES:
        r = f(u)
        feats.append(r)

    return feats


def predict(d, classifier):
    feats = _extract_features(d)
    feats = np.array([feats], dtype=int)
    return classifier.predict(feats)


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $ csirtg-domainsml --training data/training.csv -i paypal-badsite.com
                '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-domainsml'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('--good', action="store_true", default=False)

    args = p.parse_args()

    for l in sys.stdin:
        l = l.rstrip()
        ff = _extract_features(l)

        if args.good:
            ff.append(0)
        else:
            ff.append(1)

        ff = [str(f) for f in ff]
        out = ','.join(ff)
        print(out)


if __name__ == '__main__':
    main()
