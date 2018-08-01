import csv
from competition.models import Students
from datetime import date
import re

csv_path = '/home/sabesan/tmv_src/asogt/db_data/data/hello.csv'
data_row_start = 3 # 3rd row
cols_required = 7

def get_date(date_text):
    #example string = '2002-03-09 00:00:00.000'
    parts = date_text.replace("\'", "").split('-')
    year = int(re.sub("[^0-9]", "", parts[0]))
    month = int(re.sub("[^0-9]", "", parts[1]))
    day = int(re.sub("[^0-9]", "", parts[2].split(" ")[0]))
    
    return date(year, month, day)

with open(csv_path) as f:
    reader = csv.reader(x.replace('\0', '') for x in f)
    for row_count, row in enumerate(reader):
        if row_count < (data_row_start -1) or len(row)< cols_required:
            continue
        _, created = Students.objects.get_or_create(
            userid = row[0].strip(),
            firstname = row[1].strip(),
            lastname = row[2].strip(),
            firstname_tamil = unicode(row[3].strip(), 'utf-8'),
            lastname_tamil = unicode(row[4].strip(), 'utf-8'),
            dob = get_date(row[5]),
            gender = row[6].strip()
            )
        import pdb; pdb.set_trace()
        print("Created : {:b}", created)