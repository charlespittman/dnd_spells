from __future__ import unicode_literals

import json
import re


class Spell:

    fields = ["archetype", "casting_time", "circles", "class", "components",
              "concentration", "desc", "domains", "duration", "higher_level",
              "level", "material", "name", "oaths", "page", "patrons", "range",
              "ritual", "school", ]

    stats = ['Strength', 'Constitution', 'Dexterity', 'Intelligence', 'Wisdom',
             'Charisma', ]

    def __init__(self, entry):
        self.entry = entry
        self.archetype = entry.get('archetype')
        self.casting_time = entry.get('casting_time')
        self.circles = entry.get('circles')
        self.distance = entry.get('range')
        self.domains = entry.get('domains')
        self.duration = entry.get('duration')
        self.material = entry.get('material')
        self.name = entry.get('name')
        self.oaths = entry.get('oaths')
        self.reference = entry.get('page')
        self.school = entry.get('school')

    # FIXME: Need to have this in right format
    def __repr__(self):
        return 'Spell({}, {})'.format(self.name, self.description)

    def __str__(self):
        return 'Name: "{}", Level: {}'.format(self.name, self.level)

    @property
    def ritual(self):
        return 'yes' in self.entry.get('ritual')

    @property
    def components(self):
        return self.entry.get('components').split(', ')

    @property
    def concentration(self):
        return 'yes' in self.entry.get('concentration').lower()

    @property
    def description(self):
        return [p for p in re.split(r'</?p>', self.entry.get('desc')) if p]

    @property
    def higher_level(self):
        self._higher_level = self.entry.get('higher_level')
        if self._higher_level:
            return [p for p in re.split(r'</?p>', self._higher_level) if p]

    @property
    def level(self):
        lvl = self.entry.get('level').lower()
        if 'cantrip' in lvl:
            return 0
        else:
            return int(re.match(r'(\d)', lvl).group(0))

    @property
    def pc_class(self):
        return self.entry.get('class').split(', ')

    @property
    def saving_throw(self):
        self._saves = []
        for s in self.stats:
            for d in self.description:
                if s in d:
                    self._saves.append(s)
        return self._saves

with open('spellData.json', 'r') as f:
    data = json.load(f)

bard_spells = []
cleric_spells = []
druid_spells = []
paladin_spells = []
ranger_spells = []
sorceror_spells = []
wizard_spells = []
warlock_spells = []

ritual_spells = []

verbal_spells = []
somatic_spells = []
material_spells = []

illusion_spells = []
enchantment_spells = []

for entry in data:
    spell = Spell(entry)
    if 'Bard' in spell.pc_class:
        bard_spells.append(spell)
    if 'Cleric' in spell.pc_class:
        cleric_spells.append(spell)
    if 'Druid' in spell.pc_class:
        druid_spells.append(spell)
    if 'Paladin' in spell.pc_class:
        paladin_spells.append(spell)
    if 'Ranger' in spell.pc_class:
        ranger_spells.append(spell)
    if 'Sorceror' in spell.pc_class:
        sorceror_spells.append(spell)
    if 'Wizard' in spell.pc_class:
        wizard_spells.append(spell)
    if 'Warlock' in spell.pc_class:
        warlock_spells.append(spell)

    # Del says only Bards, Clerics, Druids, and Wizards can cast all of their
    # spells as rituals.  There are special rules for Paladins, Rangers, and
    # Warlocks, which this doesn't account for.
    if spell.ritual:
        ritual_spells.append(spell)

    if 'M' in spell.components:
        material_spells.append(spell)
    if 'S' in spell.components:
        somatic_spells.append(spell)
    if 'V' in spell.components:
        verbal_spells.append(spell)

    if 'Illusion' in spell.school:
        illusion_spells.append(spell)

    if 'Enchantment' in spell.school:
        enchantment_spells.append(spell)

def ie(n):
    for s in enchantment_spells + illusion_spells:
        if s.level is n:
            print(s.name, s.level)

# if __name__ == '__main__':
#     with open('spellData.json', 'r') as f:
#         data = json.load(f)

#     for spell in data:
#         if 'paladin' in spell.pc_class.lower():
#             paladin_spells.append(s)
