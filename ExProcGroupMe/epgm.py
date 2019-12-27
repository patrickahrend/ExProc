# Imports
import re
import requests
import json
from pathlib import Path

# Setup/Import of data, variables, paths
EP_Path = Path(__file__).parents[0]
print("hey, this is odd", EP_Path)
datastore_folder = Path(EP_Path, "datastore")
groupme_folder = Path(EP_Path, "ExProcGroupMe/")

# Collecting some config variables
with open(datastore_folder / "auth.json", encoding="utf8") as datastore_auth:
    auth_json = json.load(datastore_auth)
    GROUPME_TOKEN = auth_json['GROUPME_TOKEN']


# Setting up other simple local variables
BASE_URL = "https://api.groupme.com/v3"
GROUP_URL = "/groups/{}/messages?limit=100" # The {}'s will be replaced with group_id by format()
AFTER_MSG = "&after_id={}"

def find_url_in_text(string):
    # findall() has been used with valid conditions for urls in string
    if string:
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return ""

def parse_all_groups_messages(): #Finds URLs in all included group chats, and returns them as a dictionary with lists
    with open('gm_data.json') as json_file:
        gm_data = json.load(json_file)

    all_messages = {}
    url_count = 0
    for group, values in gm_data['groups'].items():
        group_msgs = []
        try:
            urls_returned, gm_data['groups'][group]['last_read_msg_id'] = parse_group_since_last(values['group_id'], values['last_read_msg_id'])
            url_count += len(urls_returned)
        except KeyError:
            print("Warning: No last message id provided for group: ", group, "; older messages won't be parsed.")
            urls_returned,  gm_data['groups'][group]['last_read_msg_id'] = parse_group(values['group_id'])
            url_count += len(urls_returned)

        all_messages[group] = urls_returned

    print("Totals URLs found: ", url_count)
    with open('gm_data.json', "w") as json_file:
        json.dump(gm_data, json_file)
        print("JSON Data saved successfully.")
    with open('latest_gm_msgs.txt', "w") as msgs_file:
        json.dump(all_messages, msgs_file)
        print("Links successfully saved to file.")



def parse_group(group_id): # Returns list of URL's, along with the last message_id for storage.
    response = requests.get(BASE_URL + GROUP_URL.format(group_id) + GROUPME_TOKEN).content.decode("utf8")
    json_content = json.loads(response)

    messages = json_content['response']['messages']
    urls_found = []
    newest_msg_id = messages[0]['id']

    for msg in messages:
        urls_found.extend(find_url_in_text(msg['text']))
    return urls_found, newest_msg_id


def parse_group_since_last(group_id, last_read):
    response = requests.get(BASE_URL + GROUP_URL.format(group_id) + AFTER_MSG.format(last_read) + GROUPME_TOKEN).content.decode("utf8")
    json_content = json.loads(response)

    messages = json_content['response']['messages']
    urls_found = []
    try:
        last_read_id = messages[-1]["id"]
    except IndexError:
        print("There have been no additional messages in the selected group: ", group_id)
        return [], last_read

    for msg in messages:
        urls_found.extend(find_url_in_text(msg['text']))

    if len(messages) > 99: # Max size, more messages possible. Recurse through
        urls_returned, last_read_id = parse_group_since_last(group_id, last_read_id)
        urls_found.extend(urls_returned)

    return urls_found, last_read_id

parse_all_groups_messages()