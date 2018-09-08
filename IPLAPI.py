from flask import Flask, Response
from flask import json
from IPLDataReader import get_winner, \
    get_batsman_runs, get_bowler_wickets, team_stats, \
    get_batsman_runs_overall, get_bowler_wickets_overall, get_matches, get_abandoned_matches, orange_cap, purple_cap, season_teams
from IPLDataReader import get_loser, get_season_stats, get_batsman_like
from IPLData import Player, SeasonTeamPointsDTO

app = Flask(__name__)


@app.route('/')
def welcome_message():
    return "Welcome to Python IPL API"


# @auth.verify_password
# def verify(username, password):
#     if not (username and password):
#         return False
#     return USER_DATA.get(username) == password


@app.route('/iplstats/winner/<int:season>')
def ipl_winner(season):
    return "Winner of season %s is %s" % (str(season), get_winner(season)['winner'])


@app.route('/iplstats/loser/<int:season>')
def ipl_loser(season):
    match_details = get_loser(season)
    winner = match_details['winner']
    if winner == match_details['team1']:
        loser = match_details['team2']
    else:
        loser = match_details['team1']
    return "Loser of season %s is %s" % (str(season), loser)


@app.route('/iplstats/season/<int:season>')
def ipl_seasonstat(season):
    seasonstr = get_season_stats(season)
    # st = season_teams(season)
    js = json.dumps(seasonstr)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


@app.route('/iplstats/team/<stat_team>')
def team_statistics(stat_team):
    season_points = team_stats(stat_team, None, None)
    print(season_points.totalMatchesPlayed)
    total_matches = season_points.totalMatchesPlayed
    winning_matches = season_points.wonMatches
    return "%s won %s matches out of %s matches in IPL" % (stat_team, winning_matches, total_matches)


@app.route('/iplstats/season/<int:season>/player/<player>')
def player_stats_season(season, player):
    player_exact = get_batsman_like(player)

    batsman_runs = get_batsman_runs(player_exact, season)
    bowler_wickets = get_bowler_wickets(player_exact, season)
    player_matches = get_matches(season, player_exact)

    player_obj = Player()
    player_obj.runs = batsman_runs
    player_obj.wickets = bowler_wickets
    player_obj.noOfMatches = player_matches
    player_obj.playername = player_exact
    player_obj.season= season

    js = json.dumps(player_obj.toJSON())

    resp = Response(js, status=200, mimetype='application/json')

    return resp
    # return "%s scored %s runs and taken %s wickets in %s matches of season %s" % (player, batsman_runs,
    #                                                                               bowler_wickets, player_matches,
    #                                                                               season)


@app.route('/iplstats/season/<int:season>/team/<stat_team>/<is_chasing>')
def season_team_chasing_percent(season, stat_team, is_chasing):
    season_team_stats  = team_stats(stat_team, season, is_chasing)

    if is_chasing == True:
        winning_percentage = (season_team_stats.winning_chasing_matches * 100) / season_team_stats.totalMatchesPlayed
        return "%s's winning percentage while chasing is %s" \
               % (stat_team, winning_percentage)
    else:
        winning_percentage = ((season_team_stats.totalMatchesPlayed - season_team_stats.winning_chasing_matches) * 100) / season_team_stats.totalMatchesPlayed
        return "%s's winning percentage while defending is %s" \
               % (stat_team, winning_percentage)


@app.route('/iplstats/season/<int:season>/team/<stat_team>')
def season_team_statistics(season, stat_team):
    season_team_stats  = team_stats(stat_team, season,None)
    print(season_team_stats.totalMatchesPlayed)
    js = json.dumps(season_team_stats.toJSON())

    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/iplstats/season/<int:season>/orangecap')
def orange_cap_player(season):
    orange_player = orange_cap(season)
    js = json.dumps(orange_player)

    resp = Response(js, status=200, mimetype='application/json')
    return resp
    # player, player_runs = orange_cap(season)
    # return "%s got orange cap in %s for scoring %s runs" % (player, season, player_runs)


@app.route('/iplstats/season/<int:season>/purplecap')
def purple_cap_player(season):
    purple_player = purple_cap(season)
    js = json.dumps(purple_player)

    resp = Response(js, status=200, mimetype='application/json')
    return resp
    # player, player_wickets = purple_cap(season)
    # return "%s got purple cap in %s for getting %s wickets" % (player, season, player_wickets)


@app.route('/iplstats/player/<player>')
def player_stats(player):
    player_exact = get_batsman_like(player)
    batsman_runs = get_batsman_runs_overall(player_exact)
    bowler_wickets = get_bowler_wickets_overall(player_exact)
    player_matches = get_matches(None, player_exact)

    player_obj = Player()
    player_obj.runs = batsman_runs
    player_obj.wickets = bowler_wickets
    player_obj.noOfMatches = player_matches
    player_obj.playername = player_exact

    js = json.dumps(player_obj.toJSON())

    resp = Response(js, status=200, mimetype='application/json')

    return resp

    # return "%s scored %s runs and taken %s wickets in %s matches of IPL" % (player, batsman_runs,
    #                                                                         bowler_wickets, player_matches)


@app.route('/iplstats/abandoned')
def abandoned_matches():
    abandoned_match_list = get_abandoned_matches()

    # convert to json data
    json_str = json.dumps([e for e in abandoned_match_list])
    return json_str


if __name__ == '__main__':
    app.run(debug=1, host='0.0.0.0')
