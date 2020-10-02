import datetime
import locale
import pandas as pd
import sqlite3
# from pprint import pprint

locale.setlocale(locale.LC_TIME, "nl_NL.UTF8")

today = datetime.date.today()
delta = (today.weekday() + 4) % 7
thursday = today - datetime.timedelta(days=delta)
print('<h3>Uitslag Herfstbridge ' + thursday.strftime('%A %d %B %Y') + ' op Step</h3>')
base = 'http://admin.stepbridge.nl/show.php?page=tournamentinfo&activityid='
activityid = '18449'  # Change this
link = '<a href="'+base+activityid+'" target="_blank">Deze uitslag op de website van Stepbridge</a>'
print('<p>&nbsp;</p>')
print('<p>'+link+'</p>')
url = base+activityid
step_raw = pd.read_html(url, index_col=0, attrs={'class': 'data'})
raw_date = step_raw[0]['Toernooi.1'][0][:9]
raw_date = str(raw_date).split('-')
d = ('0'+raw_date[0])[-2:]
m = ('0'+raw_date[1])[-2:]
y = raw_date[2].strip()
date = y+'-'+m+'-'+d
print(date)
step = pd.concat([step_raw[-2], step_raw[-1]])
step_as_list: list = list(step.values)
sql = """
INSERT INTO herfst (datum, naam, score)
    VALUES (?, ?, ?)
    ON CONFLICT(datum, naam) 
        DO UPDATE SET
        score = excluded.score;
"""

conn = sqlite3.connect('step.sqlite')
c = conn.cursor()
for line in step_as_list:
    names = line[0].split(' - ')
    score = line[1].replace(',', '.').replace('%', '')
    for name in names:
        c.execute(sql, (date, name, score))
conn.commit()
conn.close()
step.index = step.index.astype('int64')
print(step.to_html(border=0))
print('<br><br>')
