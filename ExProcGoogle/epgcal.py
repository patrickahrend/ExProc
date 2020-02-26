import dateutil.tz
import json

from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from pathlib import Path

from googleapiclient.discovery import build

# Setup/Import of data, variables, paths
EP_Path = Path(__file__).parents[1]
datastore_folder = Path(EP_Path, "datastore")
trello_folder = Path(EP_Path, "ExProcTrello/")

# Collecting some config variables
with open(datastore_folder / "ep_config.json", encoding="utf8") as datastore_auth:
    auth_json = json.load(datastore_auth)
    smt_calendar_id = auth_json['gcal_links']['smt_calendar_id']


def review_yesterday(creds):
    # Call the Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Must be an RFC3339 timestamp with mandatory time zone offset, for example, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z.
    midnight_tdayutc = (datetime.now(dateutil.tz.gettz('America/Chicago'))
                      .replace(hour=0, minute=0, second=0, microsecond=0)
                      .astimezone(dateutil.tz.tzutc()))
    midnight_ydayutc = midnight_tdayutc - timedelta(days=1)
    tday_iso = midnight_tdayutc.isoformat()
    yday_iso = midnight_ydayutc.isoformat()

    # More help here: https://developers.google.com/calendar/v3/reference/events/list
    events_result = service.events().list(calendarId=smt_calendar_id, timeMin=yday_iso, timeMax=tday_iso,
                                          singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])

    # Quickly parse all the start/end times to simplify coding
    for event in events:
        event['start']['dt'] = parse(event['start']['dateTime'])
        event['end']['dt'] = parse(event['end']['dateTime'])

    # Go over the first and last events to see if they cross the midnight hours
    if crosses_midnight(events[0]):
        events[0]['start']['dt'] = events[0]['start']['dt'].replace(day=events[0]['start']['dt'].day+1, hour=0, minute=0, second=0, microsecond=0)
    if crosses_midnight(events[-1]):
        events[-1]['end']['dt'] = events[-1]['end']['dt'].replace(hour=0, minute=0, second=0, microsecond=0)

    times = {}
    for e in events:
        lot = (e['end']['dt'] - e['start']['dt']).total_seconds()
        try:
            times[e['summary']] += lot
        except KeyError:
            times[e['summary']] = lot

    props = {}  # Proportions of day
    for k, v in times.items():
        props[k] = v / 864

    # Print it out
    print("Yesterday's time allocations:")
    for k, v in times.items():
        print(f'{k}: {(v/60):.2f}, {props[k]:.2f}%')

    return events

def crosses_midnight(event):
    if event['start']['dt'].day == event['end']['dt']:
        return False
    else:
        return True
