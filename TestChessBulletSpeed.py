import ChessPngProcessing as CBSA
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

Username = 'moseistrujillo'
GameDataFile = pd.read_csv(f'B:\ChessGameStorage\{Username}.csv')
def GrabPlayerSpeed(Username,GameNum):
#username is which user wanted to analyze, GameNum is the number of games wanted to analyze
    
    
    # GameDat = pd.read_csv('B:\ChessGameStorage\GameStorageTo04_23.csv')
    CurrentGame = GameDataFile['GamePGN'][GameNum]
    CurrentID = GameDataFile['GameID'][GameNum]

    IsWhite = False #determines if player is white or black
    if CurrentGame.split('White')[1][2:(2+len(Username))].lower() == Username:
        IsWhite = True
    Color = 'White' if IsWhite == True else 'Black'

    if CurrentGame.split('Result')[1][2:5] == '1-0': #find outcome of each game
        if IsWhite == True:
            Result = 'Win'
        else:
            Result = 'Lose'
    if CurrentGame.split('Result')[1][2:5] == '0-1':
        if IsWhite == True:
            Result = 'Lose'
        else:
            Result = 'Win'
    if CurrentGame.split('Result')[1][2:5] not in ['1-0','0-1']:
        Result = 'Draw'

    #Determine How the game ended (checkmate, stalemate, draw, etc)
    #Result = CurrentGame.split('Termination "')[1].split('"',1)[0]


    MoveTime = CBSA.TimeToPlayB(CurrentGame)

    MoveList = CBSA.MoveTimeSeperate(MoveTime)

    MoveTimesdf = pd.DataFrame(MoveList)

    #Add the timer per-move to the time dataframe
    MoveTimesdf = CBSA.TimePerMove(MoveTimesdf)  

    return MoveTimesdf[['WhiteMoveTime','BlackMoveTime']],CurrentID,Result, Color
# GrabPlayerSpeed(Username)


#store the data in a dictionary GameData
GameData = {}
for GameNum in range(2000):
    MoveTimes, GameID, Result, Color = GrabPlayerSpeed(Username,GameNum)
    GameData[GameID] = {'MoveTimes':MoveTimes, 'Result':Result, 'Color':Color}


#Determin which column were my moves
if GameData[GameID]['Color'] == 'White':
    MyMoves = GameData[GameID]['MoveTimes']['WhiteMoveTime']
    OppMoves = GameData[GameID]['MoveTimes']['BlackMoveTime']
else:
    MyMoves = GameData[GameID]['MoveTimes']['BlackMoveTime']
    OppMoves = GameData[GameID]['MoveTimes']['WhiteMoveTime']





# print(GameData['42841256615'])
#Identifies and addes User's avarge move time and Opponent's average move time to the GameData dictionary
for ID in GameData.keys():
    if GameData[ID]['Color'] == 'White':
        MyMoves = GameData[ID]['MoveTimes']['WhiteMoveTime']
        OppMoves = GameData[ID]['MoveTimes']['BlackMoveTime']
    else:
        MyMoves = GameData[ID]['MoveTimes']['BlackMoveTime']
        OppMoves = GameData[ID]['MoveTimes']['WhiteMoveTime']
    GameData[ID]['MyMovesAVG'] = MyMoves.mean()
    GameData[ID]['OppMovesAVG'] = OppMoves.mean()




#create the MoveTimeDf dataframe which contains the average move time for the user and thier opponents
MyAverageMoveTime = []
OppAverageMoveTime = []
Results = []
Color = []
for ID in GameData.keys():
    MyAverageMoveTime.append(GameData[ID]['MyMovesAVG'])
    OppAverageMoveTime.append(GameData[ID]['OppMovesAVG'])
    Results.append(GameData[ID]['Result'])
    Color.append(GameData[ID]['Color'])

MoveTimeDf = pd.DataFrame({'MyTime':MyAverageMoveTime,'OppTime':OppAverageMoveTime, 'Result':Results, 'Color':Color})

MoveTimeDf.to_csv(f'B:\ChessGameStorage\{Username}MoveTimeDf.csv')


#boolean variables for filtering the MoveTimeDf dataframe
Wins = MoveTimeDf['Result']=='Win'
Loses = MoveTimeDf['Result']=='Lose'
Draw = MoveTimeDf['Result']=='Draw'
White = MoveTimeDf['Color']=='White'
Black = MoveTimeDf['Color']=='Black'


#plot the data
Domain = (0,3)
figure, axis = plt.subplots(2,2,figsize=(10,8))
sns.histplot(data=MoveTimeDf[Wins & White],x='MyTime', bins=50, color='red',ax=axis[0,0],binrange=Domain, stat='count').set_title(f'White Wins')
sns.histplot(data=MoveTimeDf[Wins & Black],x='MyTime', bins=50, color='blue',ax=axis[1,0],binrange=Domain,stat='count').set_title('Black Wins')
sns.histplot(data=MoveTimeDf[Loses & White],x='MyTime', bins=50, color='Orange',ax=axis[0,1],binrange=Domain, stat='count').set_title('White Loses')
sns.histplot(data=MoveTimeDf[Loses & Black],x='MyTime', bins=50, color='Cyan',ax=axis[1,1],binrange=Domain, stat='count').set_title('Black Loses')
plt.show(block = False)
plt.pause(0.001)

print(MoveTimeDf['MyTime'].mean(),MoveTimeDf['OppTime'].mean())

plt.show()