# This ep.py will serve as the main conductor and manager of EP's functions.
import logging
import time

from pathlib import Path


logging.basicConfig(level=logging.DEBUG, filename="ep_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('EP has started.')

# from ExProcTodoist import eptodo # As written, importing this package will run all of ep_todo. Double check that's what you want.
from ExProcTrello import eptrello
from ExProcTelegram import eptg


data_folder = Path("datastore/")


# eptrello.update_pj_status_board(eptodo.activeProjectList, eptodo.activeThreadList)
# eptrello.update_soc_status_board()

# My idea for allowing this to loop for now is to re-fresh the Telegram bot regularly so I don't run into downtime.
while True:
    logging.info("Started another loop of EP.py")
    from ExProcTelegram import eptg
    time.sleep(900)  # 15 Minutes. Just for now.

