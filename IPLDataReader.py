import pandas as pd
import os as os
import numpy as np
from IPLData import Match, SeasonStatistics, Player, SeasonTeamPointsDTO

# colNames = ['id', 'season', 'city', 'date', 'team1', 'team2', 'toss_winner', 'toss_decision', 'result', 'dl_applied',
#             'winner',
#             'win_by_runs', 'win_by_wickets', 'player_of_match', 'venue', 'umpire1', 'umpire2', 'umpire3']
matchesCSVPath = os.path.realpath('resources/matches_chasing.csv')
deliveriesCSVPath = os.path.realpath('resources/deliveries_season.csv')

print(matchesCSVPath)
matches = pd.read_csv(matchesCSVPath, sep=',', encoding='UTF-8')

deliveries = pd.read_csv(deliveriesCSVPath, sep=',', encoding='UTF-8')

print("Loading matches")
print(matches.head(0))

# Group the matches by season
season_group_by = matches.groupby('season')

deliveries_season_group = deliveries.groupby(['season'])


def get_winner(season):
    return season_group_by.get_group(season).tail(1).iloc[0, 1:15]


def get_loser(season):
    return season_group_by.get_group(season).tail(1).iloc[0, 1:15]


def get_season_stats(season):
    shortlisted_matches = season_group_by.get_group(int(season))
    match_details = shortlisted_matches.tail(1).iloc[0, 1:15]
    winner = match_details['winner']
    if winner == match_details['team1']:
        loser = match_details['team2']
    else:
        loser = match_details['team1']

    manOfMatch = match_details['player_of_match']
    win_by_runs = match_details['win_by_runs']
    win_by_wickets = match_details['win_by_wickets']

    season_stat = SeasonStatistics()
    season_stat.season = int(season)
    season_stat.winner = winner
    season_stat.loser = loser
    season_stat.mom = manOfMatch
    season_stat.by_runs = int(win_by_runs)
    season_stat.by_wickets = int(win_by_wickets)

    mom_wickets = get_bowler_wickets_match(manOfMatch,season,match_details['id'])
    mom_runs = get_batsman_runs_match(manOfMatch, season, match_details['id'])

    mom_player = Player()
    mom_player.playername = manOfMatch
    mom_player.runs = int(mom_runs)
    mom_player.wickets = int(mom_wickets)

    season_stat.player = mom_player.toJSON()

    season_stat.season_team_points_set = season_teams(season)

    return season_stat.toJSON()


def get_winner_count(winner_team):
    return season_group_by.tail(1).loc[:, ['season', 'winner']].groupby('winner').count().loc[winner_team, 'season']


def get_batsman_runs_overall(batsman):
    return deliveries.groupby(['batsman']).get_group(batsman)['batsman_runs'].sum()


def get_batsman_runs(batsman, season):
    return deliveries_season_group.get_group(season).groupby('batsman').get_group(batsman)['batsman_runs'].sum()


def get_batsman_runs_match(batsman, season, match):
    return deliveries_season_group.get_group(season).groupby('match_id').get_group(match).groupby('batsman').\
        get_group(batsman)['batsman_runs'].sum()


def get_bowler_wickets(bowler, season):
    try:
        bowler_wickets = deliveries_season_group.get_group(season).groupby('bowler').\
            get_group(bowler)['dismissal_kind'].count()
        return bowler_wickets
    except:
        return 0

def get_bowler_wickets_match(bowler,season, match):
    try:

        bowler_wickets = deliveries_season_group.get_group(season).groupby('match_id').get_group(match).groupby('bowler').\
            get_group(bowler)['dismissal_kind'].count()
        return bowler_wickets
    except:
        return 0

def get_bowler_wickets_overall(bowler):
    return deliveries.groupby(['bowler']).get_group(bowler)['dismissal_kind'].count()


def get_matches_season(batsman, season):
    return deliveries_season_group.get_group(season).groupby('batsman').get_group(batsman)['match_id'].unique().size


