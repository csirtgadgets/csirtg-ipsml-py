# csirtg-ipsml
simple library for detecting suspicious connections.

This model is very simple and looks at features such as:

* Time of day (hour)
* General Long / Lat
* TimeZone
* Country Code
* ASN

NOTE: THE DEFAULT DATA-SETS ARE NOT STATISTICALLY SOUND

While not meant to be perfect, meant to demonstrate how you might look at suspicious connections and build a VERY SIMPLE machine learning model around those features.

https://csirtgadgets.com/commits/2018/4/20/predicting-attacks-with-python-and-sklearn
https://csirtgadgets.com/commits/2018/3/8/hunting-for-suspicious-domains-using-python-and-sklearn
https://csirtgadgets.com/commits/2018/3/30/hunting-for-threats-like-a-quant

```bash
$ sudo [apt-get|brew|yum] install geoipupdate  # ubuntu16 or later, should use if you can python3
$ sudo geoipupdate -v
$ pip install -r dev_requirements.txt
$ python setup.py develop
$ bash rebuild.sh
$ bash build_model.sh

$ csirtg-ipsml -i 122.2.223.242,6  # indicator, hour-detected
Yes
$ csirtg-domainsml -i 141.142.164.33  # indicator, hour-detected
No
```
