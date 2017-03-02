# import tennis as ts 
import pandas as pd
import functions as f

year1 = 1984
year2 = 2016
df = f.getDataRange(year1, year2)


columns_win = ['w_ace', 'w_df', 'w_1stIn', 'w_1stWon','w_2ndWon','w_bpSaved', 'w_bpFaced']
columns_lose = ['l_ace', 'l_df', 'l_1stIn', 'l_1stWon','l_2ndWon','l_bpSaved', 'l_bpFaced']
columns_total = ['t_ace', 't_df', 't_1stIn', 't_1stWon','t_2ndWon','t_bpSaved', 't_bpFaced']
columns_serving = ['Name'] + columns_total + columns_win + columns_lose 

df_serving = pd.DataFrame(columns=columns_serving)

# players = df.winner_name.unique()
players = ['Roger Federer', 
'Rafael Nadal', 
'Ivo Karlovic', 
'Andy Roddick', 
'Pete Sampras', 
'Andre Agassi', 
'Novak Djokovic', 
'Andy Murray',
'Marat Safin',
'Stanislas Wawrinka',
'Lleyton Hewitt']

for player in players:
	name = pd.Series(data={'Name':player})
	player_win = df[(df.winner_name==player)][columns_win]
	player_lose = df[(df.loser_name==player)][columns_lose]

	player_total1 = pd.DataFrame(player_win.copy())
	player_total1.columns = columns_total
	player_total2 = pd.DataFrame(player_lose.copy())
	player_total2.columns = columns_total
	player_total = pd.concat([player_total1, player_total2])

	result = pd.concat([name,player_total.mean(), player_win.mean(), player_lose.mean()])
	df_serving = df_serving.append(result, ignore_index=True)

print df_serving


df_serving_data = df_serving[columns_total]
df_serving_labels = df_serving['Name']  

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(df_serving_data)
res = pca.transform(df_serving_data)

import matplotlib.pyplot as plt 
plt.scatter(res[:,0], res[:,1], label=df_serving_labels)
for i in range(len(df_serving_labels)):
	plt.text(res[i][0], res[i][1], df_serving_labels[i])
plt.show()

