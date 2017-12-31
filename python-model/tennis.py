
"""
'tourney_id', 'tourney_name', 'surface', 'tourney_date','match_num', 'winner_id', 'winner_seed', 'winner_name',
'winner_hand', 'winner_ioc', 'winner_age', 'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 
'loser_name', 'loser_hand', 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points', 'score', 'best_of', 
'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 
'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'
"""

cols_match = ['tourney_id', 'tourney_name', 'surface', 'tourney_date','match_num', 'score', 'best_of', 'round', 'minutes']

cols_profile_winner = ['winner_id', 'winner_seed', 'winner_name', 'winner_hand', 'winner_ioc', 'winner_age', 'winner_rank','winner_rank_points']
cols_data_winner = ['w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced']
cols_profile_loser = ['loser_id', 'loser_seed', 'loser_name', 'loser_hand', 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points'] 
cols_data_loser = ['l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']

cols_data = map(lambda x: x.replace("l_",""), cols_data_loser)
cols_profile = map(lambda x: x.replace("loser_",""), cols_profile_loser)

