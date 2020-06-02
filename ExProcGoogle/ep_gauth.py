# This script gets credentials for use by other Google API apps.
# Copied entirely from https://developers.google.com/people/quickstart/python
# Had to install some of Google's Packages
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Note: I am adding all of the Google Connections to this one gauth file.
# If you add another api, make sure to add it to the below SCOPES as well as make it a new _main() method

# Imports
from __future__ import print_function
import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path


# Setup/Import of data, variables, paths
EP_Path = Path(__file__).parents[1]
datastore_folder = Path(EP_Path, "datastore")

# If modifying these scopes, delete the file token.pickle.
# These scopes indicate which authentications will be made and stored in the pickle
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly', 'https://www.googleapis.com/auth/calendar.readonly']

# Handles the production, storage, and return of the credentials for other calling scripts
# Almost all of this directly copied from Google's Python API Quickstart Documentation
def main():
    """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.

    if os.path.exists(datastore_folder / 'googletoken.pickle'):
        with open(datastore_folder / 'googletoken.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(datastore_folder / 'googlecredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(datastore_folder / 'googletoken.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds