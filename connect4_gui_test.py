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
from connect4_gui_game import *
from tkinter import *
from functools import partial
import tkinter.font as font
import pickle

numrows = 4
numcols = 4

my_player_id = int(input('Which player do you want to be? Enter 1 or 2: \n'))
opponent_type = int(input('Who do you want to play? Enter 0 for random, 1 for minmax, 2 for AI player. \n'))
num_games = int(input('How many games do you want to play? \n'))


human_player = humanPlayer(my_player_id)
if opponent_type == 0:
    opponent_player = randomplayer(3-my_player_id)
elif opponent_type == 1:
    opponent_player = minmaxplayer(3-my_player_id, 6)

else: #if ai player
    file_name = 'qplayer_' + str(3-my_player_id) + '.pkl'
    file_obj = open(file_name,'rb')
    opponent_player = pickle.load(file_obj)
    
root = Tk()
ttf = connect4GuiGame(root, opponent_player,4,4,num_games)
ttf.mainloop()