import logging

from uuid import uuid4

from actions import MeleeWeaponAttack
from character import BaseParty, ClassParty, Fighter
from fight_manager import FightManager
from models import MonsterMetricModel, monster_metric_str
from monsters import BaseMonster

class MonsterMetrics:

    def __init__(self, fighter_level:int = 1, number_of_fighters:int = 40, number_of_fights:int = 20):
        self.model = MonsterMetricModel(uuid4(), fighter_level, number_of_fighters, number_of_fights)
        logging.debug(f"MONSTER_METRICS,NEW,{monster_metric_str(self.model)}")

    def single_matchup(self, monster_name):
        for _ in range(self.model.number_of_fights):
            monsters = BaseParty()
            monster = BaseMonster.create_by_name(monster_name)
            monsters.add_member(monster)
            players = BaseParty()
            for _ in range(self.model.number_of_fighters):
                player:Fighter = Fighter.create(level=self.model.fighter_level)
                player.append_action(MeleeWeaponAttack.create_greataxe(player))
                players.add_member(player)
            FightManager.fight(players, monsters)

if __name__ == "__main__":
    logging.basicConfig(filename=f"test.log", filemode='w', level=logging.DEBUG, format="%(message)s")
    logging.debug("START")
    metrics = MonsterMetrics()
    metrics.single_matchup("goblin")
    print(f"ID: {str(metrics.model.uuid)}")
    logging.debug("END")
