# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 19:34:08 2022

@author: anish
"""
from tkinter import *
from functools import partial
import tkinter.font as font
from random import randint
from machine_player import *
from connect4state import *
from connect4game import * 
import matplotlib.pyplot as plt 
import pickle


def print_move_history(m, x):
    for element in m:
        state = x.C4State.number_to_state(element[1])
        
  
def print_q_table(qtable):
    for element in qtable:
        print( element, qtable[element])
        
        
def train(lrate, dfactor, num_games, qplayer_num, qinit, numrows, numcols, threshold, other_player_type):
    
    if(qplayer_num == 2):
        player2 = Qplayer(qplayer_num, [0,5,10], qinit, lrate, dfactor, numrows, numcols, threshold)
        if other_player_type == 'random':
            player1 = randomplayer(1)
        elif other_player_type == 'minmax':
            player1 = minmaxplayer(1, 2)
        elif other_player_type == 'qplayer':
            player1 = Qplayer(1, [0,5,10], qinit, lrate, dfactor, numrows, numcols, threshold)

    if(qplayer_num == 1):
        player1 = Qplayer(qplayer_num, [0,5,10], qinit, lrate, dfactor, numrows, numcols, threshold)
        if other_player_type == 'random':
            player2 = randomplayer(2)
        elif other_player_type == 'minmax':
            player2 = minmaxplayer(2, 2)
        elif other_player_type == 'qplayer':
            player2 = Qplayer(2, [0,5,10], qinit, lrate, dfactor, numrows, numcols, threshold)

        
    x= C4Game(player1, player2, numrows, numcols)
    cnt_1 = 0 
    cnt_2 = 0   
    tie_cnt = 0 
    list_win = []
    
    for i in range(0,num_games):
        
        win, tie = x.play_game()
        if(win == 1):
            cnt_1+=1
        elif(win == 2):
            cnt_2+=1
        else:
            tie_cnt+=1
       # x.C4State.print_state(x.C4State.state)
       # print(win, 'won')
       # print('\n')
        if i%20000 ==0:
            print(i)
            if hasattr(player1, 'Qtable'):
                print(len(player1.Qtable))   
            if hasattr(player2, 'Qtable'):
                print(len(player2.Qtable))
                
        list_win.append(win)
        player2.train(win)
        player1.train(win)
        x.reset() 

    return [player1, player2],list_win


def test(player1, player2, num_games, numrows, numcols):
    
    cnt_1 = 0
    cnt_2 = 0
    tie_cnt = 0
    list_win_2 = [] 
    
    player2.set_threshold(0)
    player1.set_threshold(0)
    
    x= C4Game(player1, player2, numrows, numcols)
    
    for i in range(0,num_games):
        
        win, tie = x.play_game()
        if(win == 1):
            cnt_1+=1
            
        elif(win == 2):
            cnt_2+=1
            
        else:
            tie_cnt+=1
        
     #   x.C4State.print_state(x.C4State.state)
     #   print(win, 'won')
     #   print('\n')
        
        list_win_2.append(win)
    
        p = x.C4State.check_win()
        
        x.reset() 
        
    prob_p1 =  cnt_1/num_games
    prob_p2 = cnt_2/num_games
    prob_tie = tie_cnt/num_games
    return  [prob_p1, prob_p2, prob_tie]



def calc_chunk_probabilities(list_win):
    num_games = len(list_win)
    p1_prob = []
    p2_prob = []
    tie_prob = []
    step_size = num_games//100
    
    for i in range(0, num_games, step_size):
        cnt_1 = 0
        cnt_2 = 0
        cnt_tie = 0
        chunk = list_win[i:i+step_size]
        for element in chunk:
            if element == 1:
                cnt_1 += 1
            if element == 2:
                cnt_2 += 1
            if element == 0:
                cnt_tie += 1
            total = step_size
        p1_prob.append(cnt_1/total)
        p2_prob.append(cnt_2/total)
        tie_prob.append(cnt_tie/total)
    return p1_prob,p2_prob,tie_prob
    



#training with random
dlist=[0.99]
qlist = [3.0] 
lrate=[0.1]
tlist = [0]
numgames = 300000

#training against another q player
#dlist = [0.99]
#qlist = [5.0]
#lrate = [0.01]
#tlist = [0]
#numgames = 300000

best_p2 = 0
best_lrate = 0
best_df = 0
best_qinit = 0
best_prob_list = [0,0,0]
qplayer_num = 1

numrows = 4
numcols = 4
numgames_test = 5000
player_3 = randomplayer(3 - qplayer_num)
for th in tlist:
    for qinit in qlist:
        for dfactor in dlist:
            for element in lrate:
                x,win_list = train(dfactor, element, numgames, qplayer_num, qinit, numrows, numcols, th, 'random')
                p1_prob, p2_prob, tie_prob = calc_chunk_probabilities(win_list)
                game_values = list(range(0,100))
                m = numgames//100
                game_values = [element*m for element in game_values]
                print('LENGTH game value', len(game_values))
                plt.plot(game_values, p1_prob)
                plt.plot(game_values,p2_prob)
                plt.plot(game_values, tie_prob)
                plt.xlabel('Number of Games')
                plt.ylabel('Probabilities')
                plt.title('Probabilities During Training Against Random Player')
                plt.legend(['player 1: AI player', 'player 2: Random player', 'tie'])
                plt.grid()
                plt.show()
                player1 = x[0]
                player2 = x[1]
                if qplayer_num == 1:
                    player2 = player_3
                else:
                    player1 = player_3
                print('TESTING -------------------------')
                prob_list = test(player1, player2, numgames_test, numrows, numcols) 
                qscore = prob_list[qplayer_num - 1]
                if(qscore > best_p2):
                    best_lrate = element
                    best_p2 = qscore 
                    best_prob_list = prob_list
                    best_df = dfactor
                    best_qinit = qinit
                    best_th = th
                print('Random player: qinit:', qinit, '| dfactor:', dfactor, '| lrate:', element, '| t:', th, '| list of probabilities:', prob_list)
                # These are deterministic games, not much to test
                depth_list = [1,6,11]
                for depth in depth_list:
                    if qplayer_num == 1:
                        player2 = minmaxplayer(3-qplayer_num,depth)
                    else:
                        player1 = minmaxplayer(3-qplayer_num,depth)
                    
                    prob_list = test(player1, player2,2, numrows, numcols) #
                    print('Depth',depth)
                    print('Minmax player:qinit:', qinit, '| dfactor:', dfactor, '| lrate:', element, '| t:', th, '| list of probabilities:', prob_list)

                
            
print('best lrate', best_lrate)
print('prob player 1 wins', best_prob_list[0])
print('prob player 2 wins', best_prob_list[1])
print('prob tie', best_prob_list[2])
print('best dfactor', best_df)
print('best_qinit', best_qinit)

    
if qplayer_num == 1:
    player_to_save = player1
else:
    player_to_save = player2
    
#file_name = 'qplayer_' + str(qplayer_num) +'.pkl'
#file_obj = open(file_name,'wb')
#pickle.dump(player_to_save, file_obj)

