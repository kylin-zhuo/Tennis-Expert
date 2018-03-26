import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from collections import Counter, defaultdict

data_path = "../tennis_atp-master/"
MIN_YEAR = 1968
MAX_YEAR = 2018

def is_winning_1st_set(score):
    score = score.strip()
    if score[:3] == 'W/O' or score[:3] == 'RET':
        return False
    sets = score.split()
    set1 = sets[0][:3]
    print set1
    a, b = set1.split('-')
    return a > b

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
    titles = {}

    all_wins, all_loses = 0, 0
    all_wins_G, all_loses_G = 0, 0
    all_wins_M, all_loses_M = 0, 0
    all_wins_F, all_loses_F = 0, 0
    all_titles, all_finalists = 0, 0
    tiebreak_wins, tiebreak_loses = 0, 0
    vs_top10_wins, vs_top10_loses = 0, 0
    deciding_set_wins, deciding_set_loses = 0, 0
    fifth_set_wins, fifth_set_loses = 0, 0
    grass_wins, grass_loses = 0, 0
    hard_wins, hard_loses = 0, 0
    clay_wins, clay_loses = 0, 0
    carpet_wins, carpet_loses = 0, 0
    titles_hard, titles_grass, titles_clay, titles_carpet = 0, 0, 0, 0
    titles_G, titles_M, titles_F = 0, 0, 0
    won_1st_set_wins, won_1st_set_loses = 0, 0
    lost_1st_set_wins, lost_1st_set_loses = 0, 0
    vs_right_hand_wins, vs_right_hand_loses = 0, 0
    vs_left_hand_wins, vs_left_hand_loses = 0, 0

    titles['titles'] = []
    titles['finalist'] = []

    for year in range(from_year, to_year+1):
        df = pd.read_csv(data_path + "atp_matches_%s.csv" % str(year))
        if not with_davis_cup:
            df = df[df.tourney_name.str.contains("Davis") == False]

        # assert(len(df['tourney_id'].unique()) == len(df['tourney_name'].unique()))
        # all_titles += len(df[((df['round'] == 'F') & (df['winner_name'] == player))])

        winning_slice = df[df["winner_name"] == player]
        losing_slice = df[df["loser_name"] == player]

        titles_hard += len(winning_slice[((winning_slice['surface'] == 'Hard') & (winning_slice['round'] == 'F'))])
        titles_grass += len(winning_slice[((winning_slice['surface'] == 'Grass') & (winning_slice['round'] == 'F'))])
        titles_clay += len(winning_slice[((winning_slice['surface'] == 'Clay') & (winning_slice['round'] == 'F'))])
        titles_carpet += len(winning_slice[((winning_slice['surface'] == 'Carpet') & (winning_slice['round'] == 'F'))])

        titles_G += len(winning_slice[((winning_slice['tourney_level'] == 'G') & (winning_slice['round'] == 'F'))])
        titles_M += len(winning_slice[((winning_slice['tourney_level'] == 'M') & (winning_slice['round'] == 'F'))])
        titles_F += len(winning_slice[((winning_slice['tourney_level'] == 'F') & (winning_slice['round'] == 'F'))])

        vs_right_hand_wins += len(winning_slice[winning_slice['loser_hand'] == 'R'])
        vs_right_hand_loses += len(losing_slice[losing_slice['winner_hand'] == 'R'])
        vs_left_hand_wins += len(winning_slice[winning_slice['loser_hand'] == 'L'])
        vs_left_hand_loses += len(losing_slice[losing_slice['winner_hand'] == 'L'])

        won_1st_set_wins += sum(map(lambda s: is_winning_1st_set(s), winning_slice.score))
        lost_1st_set_wins += sum(map(lambda s: not is_winning_1st_set(s), winning_slice.score))
        won_1st_set_loses += sum(map(lambda s: not is_winning_1st_set(s), losing_slice.score))
        lost_1st_set_loses += sum(map(lambda s: is_winning_1st_set(s), losing_slice.score))

        grass_wins += len(winning_slice[winning_slice['surface'] == 'Grass'])
        grass_loses += len(losing_slice[losing_slice['surface'] == 'Grass'])
        hard_wins += len(winning_slice[winning_slice['surface'] == 'Hard'])
        hard_loses += len(losing_slice[losing_slice['surface'] == 'Hard'])
        clay_wins += len(winning_slice[winning_slice['surface'] == 'Clay'])
        clay_loses += len(losing_slice[losing_slice['surface'] == 'Clay'])
        carpet_wins += len(winning_slice[winning_slice['surface'] == 'Carpet'])
        carpet_loses += len(losing_slice[losing_slice['surface'] == 'Carpet'])

        deciding_set_wins += sum(map(lambda s: len(s.split()) == 3, winning_slice[winning_slice['best_of'] == 3].score))
        temp = sum(map(lambda s: len(s.split()) == 5, winning_slice[winning_slice['best_of'] == 5].score))
        deciding_set_wins += temp
        fifth_set_wins += temp
        deciding_set_loses += sum(map(lambda s: len(s.split()) == 3, losing_slice[losing_slice['best_of'] == 3].score))
        temp = sum(map(lambda s: len(s.split()) == 5, losing_slice[losing_slice['best_of'] == 5].score))
        deciding_set_loses += temp
        fifth_set_loses += temp

        vs_top10_wins += len(winning_slice[winning_slice['loser_rank'] <= 10])
        vs_top10_loses += len(losing_slice[losing_slice['winner_rank'] <= 10])

        tiebreak_wins += sum(map(lambda s: sum(map(lambda x:'7-6' in x, s.split())), winning_slice.score))
        tiebreak_wins += sum(map(lambda s: sum(map(lambda x:'6-7' in x, s.split())), losing_slice.score))
        tiebreak_loses += sum(map(lambda s: sum(map(lambda x:'6-7' in x, s.split())), winning_slice.score))
        tiebreak_loses += sum(map(lambda s: sum(map(lambda x:'7-6' in x, s.split())), losing_slice.score))

        # titles
        ts = winning_slice[winning_slice['round'] == 'F']
        # finalist
        fl = losing_slice[losing_slice['round'] == 'F']

        all_titles += len(ts)
        all_finalists += len(fl)

        if len(ts):
            titles['titles'].append((year, len(ts), list(ts['tourney_name']), list(ts['loser_name'])))
        if len(fl):
            titles['finalist'].append((year, len(fl), list(fl['tourney_name']), list(fl['winner_name'])))

        all_wins_G += len(winning_slice[winning_slice['tourney_level'] == 'G'])
        all_wins_M += len(winning_slice[winning_slice['tourney_level'] == 'M'])
        all_wins_F += len(winning_slice[winning_slice['tourney_level'] == 'F'])

        all_loses_G += len(losing_slice[losing_slice['tourney_level'] == 'G'])
        all_loses_M += len(losing_slice[losing_slice['tourney_level'] == 'M'])
        all_loses_F += len(losing_slice[losing_slice['tourney_level'] == 'F'])

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
    ## OVERVIEW
    overview['all_wins'] = all_wins
    overview['all_loses'] = all_loses
    overview['all_titles'] = all_titles
    ## WINLOSS
    winloss['all_wins'] = all_wins
    winloss['all_loses']= all_loses
    winloss['all_wins_G'] = all_wins_G
    winloss['all_loses_G'] = all_loses_G
    winloss['all_wins_M'] = all_wins_M
    winloss['all_loses_M'] = all_loses_M
    winloss['all_wins_F'] = all_wins_F
    winloss['all_loses_F'] = all_loses_F
    winloss['titles_G'] = titles_G
    winloss['titles_M'] = titles_M
    winloss['titles_F'] = titles_F
    # Pressure points
    winloss['tiebreak_wins'] = tiebreak_wins
    winloss['tiebreak_loses'] = tiebreak_loses
    winloss['vs_top10_wins'] = vs_top10_wins
    winloss['vs_top10_loses'] = vs_top10_loses
    winloss['finals_wins'] = all_titles
    winloss['finals_loses'] = all_finalists
    winloss['deciding_set_wins'] = deciding_set_wins
    winloss['deciding_set_loses'] = deciding_set_loses
    winloss['fifth_set_wins'] = fifth_set_wins
    winloss['fifth_set_loses'] = fifth_set_loses
    # Environment
    winloss['grass_wins'] = grass_wins
    winloss['grass_loses'] = grass_loses
    winloss['hard_wins'] = hard_wins
    winloss['hard_loses'] = hard_loses
    winloss['clay_wins'] = clay_wins
    winloss['clay_loses'] = clay_loses
    winloss['carpet_wins'] = carpet_wins
    winloss['carpet_loses'] = carpet_loses
    winloss['titles_hard'] = titles_hard
    winloss['titles_grass'] = titles_grass
    winloss['titles_clay'] = titles_clay
    winloss['titles_carpet'] = titles_carpet
    # Others
    winloss['won_1st_set_wins'] = won_1st_set_wins
    winloss['won_1st_set_loses'] = won_1st_set_loses
    winloss['lost_1st_set_wins'] = lost_1st_set_wins
    winloss['lost_1st_set_loses'] = lost_1st_set_loses
    winloss['vs_right_hand_wins'] = vs_right_hand_wins
    winloss['vs_right_hand_loses'] = vs_right_hand_loses
    winloss['vs_left_hand_wins'] = vs_left_hand_wins
    winloss['vs_left_hand_loses'] = vs_left_hand_loses

    ## TITLES
    titles['titles'].sort(reverse=True)
    titles['finalist'].sort(reverse=True)

    return keys, res, overview, winloss, titles


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
