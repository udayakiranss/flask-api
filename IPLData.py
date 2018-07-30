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

