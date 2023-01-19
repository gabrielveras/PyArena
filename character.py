"""Characters"""

import logging

from random import choice, shuffle
from uuid import uuid4

from actions import SecondWind, ExtraAttack
from database import Database
from equipment import ArmorList
from models import ClassModel, PartyModel, character_str
from rule_books import FifthEdition as Rules
from arena_utils import roll_die, roll_sum

class BaseCharacter:

    HIT_DIE_SIZE = 8

    def __init__(self):
        self.model = None
        self.current_hp = 0
        self.proficiency = 2
        self.is_alive = True
        self._armor = ArmorList.UNARMORED
        self.has_shield = False
        self._actions = []
        self.bonus_actions = []
        self.skill_extra_attack = 1
        self.skill_critical_hit = 20
        self.skill_action_surge = False
        self.skill_fighting_style = Rules.FightingStyle.NONE

    def update(self):
        self.model.max_hit_points = Rules.get_max_hit_points(self.model.hit_dice, self.model.rolled_hit_points, self.__class__.HIT_DIE_SIZE, self.model.constitution)
        self.proficiency = Rules.get_proficiency(self.model.hit_dice)
        self.set_armor_class()
        for action in self._actions:
            action.update()

    def set_armor_class(self, armor=None):
        if armor is not None:
            self._armor = armor
        armor_class = self._armor.get_armor_class(Rules.get_ability_modifier(self.model.dexterity)) + 2*self.has_shield
        armor_class += int((Rules.FightingStyle.DEFENSE in self.skill_fighting_style) and (self._armor is not ArmorList.UNARMORED))
        self.model.armor_class = armor_class

    def get_action(self):
        return self._actions[0]

    def append_action(self, action):
        self._actions.append(action)
        action.update()

    def take_damage(self, damage):
        self.current_hp -= damage
        self.current_hp = max(self.current_hp, 0)
        self.is_alive = self.current_hp > 0

    def act(self, allies, enemies):
        target = enemies.get_random_melee_target()
        if target is not None:
            self.get_action().execute(target)
        if self.skill_action_surge:
            target = enemies.get_random_melee_target()
            if target is not None:
                self.get_action().execute(target)

class BaseClass(BaseCharacter):

    EXPERIENCE_TABLE = [0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000, 100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000]

    @classmethod
    def create(cls, name="", level=1, armor=ArmorList.UNARMORED):
        obj = cls()
        #str, dex, con, wis, int, cha = 15, 13, 14, 12, 10, 8
        str, dex, con = Rules.roll_ability_score(), Rules.roll_ability_score(), Rules.roll_ability_score()
        wis, int, cha = Rules.roll_ability_score(), Rules.roll_ability_score(), Rules.roll_ability_score()
        obj.model = ClassModel(uuid4(), name, 1, cls.HIT_DIE_SIZE, cls.HIT_DIE_SIZE, armor.armor_class, str, dex, con, wis, int, cha, 0, 18)
        obj.set_armor_class(armor)
        for _ in range(1,level):
            obj.add_level()
        obj.update()
        obj.current_hp = obj.model.max_hit_points
        obj.is_alive = True
        logging.debug(f"CHARACTER,NEW,{character_str(obj.model)}")
        return obj

    @classmethod
    def load(cls, model):
        obj = cls()
        obj.model = model
        obj.current_hp = obj.model.max_hit_points
        obj.is_alive = True
        obj.update()
        logging.debug(f"CHARACTER,NEW,{character_str(obj.model)}")
        return obj

    def __init__(self):
        super().__init__()
        self.model = None

    def add_experience(self, amount):
        self.model.experience += amount
        if self.model.experience >= BaseClass.EXPERIENCE_TABLE[self.model.hit_dice]:
            self.add_level()
            self.model.experience = min(self.model.experience, BaseClass.EXPERIENCE_TABLE[self.model.hit_dice]-1)

    def add_level(self):
        if self.model.hit_dice < 20:
            self.model.hit_dice += 1
            self.model.rolled_hit_points += roll_die(self.__class__.HIT_DIE_SIZE)
            self.model.max_hit_points = Rules.get_max_hit_points(self.model.hit_dice, self.model.rolled_hit_points, self.__class__.HIT_DIE_SIZE, self.model.constitution)

