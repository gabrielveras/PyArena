from uuid import uuid4

from character import BaseParty, ClassParty, Fighter
from fight_manager import FightManager
from monsters import BaseMonster
from models import MonsterMetricModel

class MonsterMetrics:

    def __init__(self, fighter_level:int = 1, number_of_fighters:int = 40, fights:int = 20):
        self._model = MonsterMetricModel(uuid4(), fighter_level, number_of_fighters, fights)

    def single_matchup(self, monster_name):
        for _ in range(self._model.fights):
            monsters = BaseParty()
            monster = BaseMonster.create_by_name(monster_name)
            monsters.add_member(monster)
            players = ClassParty()
            for _ in range(self._model.number_of_fighters):
                player = Fighter.create(level=self._model.fighter_level)
                players.add_member(player)
            FightManager.fight(players, monsters)

if __name__ == "__main__":
    metrics = MonsterMetrics()
    metrics.single_matchup()
    print(f"ID: {str(metrics._model.uuid)}")