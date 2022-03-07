# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:45:08 2021

@author: anany
"""


from tkinter import *

#create nine buttons in tictactoe grid

from functools import partial 
from random import randint
from machine_player import * 
from connect4state import *


class connect4GuiGame(Frame):
    def __init__(self,master,machinePlayer,numrows,numcols, num_games):
        Frame.__init__ (self,master)
        self.grid()
        self.master = master
        self.numrows = numrows
        self.numcols = numcols
        self.num_games = num_games
        self.C4State = C4State(numrows,numcols)
        self.machinePlayer = machinePlayer
        self.first_time = True    
        self.p1_cnt = 0
        self.p2_cnt = 0
        self.tie_cnt = 0
        self.reset() 
                 
    def on_click(self,r,c):
        game_over,checker = self.make_move(r,c)
        if game_over == False and checker == True:
            (r2,c2) = self.machinePlayer.get_move(self.C4State)
            self.make_move(r2,c2)
            
        
            
    def make_move(self,r,c):
        valid_moves = self.C4State.get_valid_moves(self.C4State.state)
        for (x,y) in valid_moves:
            if y == c:
                r = x
        
        checker = self.C4State.update_state(r,c)
        winner = 0 
        tie = False
        #print('checker',checker)
        if checker:
            self.update_board(r,c)
            winner = self.C4State.check_win()
            if winner == 1:
                self.p1_cnt += 1
                
            if winner == 2:
                self.p2_cnt += 1
                
            if self.C4State.check_draw() and winner == 0:
                self.tie_cnt += 1
                
            tie = self.C4State.check_draw()
            self.C4State.update_turn()
            self.end_game(winner,tie)
            
        if winner > 0 or tie: #someone won or board is full
            self.reset()
            return True,checker
        else:
            return False,checker
            
    

    def update_board(self,r,c):
        button = self.board[(r,c)] 
        if self.C4State.player_id == 1:
            button['bg'] = 'pale turquoise'
            
            
        elif self.C4State.player_id == 2:
            button['bg'] = 'light pink'
            
    
    
    def end_game(self,winner, tie):
        if winner == 0: #no winner
           if self.C4State.check_draw():
                for button in self.board.values():
                   button['state'] = DISABLED
                x = Label(self.master, text = 'The board is full', height = 8, width = 16)
                x.grid(row = 4, column = 1)
                    
        else:    
            for button in self.board.values():
                button['state'] = DISABLED
            m = "Player " + str(winner) + " has won!"
            x = Label(self.master, text = m, height = 8, width = 16)
            x.grid(row = 4, column = 1)
        return

    def clear_text(self):
        x = Label(self.master, text = '', height = 8, width = 16)
        x.grid(row = 4, column = 1)
       

    def destroy_frame(self):
         self.master.destroy()
         
    def reset(self):
        self.num_games = self.num_games - 1
        if self.num_games < 0:
            self.master.after(2000, self.destroy_frame)
            print('-------- GAME SUMMARY --------')
            print('Player 1 won', self.p1_cnt, 'games!')
            print('Player 2 won', self.p2_cnt, 'games!')
            print('Both players tied on', self.tie_cnt, 'games!')
            #print('Finished playing all games')
            # Need to print count of games won/lost/tied here
            return
        #print('Calling state reset')
        self.C4State.reset()
        
        #print(self.first_time)
        if self.first_time:
            self.board = {}
            for row in range (0,self.numrows):
                for col in range (0,self.numcols):   
                    on_click_partial = partial(self.on_click,r = row, c=col)
                    a = Button(self.master, height=8, width= 16, bg = 'white', command = on_click_partial)
                    a.grid(row=row,column=col)
                    self.board[(row,col)] = a
            
            self.first_time=False
        else:           
            for button in self.board.values():
                button['bg'] = 'white'
                button['state'] = NORMAL
                button.grid()
            self.master.after(1000, self.clear_text)
 
        self.grid()
        if self.machinePlayer.player_id == 1:
            move = self.machinePlayer.get_move(self.C4State)
            self.make_move(move[0],move[1])
