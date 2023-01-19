"""Actions"""

import logging

from equipment import WeaponProperty
from rule_books import FifthEdition as Rules
from arena_utils import roll_die, roll_sum

class BaseAction:

    def __init__(self, owner):
        self.owner = owner
        self.short_rested = True
        self.long_rested = True

    def update(self):
        "Implement this method"
        pass

    def execute(self):
        "Implement this method"
        pass

class SecondWind(BaseAction):

    def execute(self):
        if self.short_rested and self.owner.current_hp <= self.owner.model.max_hit_points * 0.3:
            amount = self.owner.model.hit_dice * roll_die(10)
            old_hp = self.owner.current_hp
            self.owner.current_hp = min(self.owner.model.max_hit_points, self.owner.current_hp + amount)
            self.short_rested = False
            logging.debug(f"ACTION,SECOND_WING,{self.owner.model.uuid},{self.owner.current_hp - old_hp}")
            return True
        return False

class MeleeWeaponAttack(BaseAction):

    @staticmethod
    def create_dagger(owner):
        return MeleeWeaponAttack(owner, (1,4), WeaponProperty.FINESSE|WeaponProperty.LIGHT|WeaponProperty.THROWN)

    @staticmethod
    def create_greataxe(owner):
        return MeleeWeaponAttack(owner, (1,12), WeaponProperty.HEAVY|WeaponProperty.TWO_HANDED)

    @staticmethod
    def create_greatsword(owner):
        return MeleeWeaponAttack(owner, (2,6), WeaponProperty.HEAVY|WeaponProperty.TWO_HANDED)

    @staticmethod
    def create_scimitar(owner):
        return MeleeWeaponAttack(owner, (1,6), WeaponProperty.FINESSE|WeaponProperty.LIGHT)

    @staticmethod
    def create_shortsword(owner):
        return MeleeWeaponAttack(owner, (1,6), WeaponProperty.FINESSE|WeaponProperty.LIGHT)

    @staticmethod
    def create_longsword(owner):
        return MeleeWeaponAttack(owner, (1,8), WeaponProperty.VERSATILE)

    def __init__(self, owner, damage_dice, weapon_properties=WeaponProperty.NONE):
        super().__init__(owner)
        self.damage_dice = damage_dice
        self.weapon_properties = weapon_properties
        self.ability_modifier = 0

    def update(self):
        strength_mod = Rules.get_ability_modifier(self.owner.model.strength)
        finesse_mod = max(strength_mod, Rules.get_ability_modifier(self.owner.model.dexterity))
        use_finesse = bool(WeaponProperty.FINESSE in self.weapon_properties)
        self.ability_modifier = strength_mod*(not use_finesse) + finesse_mod*use_finesse

    def execute(self, target):
        die_roll = roll_die(20)
        if die_roll > 1:
            attack_roll = die_roll + self.owner.proficiency + self.ability_modifier
            armor_class = target.model.armor_class
            if die_roll == 20 or attack_roll >= armor_class:
                dmg_dice = self.damage_dice[1] + 2*(WeaponProperty.VERSATILE in self.weapon_properties)
                damage = max(1,roll_sum(self.damage_dice[0], dmg_dice) + self.ability_modifier + (die_roll >= self.owner.skill_critical_hit) * roll_sum(self.damage_dice[0], dmg_dice))
                target.take_damage(damage)
                logging.debug(f"ACTION,MELEE_WEAPON_ATTACK,TRUE,{self.owner.model.uuid},{target.model.uuid},{die_roll},{attack_roll},{armor_class},{damage}")
            else:
                logging.debug(f"ACTION,MELEE_WEAPON_ATTACK,FALSE,{self.owner.model.uuid},{target.model.uuid},{die_roll},{attack_roll},{armor_class}")
        else:
            logging.debug(f"ACTION,MELEE_WEAPON_ATTACK,FALSE,{self.owner.model.uuid},{target.model.uuid},{die_roll}")
        return True

class ExtraAttack(BaseAction):

    def __init__(self, owner, attack):
        super().__init__(owner)
        self.number_of_attacks = 2
        self.attack = attack

    def execute(self, target):
        r = True
        for i in range(self.number_of_attacks):
            r = r and self.attack.execute(target)
        return r

class Multiattack(BaseAction):

    def __init__(self, owner, attacks):
        super().__init__(owner)
        self.attacks = attacks

    def execute(self, target):
        r = True
        for atk in self.attacks:
            r = r and atk.execute(target)
        return r

    def update(self):
        for atk in self.attacks:
            atk.update()
