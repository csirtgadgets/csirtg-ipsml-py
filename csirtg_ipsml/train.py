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
from .ip import TZ, CC
from .ip import extract_features, fit_features


def accuracy(classifier, test_inputs, test_outputs):
    # Use the trained classifier to make predictions on the test data
    predictions = classifier.predict(test_inputs)
    print("Predictions on testing data computed.")

    # Print the accuracy (percentage of phishing websites correctly predicted)
    accuracy = 100.0 * accuracy_score(test_outputs, predictions)
    recall = 100.0 * recall_score(test_outputs, predictions, average='micro')
    print("The recall score of your decision tree on testing data is: " + str(recall))
    print("The accuracy of your decision tree on testing data is: " + str(accuracy))


def load_data(data):
    lines = []
    for l in data:
        # hour, ip, lat, long, tz, cc, asn, bad
        l = l.rstrip("\n").split(',')

        res = l[7]

        l = list(extract_features(','.join([l[1], l[0]])))
        l[0].append(res)
        lines.append(l[0])

    lines = list(fit_features(lines))
    training_data = np.array(lines, dtype=int)
    print(training_data[1])
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
        prog='csirtg-ipsml-train'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('--save')
    p.add_argument('--load')
    p.add_argument('--training')
    p.add_argument('-i', '--indicator')

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
        with open(args.save, 'wb') as OUTFILE:
            pickle.dump(classifier, OUTFILE)


if __name__ == '__main__':
    main()
