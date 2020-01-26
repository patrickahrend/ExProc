# Description of this script and its abilities

# Use this url to get all of your cards

# Imports
import pandas as pd
import json
import requests
import re
from pathlib import Path

# Setup/Import of data, variables, paths
EP_Path = Path(__file__).parents[1]
datastore_folder = Path(EP_Path, "datastore")
trello_folder = Path(EP_Path, "ExProcTrello/")


# Collecting some config variables
with open(datastore_folder / "ep_config.json", encoding="utf8") as datastore_auth:
    auth_json = json.load(datastore_auth)
    TRELLO_API_KEY = auth_json['api_keys']['TRELLO_API_KEY']
    TRELLO_TOKEN = auth_json['api_keys']['TRELLO_TOKEN']
    MAIN_TRELLO_BOARD_ID = auth_json['trello_links']['MAIN_TRELLO_BOARD_ID']


# Setting up other simple local variables
BASE_URL = "https://api.trello.com/1/"
BOARD_URL = "boards/%s/" % MAIN_TRELLO_BOARD_ID


def format_aPL_to_markdown(pjDict):
    pjDict: dict


def get_all_cards(): # Gets all the *visible/active* cards back as a nice json
    url = BASE_URL + BOARD_URL + "?cards=visible"
    querystring = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    response = requests.get(url, params=querystring)
    print(response)
    return json.loads(response.text)['cards'] # Returns an array of cards


def find_card_by_name(substring):
    card_list = get_all_cards()
    for card in card_list:
        if substring in card['name']:
            print(card['name'], card['id'])
            print(card['desc'])
            print(card['shortUrl'], card['url'])
            return card
    print("Card not found.")
    return None

def update_pj_status_board(activeProjectListFromEPTodo, activeThreadListFromEPTodo):
    # First organize projects into their respective domains
    projects_by_domain = {}
    for pj in activeProjectListFromEPTodo:
        try:
            projects_by_domain[pj['domain']].append(pj)
        except KeyError:
            projects_by_domain[pj['domain']] = [pj]

    # Collect the card description template and prepare to fill it in
    with open(trello_folder / "template-pjstatusboard.txt", encoding="utf8") as template:
        statusboardcard_url = template.readline()[:-1]
        statusboardcard_desc = template.read()

    # Iter through data and insert into card description
    updated_card_desc = statusboardcard_desc
    for dom, pjs in projects_by_domain.items():
        # Format the projects before placing them into the respective placeholder
        text_to_insert = "\n".join([">" + pj['name'] + ', '.join([thread['content'] for thread in activeThreadListFromEPTodo if thread['project_id'] == pj['id']]) for pj in pjs])
        updated_card_desc = re.sub("{" + dom + "}", text_to_insert, updated_card_desc)

    # Clean up whatever empty tags (ie "{ETPG}") still remain in the updated_card_desc
    updated_card_desc = re.sub("{[A-z]+}", "", updated_card_desc)

    # Finally, updating our changes
    querystring = {"key":TRELLO_API_KEY, "token":TRELLO_TOKEN, "desc":updated_card_desc}
    response = requests.put(statusboardcard_url, params=querystring)
    print(statusboardcard_url)
    print(response)

def update_soc_status_board():
    # Collect and organize the data first
    people_cats = ['Five', 'Fifteen', 'Fifty', 'Forever', 'Family', 'Figures']
    people_by_cat = {}
    with open(datastore_folder / "Circles.csv", encoding="utf8") as circles:
        circles_df = pd.read_csv(circles, index_col="Name")
    for cat in people_cats:
        people_by_cat[cat] = circles_df.loc[circles_df.Group == cat]

    # Collect the card description template and prepare to fill it in
    with open(trello_folder / "template-socstatusboard.txt", encoding="utf8") as template:
        statusboardcard_url = template.readline()[:-1]
        statusboardcard_desc = template.read()

    # Iter through data and insert into card description
    updated_card_desc = statusboardcard_desc
    for cat, people in people_by_cat.items():
        # Format the projects before placing them into the respective placeholder

        text_to_insert = "\n".join([index for index, row in people.iterrows()])

        updated_card_desc = re.sub("{" + cat + "}", text_to_insert, updated_card_desc)

    # Lastly, update changes to card
    querystring = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN, "desc": updated_card_desc}
    response = requests.put(statusboardcard_url, params=querystring)

    print(statusboardcard_url)
    print(response)
    return response