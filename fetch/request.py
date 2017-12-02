import dota2api
import time
from ..config import STEAM_API_KEY


api = dota2api.Initialise(STEAM_API_KEY)


def get_recent_matches(number=500, max_overload=1, **kwargs):

    def get_match_history_wrapper(max_overload, **kwargs):
        matches = list()

        try:
            matches = api.get_match_history(**kwargs)["matches"]
        except Exception:
            pass

        if not matches:
            if max_overload > 0:
                time.sleep(3)
                matches = get_match_history_wrapper(max_overload-1, **kwargs)
            else:
                print("History Request Denied: {}".format(kwargs))

        return matches

    matches = get_match_history_wrapper(max_overload, matches_requested=number, **kwargs)
    rest_number = number - len(matches)

    if matches and rest_number > 0:
        kwargs["start_at_match_id"] = matches[-1]["match_id"]-1
        matches.extend(get_recent_matches(number=rest_number, max_overload=max_overload, **kwargs))

    return matches


def get_details_of_matches(matches, max_overload=1):

    def get_match_details_wrapper(max_overload, match_id):
        details = dict()

        try:
            details = api.get_match_details(match_id)
        except Exception as e:
            pass

        if not details:
            if max_overload > 0:
                time.sleep(3)
                details = get_match_details_wrapper(max_overload-1, match_id)
            else:
                print("Details Request Abandoned: {}".format({"match_id": match_id}))

        return details

    match_details = []
    for each in matches:
        details = get_match_details_wrapper(max_overload, each["match_id"])
        if details:
            match_details.append(details)
    return match_details


def merge_matches(matches, others):
    merged_matches = matches

    ori_ids = [each["match_id"] for each in matches]
    for each in others:
        if each["match_id"] not in ori_ids:
            merged_matches.append(each)

    return merged_matches


def filter_abandoned_matches(matches):
    finished_matches = []

    for each in matches:
        for player in each["players"]:
            if player["leaver_status"] > 1:
                break
        else:
            finished_matches.append(each)

    return finished_matches


def filter_faked_matches(matches):
    real_matches = []

    for each in matches:
        eligible = True

        for player in each["players"]:
            if "ability_upgrades" not in player.keys():
                eligible = False
                break

            if not player["item_0"] and not player["item_1"] and not player["item_2"]:
                if not player["item_3"] and not player["item_4"] and not player["item_5"]:
                    eligible = False
                    break

        if eligible:
            real_matches.append(each)

    return real_matches


def filter_arcade_matches(matches):
    formal_matches = []

    for each in matches:
        if each["game_mode"] in [1, 2, 3, 4, 22]:
            formal_matches.append(each)

    return formal_matches


def fetch_eligible_matches(num_per_account=500, accounts=[], max_overload=1):
    matches = []
    for each in accounts:
        matches = merge_matches(matches, get_recent_matches(num_per_account, max_overload, account_id=each, min_players=10))

    print("Found {} matches, fetching details...".format(len(matches)))
    matches = get_details_of_matches(matches, max_overload)

    print("Filtering matches...")
    matches = filter_abandoned_matches(matches)
    matches = filter_faked_matches(matches)
    matches = filter_arcade_matches(matches)

    print("Obtained {} matches...".format(len(matches)))
    return matches