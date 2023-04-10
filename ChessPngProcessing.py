import chessdotcom as chesscom
import requests

#Functions to process the time aspect of game data




Username = 'MoseisTrujillo'


#This gives a list of all the API Urls where the players games are stored
#The format is a dictionary with list of each year/month and the url to the games
archive = requests.get(f'https://api.chess.com/pub/player/{Username}/games/archives').json()



#get my most recent game from chesscom
def get_most_recent_game(username):
        data = chesscom.get_player_game_archives(username).json
        url = data['archives'][-1]
        games = requests.get(url).json()
        game = games['games'][-1]['pgn']   
        return game 



#Since the game is given to me as a string, I need to convert it to a list of moves
#consider adding another return variable to tell time control
def TimeToPlayB(Game):    
    GameList =  Game.split('clk ')
    MoveTimes = []
    for i in range(1,len(GameList)):
        TimeStamp = GameList[i].split(']')[0] #get time stamp in format hh:mm:ss
        TimeStamp = TimeStamp.split(':') #split up time to convert to seconds
        Time = float(TimeStamp[0])*3600 + float(TimeStamp[1])*60 + float(TimeStamp[2]) #convert to seconds
        MoveTimes.append(Time)
    if len(MoveTimes)%2 == 1:
        MoveTimes.append(0)
    return MoveTimes



#Since the move times are given sequatially, white and black moves need to be seperated
#also throws out them into a dictionary to make ez conversion to Pandas dataframe
def MoveTimeSeperate(MoveTime):
    WhiteMoves=[]
    BlackMoves=[]
    for i in range(len(MoveTime)):
        if i%2 == 0:
            WhiteMoves.append(float(MoveTime[i]))
        else:
            BlackMoves.append(float(MoveTime[i]))
    return {'WhiteMoves':WhiteMoves,
             'BlackMoves':BlackMoves,}






#Calculate the time per move
def TimePerMove(MoveTimesdf):
    MoveTimesdf['WhiteMoveTime'] = -MoveTimesdf['WhiteMoves'].diff()[1:]
    MoveTimesdf['BlackMoveTime'] = -MoveTimesdf['BlackMoves'].diff()[1:]
    return MoveTimesdf



