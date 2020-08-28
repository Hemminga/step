import sqlite3
from pprint import pprint

conn = sqlite3.connect('step.sqlite')
sql = """
    SELECT * FROM herfst WHERE datum > '2020-08-26' ORDER BY datum DESC;
"""
c = conn.cursor()
c.execute(sql)
rows = c.fetchall()
sql = """
    SELECT DISTINCT datum FROM herfst ORDER BY datum DESC;
"""
c.execute(sql)
data_rows = c.fetchall()
conn.close()

# List met alle data op volgorde (aflopend)
data = [data_rows[x][0] for x in range(len(data_rows))]
len_data = len(data)
# Lege list voor scores van gelijke lengte
scores = [None for _ in range(len(data_rows))]
# Lijst met unique deelnemers
deelnemers = list(set([rows[x][2] for x in range(len(rows))]))

uitslagen = []
for deelnemer in deelnemers:
    uitslagen.append({'naam': deelnemer, 'scores': scores[:]})

for row in rows:
    for line in uitslagen:
        if line['naam'] == row[2]:
            i = data.index(row[1])
            j = uitslagen.index(line)
            uitslagen[j]['scores'][i] = row[3]

for row in uitslagen:
    count = len(row['scores']) - row['scores'].count(None)
    average = sum(row['scores']) / count
    uitslagen[uitslagen.index(row)]['average'] = average
    uitslagen[uitslagen.index(row)]['count'] = count
    best = row['scores'][:]
    best.sort(reverse=True)
    count = len(row['scores'])
    if count > 4:
        count = 4
    uitslagen[uitslagen.index(row)]['best'] = sum(best[:count])
    if len(data) > 4:
        count = len(row['scores'][4:]) - row['scores'][4:].count(None)
        average = sum(row['scores'][4:]) / count
        uitslagen[uitslagen.index(row)]['old_average'] = average
        uitslagen[uitslagen.index(row)]['old_count'] = count

rank = 0
prev_avg = 0
uitslagen = sorted(uitslagen, key=lambda x: x['best'], reverse=True)
table = "<table>\n\t<thead>\n\t\t<tr>\n\t\t\t"
table += "<td>#</td><td>naam</td><td>gem</td><td>#</td>"
for d in data[:4]:
    table += f"<td>{d[5:]}</td>"
table += "\n\t\t</tr>\n\t</thead><tbody>"
for u in uitslagen:
    rank += 1
    avg = f"{u['average']:.2f}"
    avg = avg.replace('.', ',')
    if prev_avg == u['average']:
        prank = ''
    else:
        prank = rank
    table += f"\n\t\t<tr>\n\t\t\t<td>{prank}</td><td>{u['naam']}</td><td>{avg}</td><td>{u['count']}</td>"
    for s in u['scores'][:4]:
        val = f"{s:.2f}"
        val = val.replace('.', ',')
        table += f"<td>{val}</td>"
    table += "\n\t\t</tr>"
    prev_avg = u['average']
table += "\n\t</tbody>\n</table>"
print(table)
