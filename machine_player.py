# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:00:45 2021

@author: anish
"""
from tkinter import *
from functools import partial
import tkinter.font as font
import random
from random import randint
import copy
import numpy as np

class randomplayer(object):
    def __init__(self, player_id):
        self.player_id= player_id
        self.counter = 0 
        
        
    def get_random_move2(self, state_object):
        
        state = state_object.state
        valid_moves = state_object.get_valid_moves(state)
        
        num = len(valid_moves)
        move_coord = random.randint(0,num-1)
        return valid_moves[move_coord]
       
    def get_move(self, state_object):
        return self.get_random_move2(state_object)

    def set_playerid(self, playerid):
        self.player = playerid

    def train(self, win):
        return 
    def reset_player(self):
        return
    
    def set_threshold(self, threshold):
        return
        
class smartMC(randomplayer):
    def get_move(self, state_object):
        state_copy = copy.deepcopy(state_object)
        state = state_copy.state
        counter = 0
        for (r,c) in state:
            if state[(r,c)] == 0:
                state[(r,c)] = state_copy.player_id
                if(state_copy.check_win() == state_copy.player_id):
                    counter = 1

                    break 
                else:
                    state[(r,c)] = 0
        if(counter == 0):
           return self.get_random_move(state_object)
        else:
           return (r,c)
    
    
class minmaxplayer(randomplayer):
    def __init__(self, playerid, maxdepth):
        
        randomplayer.__init__(self,playerid)
        self.max_depth = maxdepth
        
        
    def get_move(self, state_object):
        
        move,_= self._max(state_object, 0) 
        
    
        return move
        
    def _max(self, state_object, cnt_depth):
        
        cnt_depth+=1
        state = state_object.state
        valid_moves = state_object.get_valid_moves(state)
        best_score = -10  
        best_move = (0,0)
        
        for move in valid_moves:
            state_copy = copy.deepcopy(state_object)
            state = state_copy.state
            state[move] = state_copy.player_id
            if(state_copy.check_win() == state_copy.player_id):
                best_score = 10
                return move, best_score
            else:
                if state_copy.check_draw():
                    score =0
                else:
                    if(cnt_depth <self.max_depth):
                        
                        score = self._min(state_copy, cnt_depth)
                    else:
                        score=0
            if(best_score<=score):
                best_score = score
                best_move = move
                
                
        return best_move, best_score      
        
        
    
    def _min(self, state_object, depth_cnt):
        depth_cnt+=1
        
        if(state_object.player_id == 1):
            player_id = 2
        else:
            player_id = 1
        state = state_object.state
        valid_moves = state_object.get_valid_moves(state)
        worst_score = 10
        
        for move in valid_moves:
            
            state_copy = copy.deepcopy(state_object)
            state = state_copy.state
            state[move] = player_id
            if(state_copy.check_win() == player_id):
                worst_score = -10
                return worst_score
            else:
                if state_copy.check_draw():
                    score = 0
                else:
                    if(depth_cnt<self.max_depth):
                    
                       _,score = self._max(state_copy, depth_cnt)
                    else:
                        score = 0
            if(worst_score >= score):
                worst_score = score
        return worst_score
                


            

        
    
class Qplayer(randomplayer):
    
    def __init__(self, playerid, reward, qinit, lrate, dfactor, numrows, numcols, threshold):
        self.numrows = numrows
        self.numcols = numcols
        self.player_id = playerid
        self.move_history = []
        self.reward_list = reward 
        self.Qtable = {} #key is state as anumber, the value, are the rewards for each action
        self.qinit = qinit
        self.lrate = lrate
        self.dfactor = dfactor
        self.threshold = threshold 
        
        
    def move_to_num(self, r, c):
        return self.numcols*r + c
    
    def num_to_move(self, num):
        x = num//(self.numcols)
        y = num%(self.numcols)
        return (x,y)
        
    
    def get_random_move(self, state_object):
        x = self.get_q(state_object)
      
        x = randomplayer.get_move(self, state_object)
        k = self.move_to_num(x[0], x[1]) 
        y = state_object.state_to_number(state_object.state)
        
        return x 
        
    def get_move(self, state_object):
        v = np.random.rand(1)
       
        if v[0] > self.threshold:
            x = self.get_optimal_move(state_object)
        else:
            x = self.get_random_move(state_object)
    
        num  = self.move_to_num(x[0],x[1])
        y = state_object.state_to_number(state_object.state)
        self.move_history.append((num,y))
        return x

    def get_reward(self, win):
        
        
        if(win == self.player_id):
            reward = self.reward_list[2]
        elif(win == 0):
            reward =self.reward_list[1]
        else:
            reward = self.reward_list[0]
        return reward 
    
    
    def reset_player(self):
        self.move_history = []
        
    def get_q(self, state_object):
        
        num = state_object.state_to_number(state_object.state)
        valid_moves = state_object.get_valid_moves(state_object.state)
        
        if(num not in self.Qtable):
        
            self.Qtable[num] = self.numrows*self.numcols*[-1]
            for i in range(0,self.numrows):
                for j in range(0,self.numcols):
                    
                    if((i,j) not in valid_moves):
                        
                        x = self.move_to_num(i,j)
                        self.Qtable[num][x] = -1
                    else:
                        x = self.move_to_num(i,j)
                        
                        self.Qtable[num][x] = self.qinit
                        
        return self.Qtable[num]
        
                         
    def get_optimal_move(self, state_object):

        x = self.get_q(state_object)
        m = np.argmax(x)
        coord = self.num_to_move(m)
        return coord
        
        
    def train(self, win):
        
        self.move_history.reverse()
        r= self.get_reward(win)
        bool_first_time = True
        for element in self.move_history:
            action = element[0]
            state = element[1]
            if(bool_first_time == True):
                
                self.Qtable[state][action] = r
                bool_first_time = False
            else:
                self.Qtable[state][action] = self.Qtable[state][action]*(1-self.lrate) + self.lrate*self.dfactor*next_max
            
            next_max = max(self.Qtable[state])
        
 
    def set_threshold(self, threshold):
        self.threshold = threshold

class humanPlayer(randomplayer):
    def get_move(self, state_obj):
        state_obj.print_state(state_obj.state)
        y = state_obj.numcols + 1
                
        while y not in range(0,state_obj.numcols):
            x = int(input('Which column do you want to play in? \n'))
            valid_moves = state_obj.get_valid_moves(state_obj.state)
            if x not in range(0, state_obj.numcols):
                print('The column is out of range!')
                continue
            #print(valid_moves)
            for element in valid_moves:
                #print(element[0], element[1])
                if element[1] == x:
                    return (element[0], element[1])
                
            y = state_obj.numcols + 1
            
            print('Sorry, the Column is full. PLEASE PICK ANOTHER COLUMN!')
        
