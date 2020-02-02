# Script Description:
# Goal of this todoist main.py communicator is to create the connection, download the dataset, and then prepare data for other uses

# Imports
import copy
import todoist
import datetime
import json
import pytz
from pathlib import Path
from dateutil import parser  # to use the parser, parser.parse(some_str) - returns datetime

# Setup/Import of data, variables, paths

EP_Path = Path(__file__).parents[1]
datastore_folder = Path(EP_Path, "datastore")
todoist_folder = Path(EP_Path, "ExProcTodoist")

# Collecting some config variables
with open(datastore_folder / "ep_config.json", encoding="utf8") as datastore_auth:
    auth_json = json.load(datastore_auth)
    TODOIST_TOKEN = auth_json['api_keys']['TODOIST_TOKEN']

# Setting up other simple local variables
mytz = pytz.timezone('US/Central')

# Sync up the API
api = todoist.TodoistAPI(TODOIST_TOKEN)
api_response = api.sync()

# TODO: A Quality Control Check for Todoist, that not only identifies errors in my system, but fixes them
# (1) Ensures Threads and SubThreads adopt both the highest priority of their subTasks, and the latest Deadline amongst their subtasks
# (2) If it has a due_date, shouldn't it also have a Priority > 1? Hm.

# Better way to print out the api.state
# import pprint
# pp = pprint.PrettyPrinter(indent = 4, depth = 2)
# pp.pprint(api.state)

# Todo: Someday define top level domains programmatically
# Project Data Set Up Area ================================
# Project Color Dictionary - Based on color of the project, you can tell if it's Them, Me, Us, or Fun
domain_list = ["LM", "HWB", "ETPG", "EW", "CC", "Fam", "Int", "Soc", "Rec", "NV", "OP"]
super_parent_dict = {"Me": ["LM", 33, "HWB", 36, "ETPG", 35], "Them": ["EW", 41, "CC", 32],
                     "Us": ["Fam", 45, "Int", 44, "Soc", 32], "Fun": ["Rec", 30], "N/a": ["NV", 47, "OP", 48]}
domain_dict = {33:"LM", 36:"HWB", 35:"ETPG", 41: "EW", 32: "CC", 45: "Fam", 44: "Int", 46: "Soc", 30: "Rec", 47: "NV", 48: "OP"}

# Using the_key, either a color number or project name, return what the super_parent is
def assign_super_parent(the_key):
    for k, v in super_parent_dict.items():
        if the_key in v:
            return k
    return None

# Declare Project Variables
# pjDict = {"Me":{}, "Them":{}, "Us":{}, "Fun":{}}
pjDict = {}
flat_pjDict = {}
activeProjectList = []

# It's worth noting that as written, Project notes will not make their way into pjDict
for pj in api.state['projects']:
    if pj['is_deleted'] + pj['is_archived'] + pj['is_deleted'] == 0:
        pj['super_parent'] = assign_super_parent(pj['color'])
        pj['domain'] = domain_dict[pj['color']]
        pj['is_active_project'] = b'\xe2\x96\xb6' in pj['name'].encode('utf-8')
        pj['sub_project_ids'] = []
        pj['sub_projects'] = {}
        pj['tasks'] = []  # Empty for now
        pj['has_active_task'] = False  # False for now
        flat_pjDict[pj['id']] = pj

activeProjectList = [pj for pjID, pj in flat_pjDict.items() if pj['is_active_project']]


# Creates an incredible and redundant project dictionary... Wonder if this will have performance issues
# Also creates pjDict with real tree structure by deleting projects from root if they don't belong
pjDict = flat_pjDict.copy()  # Yes, a shallow copy. I have tested this and believe it sufficient for our purposes.
for pjID, pj in flat_pjDict.items():
    if pj['parent_id'] is None:
        continue
    else:
        pjDict.pop(pjID) # Pop it from the root of the tree dictionary
        flat_pjDict[pj['parent_id']]['sub_projects'][pjID] = pj
        flat_pjDict[pj['parent_id']]['sub_project_ids'].append(pjID)


# Count items in pjDict to confirm right size...
def count_depths(someDict):
    count = 0
    for pjID, pj in someDict.items():
        if pj['sub_projects'] == {}:
            count += 1
        else:
            count += 1 + count_depths(pj['sub_projects'])
    return count
assert count_depths(pjDict) == len(
    flat_pjDict), "Uh oh. The two project dictionaries are not the same size. Something's up."

# Label Data Set Up Area ================================
labelDict_byID = {}
labelDict_byName = {}
for label in api.state['labels']:
    labelDict_byName[label['name']] = label['id']
    labelDict_byID[label['id']] = label['name']

# Item/Task Data Set Up Area ================================
# Construct a list containing all items for consideration; those that have not been checked off/completed/deleted/etc
itemDict = {}
for item in api.state['items']:
    if (item['date_completed'] is None) and (item['in_history'] + item['checked'] + item['is_deleted'] == 0):
        item['is_thread'] = 'Thread' in item['content'] or b'\xe2\x9b\x93' in item['content'].encode('utf-8')
        item['is_active'] = item['priority'] > 1 # Todo: Check if this is right
        itemDict[item['id']] = item
        # Todo: Also find its parent project and shove it in there as well

activeThreadList = [item for itemID, item in itemDict.items() if item['is_active'] and item['is_thread']]