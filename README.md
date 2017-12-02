# Dota2Picker

Dota2Picker is a simple Dota2 hero picking helper by analyzing historical matches of provided accounts in config.py

### Dependence

[Dota2api](https://github.com/joshuaduffy/dota2api)

[Qt.py](https://github.com/mottosso/Qt.py)

### Configuration

First of all, you need to apply a steam [api key](https://steamcommunity.com/dev/apikey), then fill out your key in config.py to make Dota2Picker have permission to access the Steam server.

There's an account list in config.py which will be used to grab data from server. Because of the restrict from Steam, right now Dota2Picker can only access 500 matches for each account. And the matches from the different accounts will be merged automatically after fatching.

### Usage

Before using Dota2Picker, you must fatch the data from server to your local database.

    from dota2picker.main import refresh_database, update_database

    // Fatch by overwriting old database.
    refresh_database()

    // Fatch then merge new data to existing database.
    update_database()

Run Dota2Picker !!!

    from dota2picker.main import picker_cli, picker_gui

    // By inputing 0-5 allies' hero ID and 0-5 enemies' hero ID, picker_cli will 
    // print a ordered list of suggesting heroes.
    picker_cli([ally_one, ally_two, ...], [enemy_one, enemy_two, ...], language="en"/"cn")

    // Run graphics user interface. (powerd by qt)
    picker_gui(language="en"/"cn")
