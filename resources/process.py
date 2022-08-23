import sys
import os
scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptdir, "..", "lib"))
sys.path.append(os.path.join(scriptdir, "..", "db"))

from confs_years import *

import re
import bibyml
from pprint import pprint
import mybibtex.parser
from collections import OrderedDict

parser = mybibtex.parser.Parser()
parser.parse_file("../db/abbrev0.bib")
parser.parse_file("../db/crypto_db.bib")
db = parser.parse_file("../db/crypto_conf_list.bib")

with open("abbrev.bibyml") as f:
    contents = bibyml.parse(f)

confs = get_confs_years(db)

def conf_to_name(name: str) -> str:
    convert = {
        'AC': 'asiacrypt',
        'C': 'crypto',
        'EC': 'eurocrypt',
        'SP': 'ieeesp',
        'LC': 'latincrypt',
        "JCEng": 'jcryptoeng',
        'JC': 'jcrypto',
    }
    return convert.get(name, name.lower())

months = {
    'jan': "01",
    'feb': '02',
    'mar': '03',
    'apr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dec': '12',
}

for conf, years in confs.items():
    if conf in ("JC", "JCEng", "EPRINT", "ToSC", "TCHES", "PoPETS"):
        continue
    for year in years:
        try:
            print(f"{conf!r} {year!r}", end=': ')
            confkey = conf_to_name(conf)
            yearkey = f"{str(year)[-2:]}"
            if '@0' in contents[confkey][yearkey]['month']:
                month = contents[confkey][yearkey]['month']['@0']['']
                print(month,end='')
            else:
                print('missing month')
                continue
        except KeyError as ke:
            print("missing key:", ke)
            continue

        if "~--~" in month:
            first_monthday, second_monthday = month.split("~--~")
            first_month = months[first_monthday.split("#", 1)[0].strip()]
            second_month = months[second_monthday.split("#", 3)[1].strip()]
        else:
            first_monthday = month
            first_month = months[month.split("#", 1)[0].strip()]
            second_month = first_month
        first_day = int(re.search(r'~(\d+)', first_monthday).group(1))
        last_day = int(re.search(r'(\d+)(,)?\"$', month).group(1))

        date = f"{year}-{first_month}-{first_day:02d}/{year}-{second_month}-{last_day:02d}"
        print("--> ", date)

        contents[confkey][yearkey]['date'] = OrderedDict(
            {
                "": "",
                '@0': {'': f"\"{date}\""},
                '@1': {'': f"\"{year}-{first_month}\""},
            })

with open("processed.bibyml", 'w') as fh:
    fh.write(bibyml.write_str(contents))