def get_matches(batsman):
    return deliveries.groupby('batsman').get_group(batsman)['match_id'].unique().size


def get_abandoned_matches():
    abandoned_matches = matches[matches.loc[:, 'winner'].isnull()].loc[:, ['id', 'team1', 'team2', 'venue', 'date']]
    match_list = []

    for index, row in abandoned_matches.iterrows():
        match = Match(row['id'], row['date'], row['venue'], row['team1'], row['team2'])
        match_list.append(match.toJSON())

    return match_list


def orange_cap(season):
    player = deliveries_season_group.get_group(season).groupby('batsman').\
        agg(np.sum).sort_values(by='batsman_runs').tail(1)['batsman_runs'].index[0]
    player_runs = deliveries_season_group.get_group(season).groupby('batsman').\
        agg(np.sum).sort_values(by='batsman_runs').tail(1)['batsman_runs'].iloc[0]

    orange_cap_player = Player()
    orange_cap_player.playername = player
    orange_cap_player.runs = player_runs
    orange_cap_player.season = season

    return orange_cap_player.toJSON()


def purple_cap(season):
    player = deliveries_season_group.get_group(season).groupby('bowler')['dismissal_kind']\
        .count().sort_values().tail(1).index[0]
    player_wickets = deliveries_season_group.get_group(season).groupby('bowler')['dismissal_kind']\
        .count().sort_values().tail(1).iloc[0]
    purple_cap_player = Player()
    purple_cap_player.playername = player
    purple_cap_player.wickets = player_wickets
    purple_cap_player.season = season

    return purple_cap_player.toJSON()
    # return player, player_wickets


def between_team_stats(team1, team2):
    search_for = [team1, team2]
    m_condition = (matches['team1'].str.contains('|'.join(search_for)) |
                   matches['team2'].str.contains('|'.join(search_for)))
    return matches.loc[m_condition]


def team_stats(stat_team, season, is_chasing):
    winning_chasing_matches = 0
    if season is not None:
        shortlisted_matches = season_group_by.get_group(int(season))
    else:
        shortlisted_matches = matches

    team_matches_condition = (shortlisted_matches['team1'] == stat_team) | (shortlisted_matches['team2'] == stat_team)
    total_matches = shortlisted_matches[team_matches_condition].loc[:, ['team1']].count().loc['team1']

    winner_condition = ((shortlisted_matches['team1'] == stat_team) | (shortlisted_matches['team2'] == stat_team)) & \
                               (matches['winner'] == stat_team)

    if is_chasing :
        winner_chasing_condition = winner_condition & (shortlisted_matches['chasing'] == stat_team)
        winning_chasing_matches = shortlisted_matches[winner_chasing_condition].loc[:, ['winner']].count().loc['winner']

    winning_matches = shortlisted_matches[winner_condition].loc[:, ['winner']].count().loc['winner']

    points = winning_matches * 2

    # print()
    print("%s won %s matches out of %s matches in IPL" % (stat_team, winning_matches, total_matches))
    if is_chasing:
        print(" while chasing")

    lostMatches = total_matches - winning_matches
    noResultMatches = 0


    team_season_points =  SeasonTeamPointsDTO()
    team_season_points.teamName = stat_team
    team_season_points.totalMatchesPlayed = total_matches
    team_season_points.wonMatches = winning_matches
    team_season_points.points = points
    team_season_points.lostMatches = lostMatches
    team_season_points.winning_chasing_matches = winning_chasing_matches
    team_season_points.noResultMatches = noResultMatches

    return team_season_points


def season_teams(season):
    shortlisted_matches = season_group_by.get_group(int(season))
    team_list = shortlisted_matches['team1'].unique().tolist()
    season_team_stat_list = []
    for team in team_list:
        print(team)
        season_team_stat = team_stats(team,season,None)
        season_team_stat_list.append(season_team_stat.toJSON())

    return season_team_stat_list
