from equipment import WeaponProperty

foo = WeaponProperty.LIGHT

bar = bool(foo & WeaponProperty.FINESSE)

print(bar)