class Fighter(BaseClass):

    HIT_DIE_SIZE = 10

    def __init__(self):
        super().__init__()
        self.bonus_actions.append(SecondWind(self))
        self.skill_fighting_style = self.skill_fighting_style | Rules.FightingStyle.DEFENSE

    def ability_score_improvement(self):
        inc = 2
        if self.model.strength <= 18:
            self.model.strength += 2
            inc -= 2
        elif self.model.strength == 19:
            self.model.strength += 1
            inc -= 1
        if self.model.constitution <= 18 and inc > 0:
            self.model.constitution += inc
            inc = 0
        elif self.model.constitution == 19 and inc > 0:
            self.model.constitution += 1
            inc -= 1
        if self.model.dexterity <= 18 and inc > 0:
            self.model.dexterity += inc
            inc = 0
        elif self.model.dexterity == 19 and inc > 0:
            self.model.dexterity += 1
            inc -= 1

    def add_level(self):
        super().add_level()
        match self.model.hit_dice:
            case 2:
                self.skill_action_surge += 1
            case 3:
                self.skill_critical_hit -= 1
            case 4:
                self.ability_score_improvement()
            case 5:
                extra_attack = ExtraAttack(self, self._actions[0])
                self._actions.insert(0, extra_attack)
                self.skill_extra_attack += 1
            case 6:
                self.ability_score_improvement()
            #TODO case 7: Remarkable Athlete
            case 8:
                self.ability_score_improvement()
            #TODO case 9: add Indomitable Reroll saving throw, once per long rest
            case 10: 
                self.skill_fighting_style = self.skill_fighting_style | Rules.FightingStyle.DUELING
            case 11:
                self._actions[0].number_of_attacks += 1
                self.skill_extra_attack += 1
            case 12:
                self.ability_score_improvement()
            #TODO case 13: add one more use of Indomitable (9th level)
            case 14:
                self.ability_score_improvement()
            case 15:
                self.skill_critical_hit -= 1
            case 16:
                self.ability_score_improvement()
            #TODO case 17: add one more use of Indomitable (9th level)
            #TODO case 18: 
            case 19:
                self.ability_score_improvement()
            case 20:
                self._actions[0].number_of_attacks += 1
                self.skill_extra_attack += 1
        self.update()

class BaseParty:
    "A party of characters"

    def __init__(self):
        self._uuid = uuid4()
        self._members = []
        self._fallen = []
        logging.debug(f"PARTY,NEW,{self._uuid}")

    def get_model(self):
        model = []
        for member in self._members:
            model.append(PartyModel(self._uuid, member.model.simulation, member.model.uuid))
        for fallen in self._fallen:
            model.append(PartyModel(self._uuid, fallen.model.simulation, fallen.model.uuid))
        return model

    def get_size(self):
        "Number of members in party"
        return len(self._members)

    def shuffle(self):
        "Shuffle combatants"
        shuffle(self._members)

    def end_year(self):
        "Increment the age of all members"
        pass

    def long_rest(self):
        "Heal all members to full hit points"
        for member in self._members:
            member.current_hp = member.model.max_hit_points
            member.is_alive = True
            for action in member._actions:
                action.short_rested = True
                action.long_rested = True

    def add_member(self, member):
        "Add a member to the party"
        self._members.append(member)
        logging.debug(f"PARTY,ADD_MEMBER,{self._uuid},{member.model.uuid}")

    def get_member(self, index):
        "Return the character on the index"
        return self._members[index]

    def get_random_melee_target(self):
        "Return a random member open to be a melee target"
        if self.any_alive():
            while True:
                member = choice(self._members)
                if member.is_alive:
                    return member
        return None

    def any_alive(self):
        "Returns true if there is a combatant"
        return any(member.is_alive for member in self._members)

    def fall_members(self):
        "Move fallen members to out of combat list"
        fallen = (member for member in self._members if not member.is_alive)
        for dead in fallen:
            self._members.remove(dead)
            self._fallen.append(dead)

    def get_xp_from_fallen(self):
        xp = 0
        for dead in self._fallen:
            xp += dead.model.hit_dice * 200
        return xp

    def remove_dead(self):
        "Clear all out of combat and fallen members"
        data = []
        fallen = (member for member in self._members if not member.is_alive)
        for dead in fallen:
            self._members.remove(dead)
            data.append(dead.model.__dict__)
        for f in self._fallen:
            data.append(f.model.__dict__)
        db = Database()
        db.insert_many_fighters(data)
        self._fallen.clear()

    def act(self, enemies):
        "Act on a turn"
        if enemies.any_alive():
            for member in self._members:
                member.act(self._members, enemies)
            enemies.fall_members()

class ClassParty(BaseParty):

    def add_experience(self, experience):
        party_size = len(self._members)
        if party_size > 0:
            xp_share = round(experience/party_size)
            for member in self._members:
                member.add_experience(xp_share)

    def end_year(self):
        super().end_year()
        for member in self._members:
            member.model.age += 1
