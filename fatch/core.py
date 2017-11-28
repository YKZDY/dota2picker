import json
from ..config import ACCOUNTS_ID, JSON_PATH
from .request import fatch_eligible_matches, merge_matches


def fatch_to_json():
    matches = fatch_eligible_matches(accounts=ACCOUNTS_ID)

    with open(JSON_PATH, "w") as json_file:
        json_file.write(json.dumps(matches))


def load_from_json():
    with open(JSON_PATH, "r") as f:
        matches = json.loads(f.read())

    return matches


def merge_to_json():
    with open(JSON_PATH, "r") as f:
        matches = json.loads(f.read())

    matches = merge_matches(matches, fatch_eligible_matches(accounts=ACCOUNTS_ID))

    with open(JSON_PATH, "w") as json_file:
        json_file.write(json.dumps(matches))