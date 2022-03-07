# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 13:44:01 2021

@author: anish
"""

from tkinter import *
from functools import partial
import tkinter.font as font
from random import randint
from machine_player import *
from connect4game import *
import pickle

numrows = 4
numcols = 4

my_player_id = int(input('Which player do you want to be? Enter 1 or 2: \n'))
opponent_type = int(input('Who do you want to play? Enter 0 for random, 1 for minmax, 2 for AI player. \n'))
num_games = int(input('How many games do you want to play? \n'))

human_player = humanPlayer(my_player_id)
if opponent_type == 0:
    opponent_player = randomplayer(3-my_player_id)
if opponent_type == 1:
    opponent_player = minmaxplayer(3-my_player_id,3)

else: #if ai player
    file_name = 'qplayer_' + str(3-my_player_id) + '.pkl'
    file_obj = open(file_name,'rb')
    opponent_player = pickle.load(file_obj)
    
    
if my_player_id == 1:
    x = C4Game(human_player, opponent_player, numrows,numcols)
if my_player_id == 2:
    x = C4Game(opponent_player, human_player, numrows,numcols)

player_1_cnt = 0
player_2_cnt = 0
tie_cnt = 0

for i in range (0,num_games):
    m,n = x.play_game()
    #print('move history,', player2.move_history)
    #print('q table length:', len(player2.Qtable))
    if(m != 0 ):
        if m == 1:
            player_1_cnt += 1
        if m == 2:
            player_2_cnt += 1
            
        print('The winner is player', m)
        
    else:
        tie_cnt += 1
        print('The players tied :/')
        
    x.C4State.print_state(x.C4State.state)
    print('--------------- GAME OVER! ---------------')
    x.reset()

print('GAME(S) Summary')
print('Number of games player 1 won:', player_1_cnt)
print('Number of games player 2 won:', player_2_cnt)
print('Number of tie games', tie_cnt)
