# As I figure out how to structure this file, I believe that I will use main.py as a conductor of sorts.
from pathlib import Path

from ExProcTodoist import eptodo
from ExProcTrello import eptrello


data_folder = Path("datastore/")


eptrello.update_pj_status_board(eptodo.activeProjectList, eptodo.activeThreadList)
