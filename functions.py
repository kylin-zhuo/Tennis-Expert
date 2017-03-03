import pandas as pd 
import numpy as np
import re

"""
Transform the dataframe following the following principles: 
a) 1st in&won and 2nd won: num -> ratio
b) ace and double faults: num -> ratio
c) break points saving: num -> ratio
d) break points faced: num -> ratio
"""

def transform(df):
	# Transform the 1st serve won and 2nd serve won from number to ratio
	df.w_1stWon = df.w_1stWon / df.w_1stIn
	df.l_1stWon = df.l_1stWon / df.l_1stIn
	df.w_2ndWon = df.w_2ndWon / (df.w_svpt - df.w_1stIn)
	df.l_2ndWon = df.l_2ndWon / (df.l_svpt - df.l_1stIn)

	# Transform the 1st serve in from number to ratio
	df.w_1stIn = df.w_1stIn / df.w_svpt
	df.l_1stIn = df.l_1stIn / df.l_svpt

	# Transform the break point saving ratio
	if df.w_bpFaced.tolist()[0] != 0:
		df.w_bpSaved = df.w_bpSaved / df.w_bpFaced
	if df.l_bpFaced.tolist()[0] != 0:
		df.l_bpSaved = df.l_bpSaved / df.l_bpFaced

	# Transform the aces and double faults to ratio
	df.w_ace = df.w_ace / df.w_svpt
	df.l_ace = df.l_ace / df.l_svpt
	df.w_df = df.w_df / df.w_svpt
	df.l_df = df.l_df / df.l_svpt

	# Transform the breakpoint faced ration
	df.w_bpFaced = df.w_bpFaced / df.w_svpt
	df.l_bpFaced = df.l_bpFaced / df.l_svpt


"""
Handle the NA entries:
a) drop the entries when there are more than 
"""
def dealwithna(df, t=43, v=0):
	# winner_data = winner_data.fillna(winner_data.mean)
	# loser_data = loser_data.fillna(loser_data.mean)
	df.dropna(thresh = t, axis=0, inplace=True)
	df.fillna(value=v, inplace=True)

# def deleteTour(df, tournament):
	# df = df[not df['tourney_name'][0].startswith(tournament)]

def preprocessing(df):
	# df.rename(columns={'l_bpFaced\t':'l_bpFaced'}, inplace=True)
	# df.l_bpFaced = pd.to_numeric(df.l_bpFaced, errors='coerce')
	df.tourney_date = pd.to_datetime(df.tourney_date,format='%Y%m%d')

	transform(df)
	dealwithna(df)

# concatenate the dataframes
def getDataRange(year_begin, year_end):
	dfs = []
	for i in range(year_begin,year_end):
		df = pd.read_csv('tennis_atp-master/atp_matches_{}.csv'.format(i))
		preprocessing(df)
		dfs.append(df)
	return pd.concat(dfs)


