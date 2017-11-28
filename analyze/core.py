from .objects import Statistics, HeroScore
from ..utils.core import get_heroes_id


stats = Statistics()


def refresh_stats():
    stats.refresh()


def win_rate(hero_id):
    return stats.win_rate(hero_id)


def win_rate_with_ally(hero_id, ally_id):
    return stats.win_rate_with_ally(hero_id, ally_id)


def win_rate_with_enemy(hero_id, enemy_id):
    return stats.win_rate_with_enemy(hero_id, enemy_id)


def get_recommended_list(allies, enemies, language="en"):
    recommended_list = [HeroScore(hero_id, language) for hero_id in get_heroes_id() if hero_id not in allies + enemies]

    for hero_score in recommended_list:
        for ally in allies:
            hero_score.add_ally(ally)
        for enemy in enemies:
            hero_score.add_enemy(enemy)

    recommended_list.sort(key=lambda hero_score:hero_score.sum_score, reverse=True)
    return recommended_list


def get_team_win_rate(allies, enemies):
    ally_score = 0
    enemy_score = 0

    for hero in allies:
        each_score = HeroScore(hero)
        for each in allies:
            each_score.add_ally(each)
        for each in enemies:
            each_score.add_enemy(each)
        ally_score += each_score.sum_score

    for hero in enemies:
        each_score = HeroScore(hero)
        for each in enemies:
            each_score.add_ally(each)
        for each in allies:
            each_score.add_enemy(each)
        enemy_score += each_score.sum_score

    print(ally_score, " ", enemy_score)

    return ally_score/enemy_score