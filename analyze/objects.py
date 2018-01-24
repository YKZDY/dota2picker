import os
import numpy as np
from ..config import STEAM_API_KEY, NPY_PATH
from ..fetch.core import load_from_json
from ..utils.core import get_heroes_id, get_hero_name_en, get_hero_name_cn


class Statistics(object):

    # [main hero] [mate hero] [0=ally,1=enemy] [0=win,1=sum]

    def __init__(self):
        super(Statistics, self).__init__()
        self.data = np.load(NPY_PATH) if os.path.isfile(NPY_PATH) else np.zeros([])

    def refresh(self):
        max_id = 0
        for hero_id in get_heroes_id():
            if hero_id > max_id:
                max_id = hero_id

        self.data = np.zeros([max_id+1, max_id+1, 2, 2])
        self.update()
        np.save(NPY_PATH, self.data)

    def update(self):

        def get_relation(one, two):
            return 0 if (one-4.5)*(two-4.5) > 0 else 1

        def is_win(index, result):
            result = 1 if result else 0
            return 0 if (index-4.5)*(result-0.5) > 0 else 1

        matches = load_from_json()

        for each in matches:
            heroes = [player["hero_id"] for player in each["players"]]
            result = each["radiant_win"]
            for index_x, hero_x in enumerate(heroes):
                for index_y, hero_y in enumerate(heroes):
                    self.data[hero_x][hero_y][get_relation(index_x, index_y)][1] += 1
                    self.data[hero_x][hero_y][get_relation(index_x, index_y)][0] += is_win(index_x, result)

    @staticmethod
    def get_percent(num, sum_num):
        if sum_num == 0:
            return 0
        else:
            return num/sum_num

    def win_rate(self, hero_id):
        return self.get_percent(self.data[hero_id][hero_id][0][0], self.data[hero_id][hero_id][0][1])

    def win_rate_with_ally(self, hero_id, ally_id):
        return self.get_percent(self.data[hero_id][ally_id][0][0], self.data[hero_id][ally_id][0][1])

    def win_rate_with_enemy(self, hero_id, enemy_id):
        return self.get_percent(self.data[hero_id][enemy_id][1][0], self.data[hero_id][enemy_id][1][1])


class HeroScore(object):

    stats = Statistics()

    def __init__(self, hero_id, language="en"):
        super(HeroScore, self).__init__()
        self.hero_id = hero_id

        if language == "en":
            self.hero_name = get_hero_name_en(hero_id)
        elif language == "cn":
            self.hero_name = get_hero_name_cn(hero_id)
        else:
            raise Exception("Invalid Language: %s" % language)

        self.hero_score = self.stats.win_rate(hero_id)
        self.coop_score = 0
        self.anti_score = 0
        self.sum_score = self.hero_score

    def get_coop_score(self, ally_id):
        win_rate = self.stats.win_rate(ally_id)
        win_rate_with_ally = self.stats.win_rate_with_ally(ally_id, self.hero_id)
        return win_rate_with_ally - win_rate if win_rate and win_rate_with_ally else 0

    def get_anti_score(self, enemy_id):
        win_rate = self.stats.win_rate(enemy_id)
        win_rate_with_enemy = self.stats.win_rate_with_enemy(enemy_id, self.hero_id)
        return win_rate - win_rate_with_enemy if win_rate and win_rate_with_enemy else 0

    def update_sum(self):
        self.sum_score = self.hero_score + self.coop_score + self.anti_score

    def add_ally(self, ally_id):
        self.coop_score += self.get_coop_score(ally_id)
        self.update_sum()

    def add_enemy(self, enemy_id):
        self.anti_score += self.get_anti_score(enemy_id)
        self.update_sum()

    def del_ally(self, ally_id):
        self.coop_score -= self.get_coop_score(ally_id)
        self.update_sum()

    def del_enemy(self, enemy_id):
        self.anti_score -= self.get_anti_score(enemy_id)
        self.update_sum()
