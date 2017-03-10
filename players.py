import pandas as pd
import functions as f
import numpy as np
import pylab as pb
import matplotlib.pyplot as plt
from tennis import *

start_year = 2001
end_year = 2016

df = f.getDataRange(start_year, end_year)

exit()

def aceRatio(*args):
	# w,l: the pieces of dataframe that he won or lost
	# 3 args: p1, p2, df -> the ace ratio p1 served to p2 
	# 2 args: p, df -> the ace ratio p has served in tournaments
	if len(args)==3:
		p1, p2, df = args
		w, l = df[(df.winner_name==p1)&(df.loser_name==p2)],df[(df.winner_name==p2)&(df.loser_name==p1)]
		return (w.w_ace.sum() + l.l_ace.sum())/ (len(w)+len(l))
	elif len(args)==2:
		p, df = args
		w,l = df[df.winner_name==p], df[df.loser_name==p]
		return (w.w_ace.sum() + l.l_ace.sum())/(len(w)+len(l))

# print aceRatio('Roger Federer', 'Novak Djokovic', df)
# print aceRatio('Roger Federer', df)
# print aceRatio('Roger Federer', 'Andy Murray', df)
# print aceRatio('Rafael Nadal', df)
# print aceRatio('Rafael Nadal', 'Roger Federer', df)
# print aceRatio('Novak Djokovic', df)

import itertools
l = len(players)
res = np.zeros((l,l))
it = np.nditer(res, flags=['multi_index'], op_flags=['readwrite'])

for comb in itertools.product(players,repeat=2):
	ix = it.multi_index
	p1, p2 = comb
	if p1 == p2: res[ix] = aceRatio(p1, df)
	else: res[ix] = aceRatio(p1, p2, df)
	it.iternext()

print res

plt.pcolor(res,cmap=plt.cm.Blues, label=res)
plt.xticks(range(l), players, rotation=45, horizontalalignment='right')
plt.yticks(range(l), players, rotation=45, horizontalalignment='right')
plt.show()



