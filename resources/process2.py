import re

with open("abbrev0.bib", "r") as fh:
    abbrevcontents = fh.read()

with open("crypto_conf_list.bib", "r") as fh:
    for line in fh.readlines():
        print(line, end='')
        if match := re.match(r"  month =(?P<spacing>\s*)(?P<key>\w+\d+)month,$", line):
            datekeysearch = "@string{" + f"{match.group('key')}date"
            spaces = match.group("spacing")
            if datekeysearch in abbrevcontents:
                #print('yearkey exists')
                print(f"  date = {spaces}{match.group('key')}date,")
