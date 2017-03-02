import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

import re

"""
'tourney_id', 'tourney_name', 'surface', 'tourney_date','match_num', 'winner_id', 'winner_seed', 'winner_name',
'winner_hand', 'winner_ioc', 'winner_age', 'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 
'loser_name', 'loser_hand', 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points', 'score', 'best_of', 
'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 
'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'
"""


df = pd.read_csv('2016.csv')

df.rename(columns={'l_bpFaced\t':'l_bpFaced'}, inplace=True)
df.l_bpFaced = pd.to_numeric(df.l_bpFaced, errors='coerce')

# print len(df.tourney_name.unique())

# tornaments is numpy.ndarray -> list


