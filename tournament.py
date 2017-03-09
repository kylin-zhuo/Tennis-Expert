import pandas as pd
import functions as f
import numpy as np
import pylab as pb
import matplotlib.pyplot as plt

start_year = 2001
end_year = 2016

# plt.close('all')
# exit()

df = f.getDataRange(start_year, end_year)

def sortTournaments(ts, s, e):
	df = f.getDataRange(s, e)
	res = []
	for t in ts:
		tmp = map(lambda s: int(s.strftime('%j'))/365.0, df[df.tourney_name==t].tourney_date)
		res.append((t, sum(tmp)/len(tmp)))
	return [i[0] for i in sorted(res, key=lambda tup:tup[1])]

df_gm = df[(df.tourney_level=='G') | (df.tourney_level=='M')]
degraded = ['Stuttgart Masters','Hamburg Masters']
tournaments = [t for t in df_gm.tourney_name.unique() if t not in degraded]

tournaments = sortTournaments(tournaments, 2012, 2016)
print tournaments


item = 'ace'
title = 'ace ('+str(start_year)+'-'+str(end_year)+')'
item1, item2 = 'w_'+item, 'l_'+item
res = []
for tour in tournaments:
	df_s = df_gm[df_gm.tourney_name==tour]
	res.append((tour, (df_s[item1].mean() + df_s[item2].mean())/2))
Y = [i[1] for i in res]
# print Y

X = range(len(tournaments))
fig = plt.figure()
ax = fig.add_subplot(111)
plt.bar(X, Y, align='center')
plt.xticks(X, tournaments, rotation=45, horizontalalignment='right')
ax.set_title(title)
plt.show()