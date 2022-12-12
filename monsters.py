"""Monsters"""

from enum import auto, Enum
from uuid import UUID, uuid4

from actions import MeleeWeaponAttack, Multiattack
from character import BaseCharacter
from equipment import ArmorList, WeaponProperty
from models import CharacterModel
from rule_books import FifthEdition as Rules
from arena_utils import roll_sum

class Size(Enum):
    TINY = 4
    SMALL = 6
    MEDIUM = 8
    LARGE = 10
    HUGE = 12

class BaseMonster(BaseCharacter):

    @classmethod
    def create(cls, model, challenge_rate, size, armor, has_shield=False):
        obj = cls()
        obj.challenge_rate = challenge_rate
        obj.model = model
        obj.model.rolled_hit_points = roll_sum(model.hit_dice, size.value)
        obj.model.max_hit_points = model.rolled_hit_points + model.hit_dice * Rules.get_ability_modifier(model.constitution)
        obj.has_shield = has_shield
        obj.set_armor_class(armor)
        obj.current_hp = obj.model.max_hit_points
        obj.is_alive = True
        obj.update()
        return obj

    @classmethod
    def create_goblin(cls, simulation):
        model = CharacterModel(uuid4(), simulation, "goblin", 2, 0, 0, ArmorList.LEATHER.armor_class, 8, 14, 10, 10, 8, 8)
        monster = BaseMonster.create(model, 0, Size.SMALL, ArmorList.LEATHER, True)
        monster.append_action(MeleeWeaponAttack(monster, (1,6), WeaponProperty.FINESSE|WeaponProperty.LIGHT))
        return monster

    @classmethod
    def create_ogre(cls, simulation):
        model = CharacterModel(uuid4(), simulation, "ogre", 7, 0, 0, ArmorList.HIDE.armor_class, 19, 8, 16, 5, 7, 7)
        monster = BaseMonster.create(model, 2, Size.LARGE, ArmorList.HIDE)
        large_greatclub = MeleeWeaponAttack(monster, (2,8), WeaponProperty.TWO_HANDED)
        monster.append_action(large_greatclub)
        return monster

    @classmethod
    def create_owlbear(cls, simulation):
        model = CharacterModel(uuid4(), simulation, "owlbear", 7, 0, 0, ArmorList.NATURAL_13.armor_class, 20, 12, 17, 3, 12, 7)
        monster = BaseMonster.create(model, 3, Size.LARGE, ArmorList.NATURAL_13)
        claws = MeleeWeaponAttack(monster, (2,8))
        beak = MeleeWeaponAttack(monster, (1,10))
        monster.append_action(Multiattack(monster, [claws, beak]))
        monster.append_action(claws)
        monster.append_action(beak)
        return monster

    @classmethod
    def create_hill_giant(cls, simulation):
        model = CharacterModel(uuid4(), simulation, "hill giant", 10, 0, 0, ArmorList.NATURAL_13.armor_class, 21, 8, 19, 5, 9, 6)
        monster = BaseMonster.create(model, 5, Size.HUGE, ArmorList.NATURAL_13)
        greatclub = MeleeWeaponAttack(monster, (3,8), WeaponProperty.TWO_HANDED)
        monster.append_action(Multiattack(monster, [greatclub, greatclub]))
        monster.append_action(greatclub)
        return monster

    def __init__(self):
        self.challenge_rate = 0

    def update(self):
        self.proficiency = Rules.get_proficiency(self.challenge_rate)
        super().update()
