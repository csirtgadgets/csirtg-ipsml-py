from __future__ import print_function
import numpy as np
from sklearn import tree, ensemble
from sklearn.metrics import accuracy_score, recall_score
from sklearn.preprocessing import OneHotEncoder
import pickle
from pprint import pprint
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import sys
import textwrap
import os
# http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
from sklearn import preprocessing
import ipaddress

# from .constants import PYVERSION


# https://timezonedb.com/download
me = os.path.dirname(__file__)

MODEL = '%s/../data/model.pickle' % me
# if PYVERSION == 2:
#     MODEL = '%s/../data/model_py2.pickle' % me

DATA_PATH = '%s/../data/feed2.txt' % me


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


def accuracy(classifier, test_inputs, test_outputs):
    # Use the trained classifier to make predictions on the test data
    predictions = classifier.predict(test_inputs)
    print("Predictions on testing data computed.")

    # Print the accuracy (percentage of phishing websites correctly predicted)
    accuracy = 100.0 * accuracy_score(test_outputs, predictions)
    recall = 100.0 * recall_score(test_outputs, predictions, average='micro')
    print("The recall score of your decision tree on testing data is: " + str(recall))
    print("The accuracy of your decision tree on testing data is: " + str(accuracy))


def load_data(handle):
    cc_data = preprocessing.LabelEncoder()
    cc_data.fit(CC)

    tz_data = preprocessing.LabelEncoder()
    tz_data.fit(TZ)

    lines = []
    for l in handle:
        # hour, ip, lat, long, tz, cc, asn
        l = l.rstrip("\n").split(',')
        pprint(l)

        l[1] = int(ipaddress.ip_address(l[1]))

        t = tz_data.transform([l[4]])[0]
        y = cc_data.transform([l[5]])[0]

        l[4] = y
        l[5] = t

        lines.append(l)

    training_data = np.array(lines, dtype=int)
    print("Training data loaded.")

    return training_data


def train_model(training_data):
    inputs = training_data[:, :-1]
    outputs = training_data[:, -1]

    n = int(len(inputs) * .7)
    train_inputs = inputs[:n]
    train_outputs = outputs[:n]

    test_inputs = inputs[n:]
    test_outputs = outputs[n:]
    print("Training data loaded.")

    # Create a decision tree classifier model using scikit-learn
    classifier = ensemble.RandomForestClassifier()
    print("classifier created.")

    print("Beginning model training.")
    # Train the decision tree classifier
    classifier.fit(train_inputs, train_outputs)
    print("Model training completed.")

    return classifier, test_inputs, test_outputs


def model_save(cls, filename):
    print("Saving model to %s" % filename)
    print(filename, pickle.dumps(cls))


def main():
    import sys
    p = ArgumentParser(
        description=textwrap.dedent('''\
                    example usage:
                        $
                    '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-ipsml'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('--save')
    p.add_argument('--load')
    p.add_argument('--training')

    args = p.parse_args()

    if args.load:
        with open(args.load) as FILE:
            classifier = pickle.load(FILE)

    else:
        handle = sys.stdin
        if args.training:
            handle = open(args.training)

        training_data = load_data(handle)
        classifier, test_inputs, test_outputs = train_model(training_data)
        accuracy(classifier, test_inputs, test_outputs)

    if args.save:
        with open(args.save, 'w') as OUTFILE:
            print(pickle.dumps(classifier), file=OUTFILE)


if __name__ == '__main__':
    main()
