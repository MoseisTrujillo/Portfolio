import ChessPngProcessing as CBSA
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from TestChessBulletSpeed import GrabPlayerSpeed

username = 'moseistrujillo'
gamenum = 10

MoveTimes, GameID, Result, Color = GrabPlayerSpeed(username,gamenum)


# plot the distrbution of games
moves = []
movesdist = pd.DataFrame({})
for i in range(gamenum):
    MoveTimes, GameID, Result, Color = GrabPlayerSpeed(username,i)
    moves.append(MoveTimes)
    df1 = pd.DataFrame({f'WhiteMoveTime{i}':MoveTimes['WhiteMoveTime']})
    df2 = pd.DataFrame({f'BlackMoveTime{i}':MoveTimes['BlackMoveTime']})
    movesdist = pd.concat([movesdist,df1,df2],axis = 1)

#(movesdist['WhiteMoveTime1']-movesdist['BlackMoveTime1'])
# sns.scatterplot(data = movesdist, x = movesdist.index, y = 'BlackMoveTime1', color = 'blue')
# plt.show()
f, ax = plt.subplots(figsize=(7, 7))
ax.set(yscale="log")
sns.scatterplot(data = MoveTimes, x = MoveTimes.index, y = 'WhiteMoveTime', color = 'blue')
sns.scatterplot(data = MoveTimes, x = MoveTimes.index, y = 'BlackMoveTime', color = 'red')
sns.regplot(data = MoveTimes, x = MoveTimes.index, y = 'WhiteMoveTime', color = 'blue')
plt.show()