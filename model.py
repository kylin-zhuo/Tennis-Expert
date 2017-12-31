from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd
import functions as f
import numpy as np


def model1(df):
	winners = pd.DataFrame(df[['w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 
		'w_2ndWon','w_SvGms', 'w_bpSaved', 'w_bpFaced']])
	losers = pd.DataFrame(df[['l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 
		'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']])

	winners.columns = range(9)
	losers.columns = range(9)

	winners = winners.dropna(axis=0, how='any')
	losers = losers.dropna(axis=0, how='any')
	n_winners = len(winners)
	n_losers = len(losers)

	w = [1]*n_winners
	l = [0]*n_losers
	w.extend(l)
	y = w

	data_train, data_test, label_train, label_test = train_test_split(X, y, test_size = 0.33, random_state = 7)

	frames = [winners, losers]
	X = pd.concat(frames)

	model = SVC(C=1, gamma=0.01)
	model.fit(data_train, label_train)

	print model.score(data_test, label_test)


def model2(df):
	tournaments = df.tourney_name.unique().tolist()

	features0 = ['minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 
	'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']

	features = ['w_ace', 'w_df', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_bpSaved', 'w_bpFaced']

	# X = pd.DataFrame([], columns = features)
	X = []
	y = []
	shuffle = 1

	# loop through each tournament to extract info
	for tour in tournaments:

		if tour.startswith('Davis Cup'):
			continue
		df_tour = df[df.tourney_name == tour]
		transform(df_tour)

		s = df_tour[df_tour['round'] == 'F']

		winner = s['winner_name'].tolist()[0]
		loser = s['loser_name'].tolist()[0]

		# extractFeature(df_tour, X, y)

		# Remember to remove the data of the final
		df_tour = df_tour[df_tour['round'] != 'F']
		winner_data = df_tour[df_tour['winner_name'] == winner][features]
		loser_data = df_tour[df_tour['winner_name'] == loser][features]

		winner_data = dealwithna(winner_data, 5, 0)
		loser_data = dealwithna(loser_data, 5, 0)

		winner_data_mean = winner_data.mean(axis=0).tolist()
		loser_data_mean = loser_data.mean(axis=0).tolist()

		"""
		if shuffle == 1:
			X.append(np.subtract(winner_data_mean, loser_data_mean).tolist())
			y.append(1)
			shuffle *= -1
		else:
			X.append(np.subtract(loser_data_mean, winner_data_mean).tolist())
			y.append(0)
			shuffle *= -1
		"""
	X = pd.DataFrame(X, columns=features)
	data_train, data_test, label_train, label_test = train_test_split(X, y, test_size = 0.33, random_state = 7)

	model = SVC(C=1, gamma=0.1)
	model.fit(data_train, label_train)
	print model.score(data_test, label_test)