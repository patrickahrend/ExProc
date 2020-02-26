# This ep.py will serve as the main conductor and manager of EP's functions.

#Imports
import datetime
import logging
import time
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="ep_logfile.txt", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('EP has started.')

# from ExProcTodoist import eptodo # As written, importing this package will run all of ep_todo. Double check that's what you want.
from ExProcTrello import eptrello
from ExProcTelegram import eptg
from ExProcGoogle import ep_gauth, epgcal

# Setup/Import of data, variables, paths
data_folder = Path("datastore/")

# Collecting some config variables

# Setting up other simple local variables
google_creds = ep_gauth.main()

# Start of the day scripts
# events = epgcal.review_yesterday(google_creds)
# eptrello.update_pj_status_board(eptodo.activeProjectList, eptodo.activeThreadList)
# eptrello.update_soc_status_board()

