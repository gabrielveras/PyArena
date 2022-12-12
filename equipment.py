"Equipments for characters"

from enum import auto, IntEnum, Enum, Flag

class ArmorEnum(IntEnum):
    "Armor class"

    UNARMORED = 10
    LEATHER = 12
    CHAIN = 16
    PLATE = 18

class Armor:

    class Type(Enum):
        LIGHT = 2
        MEDIUM = 1
        HEAVY = 0

    def __init__(self, name, armor_class, min_strength, stealth_disadvantage, weight):
        self.name = name
        self.armor_class = armor_class
        self.min_strength = min_strength
        self.stealth_disadvantage = stealth_disadvantage
        self.weight = weight

    def get_armor_class(self, dexterity_modifier):
        return self.armor_class + dexterity_modifier

class MediumArmor(Armor):
    def __init__(self, name, armor_class, min_strength, stealth_disadvantage, weight):
        super().__init__(name, armor_class, min_strength, stealth_disadvantage, weight)

    def get_armor_class(self, dexterity_modifier):
        return self.armor_class + min(2, dexterity_modifier)

class HeavyArmor(Armor):
    def __init__(self, name, armor_class, min_strength, stealth_disadvantage, weight):
        super().__init__(name, armor_class, min_strength, stealth_disadvantage, weight)

    def get_armor_class(self, dexterity_modifier):
        return self.armor_class

class ArmorList:
    UNARMORED:Armor = Armor("unarmored", 10, 99, False, 0)
    PADDED:Armor = Armor("padded", 11, 99, True, 8)
    LEATHER:Armor = Armor("leather", 11, 99, False, 10)
    STUDDED_LEATHER:Armor = Armor("leather", 12, 99, False, 13)
    HIDE:MediumArmor = MediumArmor("hide", 12, 99, False, 12)
    CHAIN_SHIRT:MediumArmor = MediumArmor("chain shirt", 13, 99, False, 20)
    SCALE_MAIL:MediumArmor = MediumArmor("scale_mail", 14, 99, True, 45)
    BREASTPLATE:MediumArmor = MediumArmor("breastplate", 14, 99, False, 20)
    HALF_PLATE:MediumArmor = MediumArmor("half plate", 15, 99, True, 40)
    RING_MAIL:HeavyArmor = HeavyArmor("ring mail", 14, 99, True, 40)
    CHAIN_MAIL:HeavyArmor = HeavyArmor("chain mail", 16, 13, True, 55)
    SPLINT:HeavyArmor = HeavyArmor("splint", 17, 15, True, 60)
    PLATE:HeavyArmor = HeavyArmor("plate", 18, 15, True, 65)
    NATURAL_11:Armor = HeavyArmor("natural (11)", 11, 99, False, 0)
    NATURAL_12:Armor = HeavyArmor("natural (12)", 12, 99, False, 0)
    NATURAL_13:Armor = HeavyArmor("natural (13)", 13, 99, False, 0)
    NATURAL_14:Armor = HeavyArmor("natural (14)", 14, 99, False, 0)

class WeaponProperty(Flag):
    NONE = 0
    AMMUNITION = auto()
    FINESSE = auto()
    HEAVY = auto()
    LIGHT = auto()
    LOADING = auto()
    RANGE = auto()
    REACH = auto()
    SPECIAL = auto()
    THROWN = auto()
    TWO_HANDED = auto()
    VERSATILE = auto()

class Weapon:
    def __init__(self, name, damage, two_handed):
        self._name = name
        self._damage = damage
        self._two_handed = two_handed

class WeaponList:
    DAGGER:Weapon = Weapon("dagger", 4, False)
    SWORD:Weapon = Weapon("sword", 6, False)
