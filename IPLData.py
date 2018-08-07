class Match:

    def __init__(self, matchId, date, venue, teamA, teamB):
        self.matchID= matchId
        self.date = date
        self.venue = venue
        self.teamA = teamA
        self.teamB = teamB

    def toJSON(self):
        return {
            'matchid': self.matchID,
            'date': self.date,
            'venue':self.venue,
            'teamA':self.teamA,
            'teamB':self.teamB
        }


class Player:
    playername = ''
    noOfMatches = 0
    runs = 0
    wickets = 0
    season = None

    def _init_(self):
        pass

    def toJSON(self):
        return {
            'name': self.playername,
            'noOfMatches': self.noOfMatches,
            'totalRuns': int(self.runs),
            'totalWickets': int(self.wickets),
            'season': self.season
        }


class SeasonStatistics:
    season = 0
    winner = ''
    mom = ''
    by_runs = 0
    by_wickets = 0
    player = None

    def _init_(self):
        pass

    def toJSON(self):
        return {
            'season': self.season,
            'winner': self.winner,
            'playerOfMatch': self.mom,
            'loser': self.loser,
            'runs': self.by_runs,
            'wickets': self.by_wickets,
            'PlayerInningsDTO' : self.player
        }



