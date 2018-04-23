import os
from setuptools import setup, find_packages
import versioneer
import sys


# https://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
        'coverage',
        'pytest_cov',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirements." % err_msg
        raise ImportError(msg)
    r = os.system('py.test test -v --cov=csirtg_ipsml --cov-fail-under=65')
    if r == 0:
        sys.exit()
    else:
        raise RuntimeError('tests failed')


data_files = [
    'data/whitelist.txt',
    'data/blacklist.txt',
    'data/model.pickle',
    'data/py2model.pickle'
]

setup(
    name="csirtg_ipsml",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CSIRTG IP ML Framework",
    long_description="",
    url="https://github.com/csirtgadgets/csirtg-ipsml",
    license='MPL2',
    data_files=[('data', data_files)],
    keywords=['network', 'security'],
    author="Wes Young",
    author_email="wes@barely3am.com",
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.19,<0.20',
        'numpy',
        'scipy',
        'pygeoip',
        'arrow',
        'maxminddb',
        'geoip2',
    ],
    entry_points={
       'console_scripts': [
           'csirtg-ipsml-train=csirtg_ipsml.train:main',
           'csirtg-ipsml=csirtg_ipsml:main'
       ]
    },
)
