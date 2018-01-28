from Qt import QtWidgets
from .widgets import HeroDropedMenu, DisplayHeroList
from ..analyze.core import get_team_win_rate


class Dota2Picker(QtWidgets.QWidget):
    def __init__(self, language="en"):
        super(Dota2Picker, self).__init__()
        self.size = {"w": 600, "h": 760}
        self.title = "Dota2 Picker"
        self.language = language
        self.allies = [HeroDropedMenu(language), HeroDropedMenu(language), HeroDropedMenu(language), HeroDropedMenu(language), HeroDropedMenu(language)]
        self.enemies = [HeroDropedMenu(language), HeroDropedMenu(language), HeroDropedMenu(language), HeroDropedMenu(language), HeroDropedMenu(language)]
        self.moniter = DisplayHeroList(language)
        self.refresh = QtWidgets.QPushButton("Refresh")
        self.init_ui()
        self.init_connection()

    def init_ui(self):
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        self.setWindowTitle(self.title)
        self.setGeometry(
            (screen_size.width() - self.size["w"]) / 2,
            (screen_size.height() - self.size["h"]) / 2,
            self.size["w"], self.size["h"])

        allies_lay = QtWidgets.QVBoxLayout()
        allies_lay.addWidget(QtWidgets.QLabel("Allies:"))
        for each in self.allies:
            allies_lay.addWidget(each)

        enemies_lay = QtWidgets.QVBoxLayout()
        enemies_lay.addWidget(QtWidgets.QLabel("Enemies:"))
        for each in self.enemies:
            enemies_lay.addWidget(each)

        heroes_lay = QtWidgets.QHBoxLayout()
        heroes_lay.addLayout(allies_lay)
        heroes_lay.addLayout(enemies_lay)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(heroes_lay)
        layout.addWidget(self.moniter)
        layout.addWidget(self.refresh)

        self.setLayout(layout)

    def init_connection(self):
        self.refresh.clicked.connect(self.refresh_callback)

    def refresh_callback(self):
        self.moniter.refresh_data([ally.content for ally in self.allies if ally.content], 
            [enemy.content for enemy in self.enemies if enemy.content])
        print(get_team_win_rate([ally.content for ally in self.allies if ally.content], 
            [enemy.content for enemy in self.enemies if enemy.content]))
