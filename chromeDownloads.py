import os
from functions import *

# Vars:
__name__ = "CDLE"
__author__ = "TooSlepy"
__PyVer__ = "3.6"

data = ["Any 0😋s mean that there is no data for that field this generally means that the download was not completed "]
fp = os.getenv("appdata") + "\..\Local\Google\Chrome\\User data\Default\\"  # Sets file path
dbFile = fp + "\History"  # Database file

# Connecting to the database file

for array in sql3(dbFile, 'downloads'):
    for row in array:
        row = str(row)
        url = sqlWhens('url', 'downloads_url_chains', 'id', row, 'chain_index', '0', False)

        title = sqlWhen('target_path', 'downloads', 'id', row)
        title = title.split("\\")
        title = ''.join(title[-1:])
        title.strip("'[]")

        dateAdded = sqlWhen('start_time', 'downloads', 'id', row)
        dateAdded = str(date_from_webkit(dateAdded, 10))

        dateCompleted = sqlWhen('end_time', 'downloads', 'id', row)
        if dateCompleted == '0':
            dateCompleted = '0'
        else:
            dateCompleted = str(date_from_webkit(dateCompleted, 10))

        fPath = sqlWhen('current_path', 'downloads', 'id', row)
        if fPath == '':
            fPath = 'No Path'
        else:
            fPath = fPath
            fPath = fPath.replace('\\\\', '\\')

        fPathTarget = sqlWhen('target_path', 'downloads', 'id', row)
        fPathTarget = fPathTarget.replace('\\\\', '\\')

        totalBytes = sqlWhen('total_bytes', 'downloads', 'id', row)
        receivedBytes = sqlWhen('received_bytes', 'downloads', 'id', row)

        opened = sqlWhen('opened', 'downloads', 'id', row)
        if opened == 0:
            opened = False
        else:
            opened = True
        opened = str(opened)

        whenOpened = sqlWhen('last_access_time', 'downloads', 'id', row)
        if whenOpened == '0':
            whenOpened = '0'
        elif whenOpened > '0':
            whenOpened = str(date_from_webkit(whenOpened))

        lastModified = sqlWhen('last_modified', 'downloads', 'id', row)
        currentFType = sqlWhen('mime_type', 'downloads', 'id', row)
        FType = sqlWhen('original_mime_type', 'downloads', 'id', row)
        fileExists = str(os.path.isfile(fPath))
        print(title + ', ' + url + ', ' + fPath + ', ' + fPathTarget + ', ' + fileExists + ', ' + dateAdded + ', ' + dateCompleted + ', ' +
              totalBytes + ', ' + receivedBytes + ', ' + opened + ', ' + whenOpened + ', ' + lastModified  + ', ' +
              currentFType + ', ' + FType)
        data.append(
            {'Title': title, 'File Path': fPath, 'File Path Target': fPathTarget,'File Exists': fileExists, 'URL': url,
             'Date Added (UTC)': str(dateAdded), 'Date Completed (UTC)': dateCompleted, 'File Size': totalBytes,
             'Bytes Received': receivedBytes, 'Opened':opened, 'Time Opened': whenOpened, 'Last Modified': lastModified,
             'Current File Type': currentFType, 'Original File Type': FType})

full = str(data)
full = full.replace("'", '"')
full = full.replace("😋","'")
dl = open("exported\ChromeDownloadsHistory" + ".json", "w")
dl.write(str(full))
print(full)
# Closing the connection to the database file
sql3(dbFile,'downloads').close()

