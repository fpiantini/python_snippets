#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

# -------------------------------------------------------------
def one_dict(list_dict):
    """
    converts a list of dictionaries on a dictionary of lists.
    Example:
       [
         {'a_key': 'a_value_1', 'b_key': 'b_value_1'},
         {'a_key': 'a_value_2', 'b_key': 'b_value_2'}
       ]
    becomes:
       {
         'a_key': ['a_value_1', 'a_value_2'],
         'b_key': ['b_value_1', 'b_value_2'],
       }
    This is useful to process data with Pandas. The output of this
    function ca be used to build a Panda DataSet using the DataFrame
    constructor
    """

    # This extract the keys
    keys = list_dict[0].keys()
    # keys = ['a_key', 'b_key']

    # initialize dictionary
    out_dict = {key: [] for key in keys}
    # out_dict = {'a_key': [], 'b_key': []}

    for dict_ in list_dict:
        # for every element (dictionary) in input list, e.g.:
        #   {'a_key': 'a_value_1', 'b_key': 'b_value_1'}
        for key, value in dict_.items():
            # extract the key,value pairs, e.g.:
            #   'a_key', 'a_value_1'
            # and insert the value in the correct list of the
            # output dictionary, e.g.:
            #   out_dict['a_key'].append('a_value_1')
            out_dict[key].append(value)
            # after first iteration, for example out_dict will be:
            #   out_dict = {'a_key': ['a_value_1'], 'b_key': []}
        # after first complete execution of the internal loop:
        #   out_dict = {'a_key': ['a_value_1'], 'b_key': ['b_value_1']}

    # after completation of all iterations:
    #   out_dict = {
    #     'a_key': ['a_value_1', 'a_value_2'],
    #     'b_key': ['b_value_1', 'b_value_2'],
    #   }
    return out_dict

