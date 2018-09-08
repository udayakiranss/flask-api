import pandas as pd
import os as os
import numpy as np

matchesCSVPath = os.path.realpath('resources/matches-till-2018.csv')
deliveriesCSVPath = os.path.realpath('resources/deliveries-till-2018.csv')

print(matchesCSVPath)
matches = pd.read_csv(matchesCSVPath, sep=',', encoding='UTF-8')
deliveries = pd.read_csv(deliveriesCSVPath, sep=',', encoding='UTF-8')


def chasing(match):
    winner = match['winner']
    toss_winner = match['toss_winner']
    toss_decision = match['toss_decision']
    chasing = None
    if winner is not None:
        if winner == toss_winner:
            if toss_decision == 'field':
                chasing = winner
            else:
                chasing = toss_winner
        else:
            if toss_decision == 'field':
                chasing = toss_winner
            else:
                chasing = winner

    return chasing


matches['chasing'] = matches.apply(chasing, axis=1)

matches.to_csv('matches-chasing-2018.csv')

print(matches.head(0))
seasonList = []
deliveriesId = deliveries['match_id']
matchesId = matches[['id','season']]
counter = 0
for matchId in deliveriesId:
    counter +=1
    seasonList.append(matchesId.loc[matchesId['id'] == matchId, 'season'].iloc[0])
    if counter % 10000 == 0:
        print(counter)

print(seasonList)
deliveries['season'] = seasonList
deliveries.to_csv('deliveries_season-2018.csv')