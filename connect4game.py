# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 22:14:41 2021

@author: anish
"""

from tkinter import *
from functools import partial
import tkinter.font as font
from random import randint
from machine_player import *
from connect4state import *

class C4Game(object):

    def __init__(self, player1, player2, numrows, numcols):
        self.players = [0,0]
        self.players[0] = player1
        self.players[1] = player2 
        self.C4State = C4State(numrows,numcols)
            
    def make_move(self):
     row, column = self.players[self.C4State.player_id-1].get_move(self.C4State)
     checker = self.C4State.update_state(row, column)
    
     check_win = self.C4State.check_win()  
     tie = self.C4State.check_draw()  
    
     return check_win, tie
    
        
    def play_game(self):
        game_over = False
        while(game_over == False):
            winner, draw = self.make_move()
            if(winner == 1 or winner == 2 or draw == True):
                game_over = True
            else:
                self.C4State.update_turn()
        
        return winner, draw
    
    def reset(self):
        self.C4State.reset()
        for player in self.players:
            player.reset_player()
            


def print_move_history(m, x):
    for element in m:
        state = x.C4State.number_to_state(element[1])
        x.C4State.print_state(state) 
        print(element[0])
        

