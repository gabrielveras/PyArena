""""""

from enum import Flag, auto
from math import ceil, floor

from arena_utils import roll_sum

class FirstEdition:

    ABILITY_SCORES = [-8, -5, -3, -2, -2, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 5, 8]

    @classmethod
    def get_ability_modifier(cls, score):
        return cls.ABILITY_SCORES[score+1]

    @classmethod
    def roll_ability_score(cls):
        return roll_sum(3, 6)

    @classmethod
    def get_max_hit_points(cls, hit_dice, rolled_hit_points, constitution=0):
        max_hp = rolled_hit_points + cls.get_ability_modifier(constitution) + max(0, (hit_dice-9)*2)
        return max(1, max_hp)

class FifthEdition:

    class Skills(Flag):
        NONE = 0
        ACROBATICS = auto()
        ANIMAL_HANDLING = auto()
        ATHLETICS = auto()
        HISTORY = auto()
        INSIGHT = auto()
        INTIMIDATION = auto()
        PERCEPTION = auto()
        SURVIVAL = auto()

    class FightingStyle(Flag):
        NONE = 0
        ARCHERY = auto()
        DEFENSE = auto()
        DUELING = auto()
        GREAT_WEAPON = auto()
        PROTECTION = auto()
        TWO_WEAPON = auto()
        ALL = ARCHERY | DEFENSE | DUELING | GREAT_WEAPON | PROTECTION | TWO_WEAPON

    @classmethod
    def get_proficiency(cls, value):
        "Param is Hit Dice for PCs and Challenge Rate for NPCs."
        return max(2, ceil(value/4) + 1)

    @classmethod
    def get_ability_modifier(cls, score):
        return floor((score-10)/2)

    @classmethod
    def roll_ability_score(cls):
        return roll_sum(4, 6, True)

    @classmethod
    def get_max_hit_points(cls, hit_dice, rolled_hit_points, hit_die_size=8, constitution=0):
        max_hp = hit_die_size + rolled_hit_points + (hit_dice * cls.get_ability_modifier(constitution))
        return max(1, max_hp)
