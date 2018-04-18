import sqlite3
import os
import itertools
import pandas as pd
import json
import math

# Vars:
__name__ = "FDLE"
__author__ = "TooSlepy"
__PyVer__ = "3.6"
table1 = 'moz_annos'  # name of the table to be queried
column_2 = 'place_id'
column_3 = 'anno_attribute_id'
data = []
fp = os.getenv("appdata") + "\Mozilla\Firefox\Profiles\\"  # sets mzfp
for x in os.listdir(fp):  # finds default user
    if '.default' in x:
        ffID = x
dbFile = fp + ffID + "\places.sqlite"  # dir for firefox user profile

# Connecting to the database file
conn = sqlite3.connect(dbFile)  # Opens db file
c = conn.cursor()
c.execute('SELECT {an} \
             FROM {tn} \
            WHERE NOT {cn}=4'. \
          format(an=column_2, tn=table1, cn=column_3))
result = [list(i) for i in c.fetchall()]
result.sort()
result = (result for result, _ in itertools.groupby(result))


def sqlWhen(col, table, idcol1, row1):
    c.execute('SELECT {an} \
                         FROM {tn} \
                        WHERE {cn} = {bn};'. \
              format(an=col, tn=table, cn=idcol1, bn=row1))
    return ''.join([item for sublist in [list(row) for row in c.fetchall()] for item in sublist])


def sqlWhens(col, table, idcol1, row1, idcol2, row2, ispec):
    c.execute('SELECT {an} \
                         FROM {tn} \
                        WHERE {cn} = {bn} AND \
                              {dn} = {en};'.
              format(an=col, tn=table, cn=idcol1, bn=row1, dn=idcol2, en=row2))
    if ispec is True:
        return str(', '.join([item for sublist in [list(row) for row in c.fetchall()] for item in sublist]))
    else:
        return ''.join([item for sublist in [list(row) for row in str(c.fetchall())] for item in sublist])

for array in result:
    for row in array:
        row = str(row)
        url = sqlWhen('url', 'moz_places', 'id', row)
        title = sqlWhen('title', 'moz_places', 'id', row)
        dateAdded = sqlWhens('dateAdded', 'moz_annos', 'place_id', row, 'anno_attribute_id', '6', False)
        dateAdded = dateAdded.strip('[()],')
        dateAdded = pd.to_datetime((int(dateAdded) // 1000000), unit='s')
        file = sqlWhens('content', 'moz_annos', 'place_id', row, 'anno_attribute_id', '6', False)
        file = file.replace('%20', ' ')
        file = file.replace('file:///', '')
        extra = sqlWhens('content', 'moz_annos', 'place_id', row, 'anno_attribute_id', '7', True)
        extra = extra.replace(",", ", ")
        try:
            extra = json.loads(extra)
            content = [v for _, v in extra.items()]
        except:
            print('\nThere is no extra content row for ' + title + ' @ ' + file +
                  ' please wait for it to download or cancel the download\n')
            content = [0, 0, 0]

        # Arrays are set out as: ID (The SQLite mos_places id), FileName, URL, DateAdded,
        # State(0=Paused/Missing Row, 1=True, 2=Unknown, 3= Incomplete), EndTime, FileSize

        row = str(row)
        if len(content) > 2:
            print(row + ', ' + title + ', ' + file + ', ' + url + ', ' + str(dateAdded)
                 + ' UTC, ' + str(content[0]) + ', ' + str(content[1]) + ', ' + str(content[2]))
            data.append(
                {'Title': title, 'File': file, 'URL': url, 'Date Added (UTC)': str(dateAdded), 'Status': content[0],
                'End Time (UNIX)': content[1], 'File Size (bytes)': (content[2])})

        elif len(content) <= 2:
            print(row + ', ' + title + ', ' + file + ', ' + url + ', ' + str(dateAdded)
                  + ' UTC, ' + str(content[0]) + ', ' + str(content[1]))
            data.append({'Title': title, 'File': file, 'URL': url, 'Date Added (UTXC)': str(dateAdded),
                         'Status': content[0],
                         'End Time(UNIX)': content[1]})

full = str(data)
full = full.replace("'", '"')
dl = open("exported\FirefoxDownloadH" + ".json", "w")
dl.write(str(full))
print(full)
# Closing the connection to the database file
conn.close()
