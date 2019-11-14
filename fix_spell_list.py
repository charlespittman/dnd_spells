import json
import re


SCHOOLS = ['Abjuration', 'Conjuration', 'Divination', 'Enchantment',
           'Evocation', 'Illusion', 'Necromancy', 'Transmutation']

def str_bool(string):
    return 'yes' in string.lower()

def str_list(string):
    return [s.strip() for s in string.split(',')]

def str_par(string):
    pars = re.split(r'</?p>', string)
    return [p for p in pars if p]

def main():
    with open('spellData.json', 'r') as f:
        data = json.load(f)

    for s in data:
        assert s['school'] in SCHOOLS

        for b in ['concentration', 'ritual']:
            if isinstance(s[b], str):
                s[b] = str_bool(s[b])

        for l in ['components', 'class']:
            if isinstance(s[l], str):
                s[l] = str_list(s[l])

        for p in ['desc', 'higher_level']:
            try:
                if isinstance(s[p], str):
                    s[p] = str_par(s[p])
            except KeyError:
                s[p] = None

        try:
            s['material'] = s['material']
        except KeyError:
            s['material'] = None

    with open('spells.json', 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
