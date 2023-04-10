import pandas as pd
import requests
import chessdotcom as chesscom

#grabs games for Username and saves them to a csv file


Username = 'moseistrujillo'

data = chesscom.get_player_game_archives(Username).json #returns a dictionary of urls to each month of games

GameID = []
GamePGN = []
ArchiveRange = len(data['archives'])
for month in range(ArchiveRange-12,ArchiveRange): #currently only getting last 12 months
    url = data['archives'][month]
    games = requests.get(url).json() #gets each game played in the month
    for gameNum in range(len(games['games'])): #grab the game id and pgn for each game
        try: #most games are live, but some are daily
            GameID.append(games['games'][gameNum]['pgn'].split('live/')[1].split('"')[0])
        except IndexError:
            GameID.append(games['games'][gameNum]['pgn'].split('daily/')[1].split(' ')[0])
        GamePGN.append(games['games'][gameNum]['pgn'])
GameReadyToSave = pd.DataFrame(list(zip(GameID,GamePGN)), columns= ['GameID','GamePGN']) #convert to dataframe
GameReadyToSave.to_csv(f'B:\ChessGameStorage\{Username}.csv',index = False, mode = 'a')