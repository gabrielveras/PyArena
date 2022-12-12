
from dataclasses import dataclass
from uuid import UUID

@dataclass
class ArenaModel:
    uuid:UUID
    number_of_years:int
    number_of_fighters:int
    fights_per_year:int
    max_turns:int
    #timestamp:int

@dataclass
class CharacterModel:
    uuid:UUID
    simulation:UUID
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
    #TODO timestamp:int

@dataclass
class ClassModel(CharacterModel):
    experience:int
    age:int

@dataclass
class PartyModel:
    uuid:UUID
    simulation:UUID
    member:UUID
    #TODO timestamp:int
