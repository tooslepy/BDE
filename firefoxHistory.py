import sqlite3
import os
import itertools
import pandas as pd
import json

# Vars:
__name__ = "FHE"
__author__ = "TooSlepy"
__PyVer__ = "3.6"

data = []
fp = os.getenv("appdata") + "\Mozilla\Firefox\Profiles\\"  # Sets file path
dbFile = fp + ffID + "\places.sqlite"  # Database file

# Connecting to the database file
conn = sqlite3.connect(dbFile)  # Opens db file
c = conn.cursor()



full = str(data)
full = full.replace("'", '"')
full = full.replace("😋","'")
dl = open("exported\FirefoxHistory" + ".json", "w")
dl.write(str(full))
print(full)
# Closing the connection to the database file
sql3(dbFile,'downloads').close()