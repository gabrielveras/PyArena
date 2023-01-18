from character import BaseParty
from arena_utils import flip_coin

class FightManager:

    MAX_TURNS = 20

    @classmethod
    def fight(cls, party_1:BaseParty, party_2:BaseParty):
        "Two parties fight. Returns True if Party 1 wins or False if Party 2 wins."
        ellapsed_turns = 0
        initiative = flip_coin()
        party_1_is_alive = party_1.any_alive()
        party_2_is_alive = party_2.any_alive()
        while ellapsed_turns < cls.MAX_TURNS and party_1_is_alive and party_2_is_alive:
            ellapsed_turns += 1
            if initiative:
                party_1.act(party_2)
                party_2.act(party_1)
            else:
                party_2.act(party_1)
                party_1.act(party_2)
            party_1_is_alive = party_1.any_alive()
            party_2_is_alive = party_2.any_alive()
        if party_1_is_alive == party_2_is_alive:
            return flip_coin()
        else:
            return party_1_is_alive
