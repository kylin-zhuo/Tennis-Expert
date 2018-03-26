import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from collections import Counter, defaultdict

data_path = "../tennis_atp-master/"
MIN_YEAR = 1968
MAX_YEAR = 2018


def player_info(player, year, with_davis_cup = True):

    if year:
        from_year = int(year)
        to_year = int(year)
    else:
        from_year = MIN_YEAR
        to_year = MAX_YEAR

    res = {}
    overview = {}
    winloss = {}

    all_wins, all_loses = 0, 0
    all_wins_G, all_loses_G = 0, 0
    all_wins_M, all_loses_M = 0, 0
    all_titles = 0
    tiebreak_wins, tiebreak_loses = 0, 0
    vs_top10_wins, vs_top10_loses = 0, 0

    for year in range(from_year, to_year+1):

        df = pd.read_csv(data_path + "atp_matches_%s.csv" % str(year))
        if not with_davis_cup:
            df = df[df.tourney_name.str.contains("Davis") == False]

        # assert(len(df['tourney_id'].unique()) == len(df['tourney_name'].unique()))
        # all_titles += len(df[((df['round'] == 'F') & (df['winner_name'] == player))])

        winning_slice = df[df["winner_name"] == player]
        losing_slice = df[df["loser_name"] == player]

        tiebreak_wins += sum(map(lambda s: sum(map(lambda x:'7-6' in x, s.split())), winning_slice.score))
        tiebreak_wins += sum(map(lambda s: sum(map(lambda x:'6-7' in x, s.split())), losing_slice.score))
        tiebreak_loses += sum(map(lambda s: sum(map(lambda x:'6-7' in x, s.split())), winning_slice.score))
        tiebreak_loses += sum(map(lambda s: sum(map(lambda x:'7-6' in x, s.split())), losing_slice.score))

        all_titles += len(winning_slice[winning_slice['round'] == 'F'])
        all_wins_G += len(winning_slice[winning_slice['tourney_level'] == 'G'])
        all_wins_M += len(winning_slice[winning_slice['tourney_level'] == 'M'])

        all_loses_G += len(losing_slice[losing_slice['tourney_level'] == 'G'])
        all_loses_M += len(losing_slice[losing_slice['tourney_level'] == 'M'])

        n_winning, n_losing = len(winning_slice), len(losing_slice)
        all_wins += n_winning
        all_loses += n_losing

        if n_winning or n_losing:

            # ace_rate_winning = np.sum(winning_slice.w_ace) / np.sum(winning_slice['w_svpt'])
            # ace_rate_losing = np.sum(losing_slice.l_ace) / np.sum(losing_slice['l_svpt'])
            # ace_rate_overall = (np.sum(winning_slice.w_ace) + np.sum(losing_slice.l_ace)) / \
            #  (np.sum(winning_slice['w_svpt']) + np.sum(losing_slice['l_svpt']))

            data = {
            'player': player,
            'year': year,
            'n_winning': n_winning,
            'n_losing': n_losing,
            # 'ace_rate_winning': ace_rate_winning,
            # 'ace_rate_losing': ace_rate_losing,
            # 'ace_rate_overall': ace_rate_overall
            }

            res[year] = data

    keys = ['player', 'year', 'n_winning', 'n_losing',
    'ace_rate_winning', 'ace_rate_losing', 'ace_rate_overall']
    overview['all_wins'] = all_wins
    overview['all_loses'] = all_loses
    overview['all_titles'] = all_titles
    winloss['all_wins'] = all_wins
    winloss['all_loses']= all_loses
    winloss['all_wins_G'] = all_loses_G
    winloss['all_loses_G'] = all_loses_G
    winloss['all_wins_M'] = all_wins_M
    winloss['all_loses_M'] = all_loses_M
    winloss['tiebreak_wins'] = tiebreak_wins
    winloss['tiebreak_loses'] = tiebreak_loses

    return keys, res, overview, winloss


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
    wins_grass, loses_grass = 0, 0
    wins_hard, loses_hard = 0, 0
    wins_clay, loses_clay = 0, 0
    matches = []

    for year in range(from_year, to_year+1):
        df = pd.read_csv(data_path + "atp_matches_%s.csv" % year)
        df = df[((df['winner_name'] == p1) & (df['loser_name'] == p2)) | ((df['loser_name'] == p1) & (df['winner_name'] == p2))]

        df_grass = df[df['surface'] == 'Grass']
        df_hard = df[df['surface'] == 'Hard']
        df_clay = df[df['surface'] == 'Clay']

        for i in range(len(df)):
            matches.append(dict(df.iloc[i]))

        head_2_heads = Counter(zip(df["winner_name"], df["loser_name"]))
        head_2_heads_grass = Counter(zip(df_grass["winner_name"], df_grass["loser_name"]))
        head_2_heads_hard = Counter(zip(df_hard["winner_name"], df_hard["loser_name"]))
        head_2_heads_clay = Counter(zip(df_clay["winner_name"], df_clay["loser_name"]))

        wins += head_2_heads[(p1, p2)]
        loses += head_2_heads[(p2, p1)]
        wins_grass += head_2_heads_grass[(p1, p2)]
        loses_grass += head_2_heads_grass[(p2, p1)]
        wins_hard += head_2_heads_hard[(p1, p2)]
        loses_hard += head_2_heads_hard[(p2, p1)]
        wins_clay += head_2_heads_clay[(p1, p2)]
        loses_clay += head_2_heads_clay[(p2, p1)]        

    matches.sort(key=lambda x:x['tourney_date'], reverse=True)

    res = {
    'p1': p1,
    'p2': p2,
    'h2h': [wins, loses],
    'h2h_grass': [wins_grass, loses_grass],
    'h2h_hard': [wins_hard, loses_hard],
    'h2h_clay': [wins_clay, loses_clay],
    'matches': matches
    }
    return res
