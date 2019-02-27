#!/usr/bin/env python

from __future__ import print_function
import argparse

import pandas as pd
from sklearn import linear_model, pipeline, metrics
    
def make_df_from_file(in_path):
    '''
    Input is the file specified by `in_path`, a .csv file containing the original, unconverted RAPM data. If the file does not
    exist or is not readable, an exception will be thrown and there will be no output.
    
    Otherwise, output is the dataframe of the data read from `path`, except that columns corresponding to the offensive and
    defensive lineups (ConcatLineup and ConcatLineup_Opp) are renamed as such.
    '''
    
    try:
        df = pd.read_csv(in_path)
        df = df.rename(columns={'ConcatLineup': 'OffLineup', 'ConcatLineup_Opp': 'DefLineup'})
        return df
    except:
        print('File not found, please retype your input file.')
        return

def get_by_lineup_eff(df):
    '''
    Input is the dataframe `df` returned successfully from `make_df_from_file`.
    
    Output is the dataframe which aggregates -- over each `OffLineup`, `DefLineup` pair (along with the `isHomeTeam` indicator
    for the `OffLineup`) -- the total efficiency (per 100 possessions)
    '''    
    # get the no. of points, total no. of possessions and home/away team on offense indicator for each pair of off/def lineups
    agg_d = {'PTS': 'sum', 'OverallPossNum': 'count', 'isHomeTeam': 'mean'}
    by_lineups = df.groupby(['OffLineup', 'DefLineup']).agg(agg_d).astype(int).reset_index()
    
    # convert the pts for each off. lineup vs def. lineup pair to efficiency (Eff)
    by_lineups['Eff'] = by_lineups.apply(lambda row: 100 * (row['PTS'] / row['OverallPossNum']), axis=1)
    
    # keep only efficiency with each off/def lineup pair, re-format these lineups and add new column for all players on court
    by_lineups.drop(columns=['PTS', 'OverallPossNum'], inplace=True)
    by_lineups['OffLineup'] = by_lineups['OffLineup'].apply(lambda x: ' '.join(x.split('.')[1:-1]))
    by_lineups['DefLineup'] = by_lineups['DefLineup'].apply(lambda x: ' '.join(x.split('.')[1:-1]))
    by_lineups['OnCourt'] = by_lineups['OffLineup'] + ' ' + by_lineups['DefLineup']
    return by_lineups

def make_data_matrix(by_lineups):
    '''
    Input is the dataframe `by_lineups` returned successfully from `get_by_lineup_eff`.
    
    Output is the dataframe whose columns are all possible player IDs in the data for both offense and defense (so two per
    player), and a column each indicating whether the home team is on offense and for the efficiency margin. Each row corresponds
    to the margin for a given pair of offensive and defensive lineups, with players on offense assigned a 1 for the column
    corresponding to their offensive presence and players on defense assigned -1 for the column corresponding to their defensive
    presence and zeros assigned otherwise.
    '''
    # define index columns
    cols = ['OnCourt', 'Eff', 'isHomeTeam']
    
    # the final dataframe should accommodate the following model:
    # Eff = ORAPM_1 * x_1 + ... + ORAPM_n * x_n + DRAPM_1 *y_1 + ... + D_RAPM_n * y_n + HOME_OFF * isHomeTeam + error, where:
    # x_k = 1 if player k is on offense and 0 otherwise
    # y_k = -1 if player k is on defense and 0 otherwise
    # ORAPM_k (DRAPM_k) is the estimated offensive (defensive) RAPM of player defensive
    # HOME_OFF is an estimate of the effect of being the home team on offense
    # isHomeTeam and Eff are as defined previously
    
    # make "subdataframe" of all offensive players
    off_lineups = pd.get_dummies(
        by_lineups.set_index(cols).OffLineup \
        .str.split(' ', expand=True).stack()
        ).groupby(level=cols).sum().astype(int).reset_index()
    
    # make "subdataframe" of all defensive players
    def_lineups = pd.get_dummies(
        by_lineups.set_index(cols).DefLineup \
        .str.split(' ', expand=True).stack()
        ).groupby(level=cols).sum().multiply(-1).astype(int).reset_index()
    
    # combine into a single dataframe
    oncourt_df = off_lineups.merge(def_lineups, on=['OnCourt', 'Eff', 'isHomeTeam']).drop('OnCourt', axis=1)
    return oncourt_df

