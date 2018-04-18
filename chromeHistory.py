import os
import pandas as pd
from functions import *

# Vars:
__name__ = "CHE"
__author__ = "TooSlepy"
__PyVer__ = "3.6"

data = []
fp = os.getenv("appdata")+"\..\Local\Google\Chrome\\User data\Default\\"  # Sets file path
dbFile = fp+"\History"  # Database file

for array in sql3(dbFile, 'downloads'):
    for row in array:
        row = str(row)
        title = sqlWhen('title', 'urls', 'id', row)
        url = sqlWhen('url', 'urls', 'id', row)
        visitCount = sqlWhen('visit_count', 'urls', 'id', row)

        lastVisitTime = sqlWhen('last_visit_time', 'urls', 'id', row)
        if lastVisitTime == "1610612736" or lastVisitTime == "-1610612736":
            lastVisitTime = 'Honestly I have no idea this data entry has an underflow or overflow'
        else:
            lastVisitTime = str(date_from_webkit(lastVisitTime, 10))

        typedCount = str(sqlWhen('typed_count', 'urls', 'id', row))

        isHidden = sqlWhen('hidden', 'urls', 'id', row)
        if isHidden == '0':
            isHidden = False
        else:
            isHidden = True

        data.append(
            {'Title': title, 'Url': url, 'Amount of times visited': visitCount, 'Time last visited': lastVisitTime,
             'Amount of times typed': typedCount, 'Amount of time spent on site': visitDuration})
        print({'Title': title, 'Url': url, 'Amount of times visited': visitCount, 'Time last visited': lastVisitTime,
               'Amount of times typed': typedCount, 'Amount of time spent on site': visitDuration})

full = str(data)
full = full.replace("'", '"')
full = full.replace("😋","'")
dl = open("chromeHistory" + ".json", "w")
dl.write(str(full))
print(full)
# Closing the connection to the database file
sql3(dbFile,'downloads').close()