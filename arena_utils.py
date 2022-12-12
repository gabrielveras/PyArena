"""Utilities for use in PyArena"""

from random import seed
from random import randint, getrandbits

def pairwise(iterable):
    "Return a pair of elements for use in loops"
    a = iter(iterable)
    return zip(a, a)

def grouped(iterable, n):
    "Return a group of N elements for use in loops"
    return zip(*[iter(iterable)]*n)

def flip_coin() -> bool:
    "Roll a dice of the desired size"
    return bool(getrandbits(1))

def roll_die(size:int) -> int:
    "Roll a dice of the desired size"
    if size > 0:
        return randint(1,size)
    return 0

def roll_dice(number:int, size:int) -> list[int]:
    "Roll a number of dice of the desired size"
    if number > 0 and size > 0:
        dice = [randint(1,size) for i in range(number)]
        return dice
    return []

def roll_sum(number:int, size:int, drop_lowest:bool=False) -> int:
    "Roll a number of dice and return their sum"
    roll = roll_dice(number, size)
    return sum(roll) - min(roll)*drop_lowest

def get_ability_modifier(score:int) -> int:
    "Returns the ability modifier based on the ability score"
    _modifiers = [-3,-2,-2,-1,-1,-1,0,0,0,0,1,1,1,2,2,3]
    if 3 <= score <= 18:
        return _modifiers[score-3]
    return 0

seed(0)
