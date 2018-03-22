import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from collections import Counter

data_path = '../tennis_atp-master/'
MIN_YEAR = 1968
MAX_YEAR = 2018

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

    data = {
    'player': player,
    'year': year,
    'n_winning': n_winning,
    'n_losing': n_losing,
    'ace_rate_winning': ace_rate_winning,
    'ace_rate_losing': ace_rate_losing,
    'ace_rate_overall': ace_rate_overall
    }

    keys = ['player', 'year', 'n_winning', 'n_losing',
    'ace_rate_winning', 'ace_rate_losing', 'ace_rate_overall']

    return keys, data

# Extract the rivary data of two players
def rivary(p1, p2, from_year, to_year):

    print p1, p2, from_year, to_year

    if not from_year or len(from_year) == 0:
        from_year = MIN_YEAR
    if not to_year or len(to_year) == 0:
        to_year = MAX_YEAR

    from_year = int(from_year)
    to_year = int(to_year)

    assert(from_year <= to_year)

    wins, loses = 0, 0
    matches = []

    for year in range(from_year, to_year+1):
        df = pd.read_csv(data_path + "atp_matches_%s.csv" % year)
        df = df[((df['winner_name'] == p1) & (df['loser_name'] == p2)) | ((df['loser_name'] == p1) & (df['winner_name'] == p2))]

        for i in range(len(df)):
            matches.append(dict(df.iloc[i]))

        head_2_heads = Counter(zip(df["winner_name"], df["loser_name"]))
        wins += head_2_heads[(p1, p2)]
        loses += head_2_heads[(p2, p1)]

    matches.sort(key=lambda x:x['tourney_date'], reverse=True)

    res = {
    'p1': p1,
    'p2': p2,
    'h2h': [wins, loses],
    'matches': matches
    }
    return res
