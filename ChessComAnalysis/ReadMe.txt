Read Me

This Folder contains Analysis done on Chess games from the site Chess.com. Currently the Username is set to 'moseistrujillo',
but it can be changed to any valid Chess.com Username. This folder contains PNG processing functions, aggregation of games, and plotting simple descriptions.

•The file ChessGameGrabber saves the past 12 months worth of games to a local drive.
•ChessPngProcessing contains several functions used to process the PGN from the chesscom API. (since the pgn is not in the standard form of a pgn)
•TestChessBulletSpeed runs a function that collects the move times from the past N games for Username. it also contains simple plots after the main function
•PlotMoveDist is the beginning of graphical/exploratory analysis on games. currently is a work in progress to plot the distribution of move times.





Additional analysis to be done is vast in nature. Current goals are:
Logistic analysis to determine weather a chess game was won or lost based on to-be-determined characteristics(ie. Date, avg move time, elo, time of day etc.). 
correlation drawing from move speed to quality of play (Chess Engine integration needed as well)
Deep learning machine to learn how to play chess in the same way I do (probably too hard lol)
create personal opening book (fiind fequency of intial first N moves played in any given game)


