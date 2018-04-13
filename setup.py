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
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)
    r = os.system('py.test test -v --cov=csirtg_domainsml --cov-fail-under=75')
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
    name="csirtg_domainsml",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CSIRTG Domains ML Framework",
    long_description="",
    url="https://github.com/csirtgadgets/csirtg-domainsml",
    license='MPLv2',
    data_files=[('data', data_files)],
    keywords=['network', 'security'],
    author="Wes Young",
    author_email="wes@barely3am.com",
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.19,<0.20',
        'numpy',
        'scipy',
        'editdistance'
    ],
    entry_points={
       'console_scripts': [
           'csirtg-domainsml-train=csirtg_domainsml.train:main',
           'csirtg-domainsml=csirtg_domainsml:main'
       ]
    },
)
