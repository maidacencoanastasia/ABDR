import struct
import datetime
import decimal
import itertools
import io
import csv
from operator import itemgetter

"""
First row -> field names.
Second row -> field specs: (type, size, decimal places).
Subsequent rows contain the data records.
If a record is marked as deleted, it is skipped.
"""


def dbfreader(f):
    # DBF format http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT

    numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))
    numfields = (lenheader - 33) // 32

    fields = []
    for fieldno in range(numfields):
        name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
        name = name.decode('ascii').replace('\0', '')  # eliminate NULs from string
        fields.append((name, typ.decode('ascii'), size, deci))

    yield [field[0] for field in fields]
    yield [tuple(field[1:]) for field in fields]

    terminator = f.read(1)
    assert terminator == b'\r'

    fields.insert(0, ('DeletionFlag', 'C', 1, 0))
    fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in fields])
    fmtsiz = struct.calcsize(fmt)

    for i in range(numrec):
        record = struct.unpack(fmt, f.read(fmtsiz))
        if record[0] != b' ':
            continue  # deleted record
        result = []
        for (name, typ, size, deci), value in zip(fields, record):
            if name == 'DeletionFlag':
                continue
            if typ == "N":
                value = value.decode('ascii').replace('\0', '').lstrip()
                if value == '':
                    value = 0
                elif deci:
                    value = decimal.Decimal(value)
                else:
                    value = int(value)
            elif typ == 'D':
                value = value.decode('ascii')
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif typ == 'L':
                value = (value.decode('ascii') in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
            elif typ == 'F':
                value = float(value.decode('ascii'))
            else:
                value = value.decode('ascii').strip()
            result.append(value)
        yield result


""" 
    Return a string suitable for writing directly to a binary dbf file.
    Fieldnames should be no longer than ten characters and not include \x00.
    Fieldspecs are in the form (type, size, deci) where
        type is one of:
            C for ascii character data
            M for ascii character memo data (real memo fields not supported)
            D for datetime objects
            N for ints or decimal objects
            L for logical values 'T', 'F'
"""


def dbfwriter(f, fieldnames, fieldspecs, records):
    # header info
    ver = 3
    now = datetime.datetime.now()
    yr, mon, day = now.year - 1900, now.month, now.day
    numrec = len(records)
    numfields = len(fieldspecs)
    lenheader = numfields * 32 + 33
    lenrecord = sum(field[1] for field in fieldspecs) + 1
    hdr = struct.pack('<BBBBLHH20x', ver, yr, mon, day, numrec, lenheader, lenrecord)
    f.write(hdr)

    # field specs
    for name, (typ, size, deci) in zip(fieldnames, fieldspecs):
        name = name.ljust(11, '\x00').encode('ascii')
        fld = struct.pack('<11sc4xBB14x', name, typ.encode('ascii'), size, deci)
        f.write(fld)

    # terminator
    f.write(b'\r')

    # records
    for record in records:
        f.write(b' ')  # deletion flag
        for (typ, size, deci), value in zip(fieldspecs, record):
            if typ == "N":
                value = str(value).rjust(size, ' ').encode('ascii')
            elif typ == 'D':
                value = value.strftime('%Y%m%d').encode('ascii')
            elif typ == 'L':
                value = str(value)[0].upper().encode('ascii')
            else:
                value = str(value)[:size].ljust(size, ' ').encode('ascii')
            assert len(value) == size
            f.write(value)

    # End of file
    f.write(b'\x1A')


# -------------------------------------------------------

if __name__ == '__main__':
    import sys

    # Read a database
    filename = "my_database.dbf"
    with open(filename, 'rb') as f:
        db = list(dbfreader(f))

    for record in db:
        print(record)

    fieldnames, fieldspecs, records = db[0], db[1], db[2:]
    # Alter the database: delete the third record and sort records by the fourth field
    del records[1]
    records.sort(key=itemgetter(3))

    # Remove a field from fieldnames and fieldspecs
    del fieldnames[0]
    del fieldspecs[0]
    records = [rec[1:] for rec in records]

    # # Create a new DBF
    # f = io.StringIO()
    # dbfwriter(f, fieldnames, fieldspecs, records)

    # # Read the data back from the new DBF
    # print('-' * 20)
    # f.seek(0)
    # for line in dbfreader(f):
    #     print(line)
    f.close()



