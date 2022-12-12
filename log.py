from character import BaseParty

class Console:

    CONFIG_FLAG = 2
    FLAG_START = 2
    FLAG_END_YEAR = 4
    FLAG_EACH_TURN = 8

    @staticmethod
    def print_start(number_of_years:int, number_of_fighters:int, fights_per_year:int):
        "Settings: X fighters for Y years with Z fights per year"
        if Console.FLAG_START & Console.CONFIG_FLAG:
            print(f"Settings: {number_of_fighters} fighters for {number_of_years} years with {fights_per_year} fights per year.")

    @staticmethod
    def print_end_year(year:int, highest_level:int, highest_age:int, oldest_age:int, oldest_level:int):
        if Console.FLAG_END_YEAR & Console.CONFIG_FLAG:
            print(f"Year {year}: Highest level is level {highest_level} and {highest_age} years old; Oldest is level {oldest_level} and {oldest_age} years old")

    @staticmethod
    def print_turn(party_1:BaseParty, party_2:BaseParty):
        if Console.FLAG_EACH_TURN & Console.CONFIG_FLAG:
            print(f"P1[{party_1.get_member(0).name} LVL {party_1.get_member(0).level} HP {party_1.get_member(0).current_hp}] vs P2[{party_1.get_member(0).name} LVL {party_2.get_member(0).level} HP {party_2.get_member(0).current_hp}]")
