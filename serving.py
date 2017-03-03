# import tennis as ts 
import pandas as pd
import functions as f

year1 = 2001
year2 = 2016
df = f.getDataRange(year1, year2)


columns_win = ['w_ace', 'w_df', 'w_1stIn', 'w_1stWon','w_2ndWon','w_bpSaved', 'w_bpFaced']
columns_lose = ['l_ace', 'l_df', 'l_1stIn', 'l_1stWon','l_2ndWon','l_bpSaved', 'l_bpFaced']
columns_total = ['ace', 'df', '1stIn', '1stWon','2ndWon','bpSaved', 'bpFaced']
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
'Lleyton Hewitt']


# res = pd.to_datetime('20150524',format='%Y%m%d') - pd.to_datetime('20150521',format='%Y%m%d')
# print res.days

# fed = df[df.winner_name == 'Roger Federer']
# fed.plot(x='tourney_date', y='w_ace', style='o')
import matplotlib.pyplot as plt

plt.scatter(df['w_1stWon'], df['w_ace'])
plt.show()
exit()

def model_pca(df):

	global df_serving
	global players

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

	# print df_serving


	def doPCA(df, labels=None, n=2):
		# Dimensional reduction for visualization
		from sklearn.decomposition import PCA
		pca = PCA(n_components=n)
		pca.fit(df)
		return pca.transform(df)


	columns1 = ['ace', 'df', '1stWon', 'bpFaced']

	df_serving_data = df_serving[columns1]

	"""
	print df_serving_data
	df_serving_data_norm = (df_serving_data - df_serving_data.mean()) / (df_serving_data.max() - df_serving_data.min())
	print df_serving_data_norm

	from sklearn import preprocessing

	min_max_scaler = preprocessing.MinMaxScaler()
	np_scaled = min_max_scaler.fit_transform(df_serving_data)
	df_serving_data_norm2 = pd.DataFrame(np_scaled)
	print df_serving_data_norm2

	df_serving_data = df_serving[columns1]

	"""
	# res = doPCA(df_serving_data_norm)
	res = doPCA(df_serving_data)
	df_serving_labels = df_serving['Name']

	import matplotlib.pyplot as plt 
	plt.scatter(res[:,0], res[:,1], label=df_serving_labels)
	for i in range(len(df_serving_labels)):
		plt.text(res[i][0], res[i][1], df_serving_labels[i])
	plt.show()

# if __name__ == '__main__':
# 	# model_pca(df)




