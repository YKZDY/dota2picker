# # -*- coding: utf-8 -*-
import sys
from Qt import QtWidgets
import dota2api
from .fatch.core import fatch_to_json, merge_to_json
from .analyze.core import refresh_stats, get_recommended_list
from .gui.core import Dota2Picker
from .config import STEAM_API_KEY


api = dota2api.Initialise(STEAM_API_KEY)


def refresh_database():
    print("Updating Dota2api references...")
    api.update_heroes()
    api.update_game_items()

    print("Fatching Matches' from Steam...")
    fatch_to_json()

    print("Analyzing Matches' Data...")
    refresh_stats()


def update_database():
    print("Updating Dota2api references...")
    api.update_heroes()
    api.update_game_items()

    print("Fatching Matches' from Steam...")
    merge_to_json()

    print("Analyzing Matches' Data...")
    refresh_stats()


def picker_cli(allies, enemies, language="en"):
    recommended_list = get_recommended_list(allies, enemies, language)

    for each in recommended_list:
        hero_name = each.hero_name.ljust(20)
        sum_score = str(round(each.sum_score*100, 2)).ljust(10)
        hero_score = str(round(each.hero_score*100, 2)).ljust(9)
        coop_score = str(round(each.coop_score*100, 2)).ljust(9)
        anti_score = str(round(each.anti_score*100, 2)).ljust(9)
        print("{} Sum Score: {} Hero Score: {} Coop Score: {} Anti Score: {}".format(hero_name, sum_score, hero_score, coop_score, anti_score))


def picker_gui(language="en"):
    app = QtWidgets.QApplication(sys.argv)
    window = Dota2Picker(language)
    window.show()
    sys.exit(app.exec_())
