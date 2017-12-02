from Qt import QtWidgets
from ..analyze.core import get_recommended_list
from ..utils.core import get_heroes_id, get_hero_name_en, get_hero_name_cn


class HeroDropedMenu(QtWidgets.QWidget):
    def __init__(self, language="en"):
        super(HeroDropedMenu, self).__init__()

        self.language = language
        self.hero_list = [{"id": 0, "name": "None"}]

        if language == "en":
            for hero_id in get_heroes_id():
                self.hero_list.append({"id": hero_id, "name": get_hero_name_en(hero_id)})
        elif language == "cn":
            for hero_id in get_heroes_id():
                self.hero_list.append({"id": hero_id, "name": get_hero_name_cn(hero_id)})
        else:
            raise Exception("Invalid Language: %s" % language)

        self.menu = QtWidgets.QComboBox()
        for each in self.hero_list:
            self.menu.addItem(each["name"])

        self.init_ui()

    @property
    def content(self):
        return self.hero_list[self.menu.currentIndex()]["id"]

    def init_ui(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.menu)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class DisplayHeroList(QtWidgets.QWidget):
    def __init__(self, language="en"):
        super(DisplayHeroList, self).__init__()

        self.language = language
        self.table = QtWidgets.QTableWidget()
        self.init_ui()

    def refresh_data(self, allies, enemies):
        data = get_recommended_list(allies, enemies, self.language)
        self.table.setRowCount(len(data))
        for index, value in enumerate(data):
            self.table.setItem(index, 0, QtWidgets.QTableWidgetItem(value.hero_name))
            self.table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(round(value.sum_score*100, 2))))
            self.table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(round(value.hero_score*100, 2))))
            self.table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(round(value.coop_score*100, 2))))
            self.table.setItem(index, 4, QtWidgets.QTableWidgetItem(str(round(value.anti_score*100, 2))))

    def init_ui(self):
        layout = QtWidgets.QHBoxLayout()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Total Score", "Hero Score", "Coop Score", "Anti Score"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
