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

    def _init_(self):
        pass

    def toJSON(self):
        return {
            'name': self.playername,
            'noOfMatches': self.noOfMatches,
            'totalRuns': int(self.runs),
            'totalWickets': int(self.wickets)
        }


class SeasonStatistics:

    def _init_(self):
        pass

    def toJSON(self):
        return {
            'season': self.playername,
            'winner': self.noOfMatches,
            'playerOfMatch': int(self.runs),
            'loser': int(self.wickets),
            'runs': self.runs,
            'wickets': self.wickets,
            'PlayerInningsDTO': {
                'totalRuns': 1,
                'totalWickets': 2
            }
        }




