import dota2api
import time
import json
from ..config import STEAM_API_KEY, HEROES_CN_PATH


api = dota2api.Initialise(STEAM_API_KEY)
heroes = api.get_heroes()["heroes"]

with open(HEROES_CN_PATH, "r", encoding="utf8") as f:
    heroes_cn = json.loads(f.read())


def timestamp_datetime(value):
    pattern = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(pattern, value)
    return dt


def get_heroes_id():
    return [each["id"] for each in heroes]


def get_hero_name_en(hero_id):
    for each in heroes:
        if each["id"] == hero_id:
            name = each["localized_name"]
            break
    else:
        raise RuntimeError("Invalid Hero ID: {}".format(hero_id))
    return name


def get_hero_name_cn(hero_id):
    for each in heroes_cn:
        if each["id"] == hero_id:
            name = each["name_cn"]
            break
    else:
        raise RuntimeError("Invalid Hero ID: {}".format(hero_id))
    return name
