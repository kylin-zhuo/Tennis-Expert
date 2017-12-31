import pandas as pd
import functions as f
import numpy as np
import pylab as pb
import matplotlib.pyplot as plt

start_year = 1991
end_year = 2016

df = f.getDataRange(start_year, end_year)


print len(df)
# print df.head()

print df['surface'].unique()
tourney_ids = df['tourney_id'].unique()

df2 = df[['tourney_id', 'tourney_name','surface', 'tourney_level']]
df2 = df2.drop_duplicates()
df2 = df2[~df2['tourney_name'].astype(str).str.startswith('Davis')]
df2['year'] = df2['tourney_id'].astype(str).str[:4].astype(int)

res = df2.groupby('year').surface.count()

exit()


#discover how many aces each type of surfaces
surfaces = df.surface.unique()

res = []

item = '2ndWon'
title = '2nd Serve Won'
item1, item2 = 'w_'+item, 'l_'+item
for surf in surfaces:
	df_s = df[df.surface==surf]
	res.append((surf, (df_s[item1].mean() + df_s[item2].mean())/2))
Y = [i[1] for i in res]
print Y
X = range(len(surfaces))
fig = plt.figure()
ax = fig.add_subplot(111)
plt.bar(X, Y, align='center',color=['blue','green','orange','purple'])
plt.xticks(X, surfaces)
ax.set_title(title)
plt.show()

def tournament_num():
	surfaces = df.surface.unique()
	dic = dict(zip(surfaces, [0]*len(surfaces)))
	for t in df.tourney_id.unique():
		s = df[df.tourney_id==t].iloc[0]['surface']
		dic[s] += 1

	X = dic.keys()
	Y = dic.values()
	pb.figure(1, figsize=(6,6))
	# ax = axes([0.1, 0.1, 0.8])
	# explode=(0.01, 0.01, 0.01)

	pb.pie(Y, labels=X, autopct='%1.01f%%', shadow=False, startangle=90)
	pb.title('Tournament Surfaces ('+str(start_year)+'-'+str(end_year)+')', bbox={'facecolor':'0.8', 'pad':5})
	pb.show()

