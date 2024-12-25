# __init__.py
from Saper.saper import Saper
from Saper.db import initialize_db


__author__ = 'chdg61'
__version__ = "0.1"



def show():
    initialize_db()
    Saper().show()