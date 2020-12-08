import unittest
import math


class Group(object):
    def __init__(
        self,
        units,
        dmg,
        hitpoints,
        atk_type,
        weaknesses,
        immunes,
        initiative,
        g_type,
        id,
    ):
        self._type = g_type
        self.units = units
        self._dmg = dmg
        self.hitpoints = hitpoints
        self._atk_type = atk_type
        self._weaknesses = weaknesses
        self._immunes = immunes
        self._initiative = initiative
        self._id = id

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, number):
        self._units = number

    @property
    def hitpoints(self):
        return self._hitpoints

    @hitpoints.setter
    def hitpoints(self, points):
        self._hitpoints = points

    @property
    def effective_power(self):
        return self._units * self._dmg

    @property
    def type(self):
        return self._type

    @property
    def initiative(self):
        return self._initiative

    @property
    def id(self):
        return self._id

    @property
    def atk_type(self):
        return self._atk_type

    def dmg_from_group(self, group):
        if group.atk_type in self._weaknesses:
            return group.effective_power * 2
        if group.atk_type in self._immunes:
            return 0
        return group.effective_power

    def inflict_dmg(self, group):
        prev = self.units
        self.units = max((self.units - self.dmg_from_group(group) // self.hitpoints), 0)
        return prev - self.units


def read_data(fname):
    with open(fname) as f:
        result = f.readlines()
    return result


def dicts_from_lines(lines):
    dicts = []
    for line in lines:
        line = line.strip()

        units = int(line.split()[0])
        hit_points = int(line.split()[4])
        weaknesses = []
        immunes = []
        if "(" in line:
            attributes_line = line[line.index("(") + 1 : line.index(")")]
            attributes = attributes_line.split(";")
            for attribute in attributes:
                if "weak" in attribute:
                    weaknesses = attribute[attribute.index("weak") + 8 :].split(",")
                    weaknesses = [w.split()[0] for w in weaknesses]
                if "immune" in attribute:
                    immunes = attribute[attribute.index("immune") + 10 :].split(",")
                    immunes = [i.split()[0] for i in immunes]

        dmg_initiative = line[line.index("does") :].split()

        dicts.append(
            {
                "units": units,
                "hitpoints": hit_points,
                "dmg": int(dmg_initiative[1]),
                "weaknesses": weaknesses,
                "immunes": immunes,
                "atk_type": dmg_initiative[2],
                "initiative": int(dmg_initiative[6]),
            }
        )

    return dicts


def parse(lines):
    split_idx = lines.index("Infection:\n")
    infections = dicts_from_lines(lines[1 : split_idx - 1])
    infections = [
        Group(**g, g_type="Immune System", id=i + 1) for i, g in enumerate(infections)
    ]
    immune_systems = dicts_from_lines(lines[split_idx + 1 :])
    immune_systems = [
        Group(**g, g_type="Infection", id=i + 1) for i, g in enumerate(immune_systems)
    ]
    infections.extend(immune_systems)
    return infections


def selection_phase(groups):
    selection_order = sorted(
        groups, key=lambda x: (x.effective_power, x.initiative), reverse=True
    )
    ordered_attacking_groups = []
    for group in selection_order:
        already_selected = [g for _, g in ordered_attacking_groups]
        defending_groups = [
            g for g in groups if g.type != group.type and g not in already_selected
        ]
        if defending_groups:
            possible_targets = sorted(
                defending_groups,
                key=lambda x: (
                    x.dmg_from_group(group),
                    x.effective_power,
                    x.initiative,
                ),
                reverse=True,
            )
            ordered_attacking_groups.append((group, possible_targets[0]))
    return ordered_attacking_groups


def attacking_phase(groups):
    groups = sorted(groups, key=lambda x: x[0].initiative, reverse=True)
    for attacker, defender in groups:
        if defender.units < 1 or attacker.units < 1:
            continue
        units = defender.inflict_dmg(attacker)
        print(
            "{} group {} attacks {} group {}, killing {} units".format(
                attacker.type, attacker.id, defender.type, defender.id, units
            )
        )


def army_strength(groups, type):
    strength = 0
    for g in groups:
        if g.type == type:
            strength += g.units
    return strength


def play(groups):
    i = 1
    while True:
        groups = [g for g in groups if g.units > 0]
        selected_groups = selection_phase(groups)
        attacking_phase(selected_groups)
        infectious_army = army_strength(groups, "Infection")
        immune_army = army_strength(groups, "Immune System")
        # print("Fight: {}, remaining infectious: {}, remaining immune: {}".format(
        #       i, infectious_army, immune_army))
        print("")
        if infectious_army == 0:
            print("Immune system won, remaining units: {}".format(immune_army))
            return immune_army
        if immune_army == 0:
            print("Infections won, remaining units: {}".format(infectious_army))
            return infectious_army
        i += 1
        if i > 10000:
            print("more than 10000 itterations")
            break


class Test(unittest.TestCase):
    def test(self):
        lines = read_data("day24_testinput.txt")
        groups = parse(lines)
        assert play(groups) == 5216


if __name__ == "__main__":
    unittest.main()
    lines = read_data("day24_input.txt")
    groups = parse(lines)
    play(groups)
