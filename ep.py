# This ep.py will serve as the main conductor and manager of EP's functions.

#Imports
import logging
import threading
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="ep_logfile.txt", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('EP has started.')

from ExProcGoogle import ep_gauth, epgcal
from ExProcTrello import eptrello
from ExProcTelegram import eptg  # Interestingly, I believe this starts eptg all by itself, and I think continues past it as well

# from ExProcTodoist import eptodo # As written, importing this package will run all of ep_todo. Double check that's what you want.


# Setup/Import of data, variables, paths
data_folder = Path("datastore/")

print("hey we made it")
# Collecting some config variables

# Setting up other simple local variables
google_creds = ep_gauth.main()

# Start of the day scripts
# events = epgcal.review_yesterday(google_creds)
# eptrello.update_pj_status_board(eptodo.activeProjectList, eptodo.activeThreadList)
# eptrello.update_soc_status_board()



