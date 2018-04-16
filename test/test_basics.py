# -*- coding: utf-8 -*-
from csirtg_ipsml import predict
from faker import Faker
from random import sample
from pprint import pprint
from time import time
import os, random
import re
import arrow

fake = Faker()


IPS = [
    ('0','141.142.234.238'),
    ('1', '128.205.1.1'),
    ('17', '128.205.1.1')
]

THRESHOLD = 0.92
SAMPLE = int(os.getenv('CSIRTG_DOMAINSML_TEST_SAMPLE', 200))


def _stats(u, inverse=False):
    n = 0
    positives = 0
    t1 = time()
    for p in u:
        p = predict(p[1], p[0])
        if (inverse and p == 0) or p == 1:
            positives += 1
        n += 1

    t2 = time()
    total = t2 - t1
    per_sec = SAMPLE / total
    print("seconds: %.2f" % total)
    print("rate: %.2f" % per_sec)

    n = (float(positives) / n)
    print(n)
    return n


def test_basics():
    assert _stats(IPS) >= 0.5


def test_random():
    s = []
    for d in range(0, SAMPLE):
        s.append([random.randint(0,23), str(fake.ipv4())])

    n = _stats(s)
    assert n > .55


def test_blacklist():
    d = []
    with open('data/blacklist.txt') as FILE:
        for l in FILE.readlines():
            l = l.rstrip("\n")
            l = re.sub(r'\r|"', '', l)
            l = l.split(',')
            l[0] = arrow.get(l[0]).hour
            d.append(l)

    d = sample(d, SAMPLE)

    n = _stats(d)
    assert n > THRESHOLD


def test_whitelist():
    d = []
    with open('data/whitelist.txt') as FILE:
        for l in FILE.readlines():
            l = l.rstrip("\n")
            l = re.sub(r'\r|"', '', l)
            l = l.split(',')
            l[0] = arrow.get(l[0]).hour
            d.append(l)

    d = sample(d, 15)
    n = _stats(d, inverse=True)
    assert n > THRESHOLD
