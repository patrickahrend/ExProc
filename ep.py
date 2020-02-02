# This ep.py will serve as the main conductor and manager of EP's functions.
from pathlib import Path

# from ExProcTodoist import eptodo # As written, importing this package will run all of ep_todo. Double check that's what you want.
from ExProcTrello import eptrello
from ExProcTelegram import eptg


data_folder = Path("datastore/")


# eptrello.update_pj_status_board(eptodo.activeProjectList, eptodo.activeThreadList)
# eptrello.update_soc_status_board()

eptg.main()
