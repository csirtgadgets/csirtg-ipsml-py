from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import os
import pickle
from csirtg_ipsml.ip import predict as predict_ip
from pprint import pprint
from .constants import PYVERSION
import sys
import arrow

MODEL = 'model.pickle'
if PYVERSION == 2:
    MODEL = 'model_py2.pickle'

if os.path.exists(os.path.join(sys.prefix, 'csirtg_ipsml', 'data', MODEL)):
    MODEL = os.path.join(sys.prefix, 'csirtg_ipsml', 'data', MODEL)

elif os.path.exists(os.path.join('usr', 'local',  'csirtg_ipsml', 'data', MODEL)):
    MODEL = os.path.join('usr', 'local',  'csirtg_ipsml', 'data', MODEL)

else:
    MODEL = os.path.join('%s/../data/%s' % (os.path.dirname(__file__), MODEL))

CLS = None
if os.path.exists(MODEL):
    with open(MODEL, 'rb') as F:
        CLS = pickle.load(F)


def predict(i, ts, classifier=CLS):
    if not classifier:
        with open(MODEL) as FILE:
            classifier = pickle.load(FILE)

    return predict_ip(i, ts, classifier)[0]


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
                $ csirtg-ipsml -i 192.158.1.1,6  # indicator,hour
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-ipsml'
    )

    p.add_argument('-i', '--indicator', help="specify indicator")

    args = p.parse_args()

    if ',' in args.indicator:
        i, hour = args.indicator.split(',')
    else:
        hour = arrow.utcnow().hour
        i = args.indicator

    p = predict(i, hour)
    if p:
        print("Yes")
    else:
        print("No")


if __name__ == '__main__':
    main()