# -------------------------------------------------------------
# ********************************************************************************
# MAIN
# ********************************************************************************
def main():

    #dict_ = { 'a': [11, 21, 31], 'b': [12, 22, 32]}
    #df = pd.DataFrame(dict_)
    #print(type(df))
    #print(df)
    #print(df.mean())

    # gets the teams using nba-api.
    nba_teams = teams.get_teams()
    #print(type(nba_teams))
    #print(nba_teams)
    #print(nba_teams[0].keys())

    # get_teams() returns a list, we convert it to a dictionary
    dict_nba_teams = one_dict(nba_teams)
    #print(type(dict_nba_teams))
    #print(dict_nba_teams)

    # converts the dictionary to a Pandas data frame
    df_teams = pd.DataFrame(dict_nba_teams)
    #print(df_teams.head(10))
    #            id              full_name abbreviation   nickname          city          state  year_founded
    # 0  1610612737          Atlanta Hawks          ATL      Hawks       Atlanta        Atlanta          1949
    # 1  1610612738         Boston Celtics          BOS    Celtics        Boston  Massachusetts          1946
    # 2  1610612739    Cleveland Cavaliers          CLE  Cavaliers     Cleveland           Ohio          1970
    # 3  1610612740   New Orleans Pelicans          NOP   Pelicans   New Orleans      Louisiana          2002
    # 4  1610612741          Chicago Bulls          CHI      Bulls       Chicago       Illinois          1966
    # 5  1610612742       Dallas Mavericks          DAL  Mavericks        Dallas          Texas          1980
    # 6  1610612743         Denver Nuggets          DEN    Nuggets        Denver       Colorado          1976
    # 7  1610612744  Golden State Warriors          GSW   Warriors  Golden State     California          1946
    # 8  1610612745        Houston Rockets          HOU    Rockets       Houston          Texas          1967
    # 9  1610612746   Los Angeles Clippers          LAC   Clippers   Los Angeles     California          1970

    # ----------------- gets a team (Warriors) information --------------------------------------------------
    # 1. search the dataframe entry with nickname = "Warriors"
    df_warriors = df_teams[df_teams['nickname'] == 'Warriors']
    #print(df_warriors)
    #            id              full_name abbreviation  nickname          city       state  year_founded
    # 7  1610612744  Golden State Warriors          GSW  Warriors  Golden State  California          1946

    # 2. get the record ID of the Warriors
    id_warriors = df_warriors['id']
    #print(id_warriors)
    # 7    1610612744
    # Name: id, dtype: int64
    #print(type(id_warriors))
    # <class 'pandas.core.series.Series'>

    # 3. find the games of the Warriors
    gfinder = leaguegamefinder.LeagueGameFinder(team_id_nullable = id_warriors)
    #print(gfinder)
    full_df = gfinder.get_data_frames()
    #print(full_df)
    games = full_df[0]
    #print(games.head())
    #   SEASON_ID     TEAM_ID TEAM_ABBREVIATION              TEAM_NAME     GAME_ID   GAME_DATE      MATCHUP WL  MIN  PTS  FGM  FGA  FG_PCT  FG3M  FG3A  FG3_PCT  FTM  FTA  FT_PCT  OREB  DREB   REB  AST  STL  BLK  TOV  PF  PLUS_MINUS
    # 0     22019  1610612744               GSW  Golden State Warriors  0021900967  2020-03-10  GSW vs. LAC  L  239  107   37   79   0.468    11  38.0    0.289   22   27   0.815   4.0  31.0  35.0   25    3    0    9  17       -24.0
    # 1     22019  1610612744               GSW  Golden State Warriors  0021900944  2020-03-07  GSW vs. PHI  W  240  118   44   80   0.550     9  25.0    0.360   21   28   0.750   7.0  28.0  35.0   30    4    2    7  19         4.0
    # 2     22019  1610612744               GSW  Golden State Warriors  0021900929  2020-03-05  GSW vs. TOR  L  240  113   40   98   0.408    14  52.0    0.269   19   25   0.760  14.0  38.0  52.0   34    4    5   15  23        -8.0
    # 3     22019  1610612744               GSW  Golden State Warriors  0021900913  2020-03-03    GSW @ DEN  W  239  116   42   82   0.512    18  41.0    0.439   14   22   0.636   5.0  30.0  35.0   31    8    3   11  23        16.0
    # 4     22019  1610612744               GSW  Golden State Warriors  0021900901  2020-03-01  GSW vs. WAS  L  239  110   42   89   0.472     9  28.0    0.321   17   24   0.708  18.0  34.0  52.0   25    7    7   21  24       -14.0

    team_abbr = games.loc[0]['TEAM_ABBREVIATION']
    #print(team_abbr)
    # GSW
    opposite_team_abbr = 'TOR'

    games_home = games[games['MATCHUP'] == f"{team_abbr} vs. {opposite_team_abbr}"]
    games_away = games[games['MATCHUP'] == f"{team_abbr} @ {opposite_team_abbr}"]
    #print(games_home)
    #      SEASON_ID     TEAM_ID TEAM_ABBREVIATION              TEAM_NAME     GAME_ID   GAME_DATE      MATCHUP WL  MIN  PTS  FGM  FGA  FG_PCT  FG3M  FG3A  FG3_PCT  FTM  FTA  FT_PCT  OREB  DREB   REB  AST  STL  BLK  TOV  PF  PLUS_MINUS
    # 2        22019  1610612744               GSW  Golden State Warriors  0021900929  2020-03-05  GSW vs. TOR  L  240  113   40   98   0.408    14  52.0    0.269   19   25   0.760  14.0  38.0  52.0   34    4    5   15  23        -8.0
    # 73       22019  1610612744               GSW  Golden State Warriors  1521900020  2019-07-07  GSW vs. TOR  W  201   80   28   70   0.400    12  27.0    0.444   12   13   0.923   6.0  37.0  43.0   18    8    3   20  25        10.0
    # 78       42018  1610612744               GSW  Golden State Warriors  0041800406  2019-06-13  GSW vs. TOR  L  240  110   39   80   0.488    11  31.0    0.355   21   30   0.700  11.0  31.0  42.0   28    9    6   16  23        -4.0
    # ....
    #print("--------------------------------------------------------")
    #print(games_away)
    #      SEASON_ID     TEAM_ID TEAM_ABBREVIATION              TEAM_NAME     GAME_ID   GAME_DATE    MATCHUP WL  MIN  PTS  FGM  FGA  FG_PCT  FG3M  FG3A  FG3_PCT  FTM  FTA  FT_PCT  OREB  DREB   REB  AST  STL  BLK  TOV  PF  PLUS_MINUS
    # 79       42018  1610612744               GSW  Golden State Warriors  0041800405  2019-06-10  GSW @ TOR  W  240  106   38   82   0.463    20  42.0    0.476   10   14   0.714   6.0  31.0  37.0   27    5    7   15  22         1.0
    # 82       42018  1610612744               GSW  Golden State Warriors  0041800402  2019-06-02  GSW @ TOR  W  240  109   38   82   0.463    13  34.0    0.382   20   23   0.870   6.0  36.0  42.0   34    7    5   15  26         5.0
    # 83       42018  1610612744               GSW  Golden State Warriors  0041800401  2019-05-30  GSW @ TOR  L  239  109   34   78   0.436    12  31.0    0.387   29   31   0.935   9.0  29.0  38.0   29    6    2   16  27        -9.0
    # ....

    # -------------------------------------------------------------------------------------------------------
    sns.set_style('darkgrid')
    games_home['PTS'].hist()
    _, ax = plt.subplots()
    games_away.plot(x = 'GAME_DATE', y = 'PLUS_MINUS', ax = ax)
    games_home.plot(x = 'GAME_DATE', y = 'PLUS_MINUS', ax = ax)
    ax.legend(["away", "home"])
    plt.show()

if __name__ == '__main__':
    main()


