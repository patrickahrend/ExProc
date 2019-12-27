# Description of this script and its abilities

# Imports
import json
import requests
import re
from pathlib import Path

# Setup/Import of data, variables, paths
EP_Path = Path(__file__).parents[1]
datastore_folder = Path(EP_Path, "datastore")
trello_folder = Path(EP_Path, "ExProcTrello/")


# Collecting some config variables
with open(datastore_folder / "auth.json", encoding="utf8") as datastore_auth:
    auth_json = json.load(datastore_auth)
    TRELLO_API_KEY = auth_json['TRELLO_API_KEY']
    TRELLO_TOKEN = auth_json['TRELLO_TOKEN']
    MAIN_TRELLO_BOARD_ID = auth_json['MAIN_TRELLO_BOARD_ID']

with open(trello_folder / "template-pjstatusboard.txt", encoding="utf8") as template:
    statusboardcard_url = template.readline()
    statusboardcard_desc = template.read()


# Setting up other simple local variables

def format_aPL_to_markdown(pjDict):
    pjDict: dict


def update_pj_status_board(activeProjectListFromEPTodo, activeThreadListFromEPTodo):
    # First organize projects into their respective domains
    projects_by_domain = {}
    for pj in activeProjectListFromEPTodo:
        try:
            projects_by_domain[pj['domain']].append(pj)
        except KeyError:
            projects_by_domain[pj['domain']] = [pj]

    # Collect the card description template and prepare to fill it in
    global statusboardcard_desc

    print(projects_by_domain)
    for dom, pjs in projects_by_domain.items():
        # Format the projects before placing them into the respective placeholder
        text_to_insert = "\n".join([">" + pj['name'] + ', '.join([thread['content'] for thread in activeThreadListFromEPTodo if thread['project_id'] == pj['id']]) for pj in pjs])
        updated_card_desc = re.sub("{" + dom + "}", text_to_insert, statusboardcard_desc)

    # Clean up whatever empty tags (ie "{ETPG}") still remain in the updated_card_desc
    updated_card_desc = re.sub("{[A-z]+}", "", updated_card_desc)

    # Finally, updating our changes
    querystring = {"key":TRELLO_API_KEY, "token":TRELLO_TOKEN, "desc":updated_card_desc}
    response = requests.put(statusboardcard_url, params=querystring)
    print(response)
