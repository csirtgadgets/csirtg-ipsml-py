from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import os
import pickle
from csirtg_ipsml.ip import predict as predict_ip
from pprint import pprint
from .constants import PYVERSION
import sys

MODEL = 'model.pickle'
if PYVERSION == 2:
    MODEL = 'model_py2.pickle'

if os.path.exists(os.path.join(sys.prefix, 'csirtg_ipsml', 'data', MODEL)):
    MODEL = os.path.join(sys.prefix, 'csirtg_ipsml', 'data', MODEL)
else:
    MODEL = os.path.join('%s/../data/%s' % (os.path.dirname(__file__), MODEL))

CLS = None
if os.path.exists(MODEL):
    with open(MODEL, 'rb') as F:
        CLS = pickle.load(F)


def predict(i, classifier=CLS):
    if not classifier:
        with open(MODEL, 'rb') as FILE:
            classifier = pickle.load(FILE)

    return predict_ip(i, classifier)[0]


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
                $ csirtg-ipsml 192.158.1.1,6  # indicator,hour
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-ipsml'
    )

    p.add_argument('-i', '--indicator', help="specify indicator")

    args = p.parse_args()

    p = predict(args.indicator)
    if p:
        print("Yes")
    else:
        print("No")


if __name__ == '__main__':
    main()
