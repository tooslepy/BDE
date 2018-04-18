import itertools
import datetime
import sqlite3


def sql3(dbfile, tbl):
    conn = sqlite3.connect(dbfile)  # Opens db file
    global c
    c = conn.cursor()
    c.execute('SELECT {an} \
                 FROM {tn}'. \
              format(an="id", tn=tbl, ))
    result = [list(i) for i in c.fetchall()]
    result.sort()
    result = (result for result, _ in itertools.groupby(result))
    return result


def date_from_webkit(webkit_timestamp, base_no):
    if base_no == 9:
        webkit_timestamp = webkit_timestamp*10
        epoch_start = datetime.datetime(1601, 1, 1)
        delta = datetime.timedelta(microseconds=int(webkit_timestamp))
        return epoch_start + delta
    else:
        epoch_start = datetime.datetime(1601,1,1)
        delta = datetime.timedelta(microseconds=int(webkit_timestamp))
        return epoch_start + delta

def sqlWhen(col, table, idcol1, row1):
    c.execute('SELECT {an} \
                         FROM {tn} \
                        WHERE {cn} = {bn};'.
              format(an=col, tn=table, cn=idcol1, bn=row1))
    test = str(c.fetchall())
    test = test.strip('[()],\'')
    return ''.join([item for sublist in [list(row) for row in test] for item in sublist])


def sqlWhens(col, table, idcol1, row1, idcol2, row2, ispec):
    c.execute('SELECT {an} \
                         FROM {tn} \
                        WHERE {cn} = {bn} AND \
                              {dn} = {en};'.
              format(an=col, tn=table, cn=idcol1, bn=row1, dn=idcol2, en=row2))
    test = str(c.fetchall())
    test = test.strip('[()],\'')
    if ispec is True:
        return str(', '.join([item for sublist in [list(row) for row in test] for item in sublist]))
    else:
        return ''.join([item for sublist in [list(row) for row in str(test)] for item in sublist])


def sqlWhensb(col, table, idcol1, row1, idcol2, row2, ispec):
    c.execute('SELECT {an} \
                         FROM {tn} \
                        WHERE {cn} = {bn} AND \
                              {dn} => {en};'.
              format(an=col, tn=table, cn=idcol1, bn=row1, dn=idcol2, en=row2))
    test = str(c.fetchall())
    test = test.strip('[()],\'')
    if ispec is True:
        return str(', '.join([item for sublist in [list(row) for row in test] for item in sublist]))
    else:
        return ''.join([item for sublist in [list(row) for row in str(test)] for item in sublist])
