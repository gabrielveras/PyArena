'''Arena simulation'''

from uuid import uuid4

from actions import MeleeWeaponAttack
from character import Fighter, ClassParty
from database import Database
from equipment import ArmorList
from fight_manager import FightManager
from models import ArenaModel

class Arena:

    NUM_SEQ:int = 0

    def __init__(self, number_of_years:int = 50, number_of_fighters:int = 100, fights_per_year:int = 12, max_turns:int = 20):
        self._model = ArenaModel(uuid4(), number_of_years, number_of_fighters, fights_per_year, max_turns)
        self._fighters:ClassParty = ClassParty()

    def run(self):
        "Run arena simulation"
        db = Database()
        db.insert_simulation(self._model)
        for year in range(0, self._model.number_of_years):
            for fight in range(0, self._model.fights_per_year):
                self.run_one_year()
            self.end_year(year)
        data = []
        for f in self._fighters._members:
            data.append(f.model.__dict__)
        db = Database()
        db.insert_many_fighters(data)

    def run_one_year(self):
        "Run one cycle of the simulation"
        size = self._fighters.get_size()
        for i in range(size, self._model.number_of_fighters):
            fighter:Fighter = Fighter.create(self._model.uuid, "John"+str(Arena.NUM_SEQ), 1, ArmorList.LEATHER)
            Arena.NUM_SEQ += 1
            fighter.append_action(MeleeWeaponAttack.create_greataxe(fighter))
            self._fighters.add_member(fighter)
        self._fighters.shuffle()
        for i in range(0, self._fighters.get_size(), 2):
            party_1 = ClassParty()
            party_1.add_member(self._fighters.get_member(i))
            party_2 = ClassParty()
            party_2.add_member(self._fighters.get_member(i+1))
            winner = FightManager.fight(party_1, party_2)
            if winner:
                party_1.add_experience(party_2.get_xp_from_fallen())
            else:
                party_2.add_experience(party_1.get_xp_from_fallen())
        self._fighters.remove_dead()
        self._fighters.long_rest()

    def end_year(self, year:int):
        "End of fighting year"
        self._fighters.end_year()

if __name__ == "__main__":
    arena = Arena()
    arena.run()
    print(f"ID: {str(arena._model.uuid)}")