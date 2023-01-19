
from dataclasses import dataclass
from uuid import UUID

@dataclass
class ArenaModel:
    uuid:UUID
    number_of_years:int
    number_of_fighters:int
    fights_per_year:int
    max_turns:int

@dataclass
class MonsterMetricModel:
    uuid:UUID
    fighter_level:int
    number_of_fighters:int
    number_of_fights:int

def monster_metric_str(m:MonsterMetricModel):
    return f"{m.uuid},{m.fighter_level},{m.number_of_fighters},{m.number_of_fights}"

@dataclass
class CharacterModel:
    uuid:UUID
    name:str
    hit_dice:int
    max_hit_points:int
    rolled_hit_points:int
    armor_class:int
    strength:int
    dexterity:int
    constitution:int
    wisdom:int
    intelligence:int
    charisma:int

def character_str(m:CharacterModel):
    return f"{m.uuid},{m.name},{m.hit_dice},{m.max_hit_points},{m.rolled_hit_points},{m.strength},{m.dexterity},{m.constitution},{m.wisdom},{m.intelligence},{m.charisma}"

@dataclass
class ClassModel(CharacterModel):
    experience:int
    age:int

@dataclass
class PartyModel:
    uuid:UUID