def estimate_rapm(df, penalty):    
    '''
    Inputs are the dataframe `df` returned from `make_data_matrix` and `penalty` corresponding to the alpha value for the Ridge
    Regression model to be fit to the data in `data_matrix`
    
    Output is dataframe where each row provides an individual player ID and then the Ridge Regressions coefficients estimating
    the player's offensive and defensive RAPM. 
    '''
    
    # Specify feature matrix X and target column y
    X = df.drop('Eff', axis=1)
    y = df['Eff']
    
    # Find number of offensive players; this is needed to split returned coefficient estimates into offense and defense
    player_cols = list(X.columns[1:])
    n_off_players = len([x for x in player_cols if x.find('_x') != -1])
    
    # Fit the "assumed to be validated" Ridge Regression model on the data to get ORAPM and DRAPM estimates
    lr_ridge = linear_model.Ridge(alpha=penalty)
    ridge_fit = lr_ridge.fit(X,y)
    
    # Match all player ids to ORAPM and DRAPM estimates separately and combine
    off_rapm = pd.DataFrame(list(zip(X.columns, ridge_fit.coef_))[1:(n_off_players+1)], columns=['PlayerID', 'EstOffRAPM'])
    def_rapm = pd.DataFrame(list(zip(X.columns, ridge_fit.coef_))[(n_off_players+1):], columns=['PlayerID', 'EstDefRAPM'])
    off_rapm['PlayerID'] = off_rapm['PlayerID'].apply(lambda x: x.split('_')[0])
    def_rapm['PlayerID'] = def_rapm['PlayerID'].apply(lambda x: x.split('_')[0])
    
    return off_rapm.merge(def_rapm, on='PlayerID', how='outer')

def write_estimated_rapm(in_path, out_path, penalty):
    '''
    Input is the file specified by `in_path`, the .csv file containing the original RAPM data, the file specified by `out_path`, 
    the .csv file where the estimated RAPMs are to be written, and (optionally) `penalty`, corresponding to the value to be
    passed to the function `estimate_rapm`.
    
    Essentially takes the data as read from `in_path` through to writing out the RAPM estimates to `out_path`:
    1) Reads data from `in_path` to a dataframe
    2) Converts to dataframe of by lineup (offense-defense pair) efficiency margins
    3) Makes the data matrix representing the offensive and defensive lineups corresponding to the above efficiency margins
    4) Uses the data matrix to fit a Ridge Regression whose coefficients are the estimated offensive and defensive RAPM for each
    player
    5) Writes all these estimates to a .csv file
    '''
  
    df = make_df_from_file(in_path)
    by_lineups = get_by_lineup_eff(df)
    on_court_eff = make_data_matrix(by_lineups)
    rapm_est = estimate_rapm(on_court_eff, penalty)
    rapm_est.to_csv(out_path, index=False)

if __name__ == "__main__":
    
    # Set up parsing of command line arguments    
    parser = argparse.ArgumentParser()
    
    # Make paths for the input and output files required arguments and flags to use to specify them
    required = parser.add_argument_group('Required Arguments')
    required.add_argument('-i', '--inputfile', help='Input Filepath', required=True)
    required.add_argument('-o', '--outputfile', help='Output Filepath', required=True)
    
    # Add the Ridge Regression penalty as an optional argument and the flag to specify it
    # Make sure only one argument is provided and it can be coerced into a float. Also provide a default value for this penalty
    parser.add_argument('-p', '--penalty', help='Ridge Regression Penalty', action='store', nargs=1, type=float, default=2000.0)
    
    # Parsing and error checking
    # 1) Check that the input filepath is specified and as a .csv file
    # 2) Check that the output filepath is specified and as a .csv file
    # 3) Then read in, analyze and write data if the input file exists and is readable
    args = parser.parse_args()    
    if args.inputfile is not None and not args.inputfile.endswith('.csv'):
        parser.error('Please specify an input file in .csv format.')
    elif args.outputfile is not None and not args.outputfile.endswith('.csv'):
        parser.error('Please specify an output file in .csv format.')
    else:
        try:
            write_estimated_rapm(args.inputfile, args.outputfile, args.penalty)
        except:
            pass