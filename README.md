# csirtg-ipssml
simple library for detecting suspicious connections

```bash
$ pip install -r dev_requirements.txt
$ python setup.py develop
$ bash rebuild.sh
$ bash build_model.sh

$ csirtg-ipsml -i 122.2.223.242,6  # indicator, hour-detected
Yes
$ csirtg-domainsml -i 141.142.164.33  # indicator, hour-detected
No
```
