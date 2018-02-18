import sqlite3
import os
import itertools
import pandas as pd
import json

__name__ = "FDLE"
__author__ = "TooSlepy"
__PyVer__ = "3.6"

mzfp = os.getenv("appdata") + "\Mozilla\Firefox\Profiles\\"  # sets mzfp

for x in os.listdir(mzfp):  # finds default user
    if '.default' in x:
        ffID = x
dbFile = mzfp + ffID + "\places.sqlite"  # dir for firefox user profile

table1 = 'moz_annos'   # name of the table to be queried
table2 = 'moz_places'
id_column = 'id'
column_2 = 'place_id'
column_3 = 'anno_attribute_id'
column_4 = 'content'
column_8 = 'dateAdded'
data = []

# Connecting to the database file
conn = sqlite3.connect(dbFile)  # Opens db file
c = conn.cursor()

c.execute('SELECT {an} \
             FROM {tn} \
            WHERE NOT {cn}=4'.\
          format(an=column_2, tn=table1, cn=column_3))
result = [list(i) for i in c.fetchall()]
result.sort()
result = (result for result,_ in itertools.groupby(result))
for array in result:
    for row in array:
        row = str(row)
        c.execute('SELECT {an} \
                     FROM {tn} \
                    WHERE {cn} = {bn};'. \
                  format(an='url', tn=table2, cn=id_column, bn=row))
        url = ''.join([item for sublist in [list(row) for row in c.fetchall()] for item in sublist])

        c.execute('SELECT {an} \
                     FROM {tn} \
                    WHERE {cn} = {bn};'.
                  format(an='title', tn=table2, cn=id_column, bn=row))
        title = ''.join([item for sublist in [list(row) for row in c.fetchall()] for item in sublist])

        c.execute('SELECT {an} \
                     FROM {tn} \
                    WHERE {cn} = {bn} AND \
                          {dn} = {en};'.
                  format(an='dateAdded', tn=table1, cn='place_id', bn=row, dn='anno_attribute_id', en='6'))
        dateAdded = ''.join([item for sublist in [list(row) for row in str(c.fetchall())] for item in sublist])
        dateAdded = dateAdded.strip('[()],')
        dateAdded = pd.to_datetime((int(dateAdded)//1000000), unit='s')
        
        c.execute('SELECT {an} \
                     FROM {tn} \
                    WHERE {cn} = {bn} AND \
                          {dn} = {en};'.
                  format(an='content', tn=table1, cn='place_id', bn=row, dn='anno_attribute_id', en='6'))
        file = ''.join([item for sublist in [list(row) for row in c.fetchall()] for item in sublist])
        file = file.replace('%20', ' ')
        c.execute('SELECT {an} \
                             FROM {tn} \
                            WHERE {cn} = {bn} AND \
                                  {dn} = {en};'.
                  format(an='content', tn=table1, cn='place_id', bn=row, dn='anno_attribute_id', en='7'))

        extra = str(', '.join([item for sublist in [list(row) for row in c.fetchall()] for item in sublist]))
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
                  + ' UTC, ' + str(content[0]) + ', ' + str(content[1]) + str(content[2]))
            data.append({'Title': title, 'File': file, 'URL': url, 'Date Added (UTC)': str(dateAdded), 'Status': content[0],
                         'End Time (UNIX)': content[1], 'File Size (bytes)': (content[2])})

        elif len(content) <= 2:
            print(row + ', ' + title + ', ' + file + ', ' + url + ', ' + str(dateAdded)
                  + ' UTC, ' + str(content[0]) + ', ' + str(content[1]))
            data.append({'Title': title, 'File': file, 'URL': url, 'Date Added (UTXC)': str(dateAdded), 'Status': content[0],
                         'End Time(UNIX)': content[1]})

full = str(data)
full = full.replace("'", '"')
full = full.replace('file:///', '')
dl = open("downloads.json", "w")
dl.write(str(full))
print(full)
# Closing the connection to the database file
conn.close()
