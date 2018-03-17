import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from collections import Counter

data_path = '../tennis_atp-master/'


def player_info(player, year, with_davis_cup = True):

    df = pd.read_csv(data_path + "atp_matches_%s.csv" % year)
    if not with_davis_cup:
        df = df[df.tourney_name.str.contains("Davis") == False]

    assert(len(df['tourney_id'].unique()) == len(df['tourney_name'].unique()))

    winning_slice = df[df["winner_name"] == player]
    losing_slice = df[df["loser_name"] == player]

    n_winning, n_losing = len(winning_slice), len(losing_slice)

    ace_rate_winning = np.sum(winning_slice.w_ace) / np.sum(winning_slice['w_svpt'])
    ace_rate_losing = np.sum(losing_slice.l_ace) / np.sum(losing_slice['l_svpt'])
    ace_rate_overall = (np.sum(winning_slice.w_ace) + np.sum(losing_slice.l_ace)) / \
     (np.sum(winning_slice['w_svpt']) + np.sum(losing_slice['l_svpt']))

    res = {
    'player': player,
    'year': year,
    'n_winning': n_winning,
    'n_losing': n_losing,
    'ace_rate_winning': ace_rate_winning,
    'ace_rate_losing': ace_rate_losing,
    'ace_rate_overall': ace_rate_overall
    }

    return res
