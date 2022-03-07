# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 12:14:49 2021

@author: anish
"""


class C4State(object):

    def __init__(self, numrows, numcols):

        self.numrows = numrows
        self.numcols = numcols
        self.state = {}
        for i in range(0,self.numrows):
            for j in range(0,self.numcols):
                self.state[(i,j)] = 0   
        self.player_id = 1

    def check_win(self):
        for r in range(0,self.numrows):
            for c in range(0, self.numcols - 4 +1):
                if self.state[(r,c)] == self.state[(r,c+1)] == self.state[(r,c+2)] == self.state[(r,c+3)]:
                    if self.state[(r,c)] > 0:
                        num = self.state[(r,c)]
                        return num
        
        for c in range (0,self.numcols):
           for r in range(0,self.numrows - 4+1):
               if self.state[(r,c)] == self.state[(r+1,c)] == self.state[(r+2,c)] == self.state[(r+3,c)]:
                   if self.state[(r,c)] > 0:
                       num = self.state[(r,c)]
                       return num
                   
        for r in range(0,self.numrows -4+1):
            for c in range(0, self.numcols - 4 +1):
                
                if self.state[(r,c)] == self.state[(r+1,c+1)] == self.state[(r+2,c+2)] == self.state[(r+3,c+3)]:
                    if self.state[(r,c)] > 0:
                        num = self.state[(r,c)]
                        return num  
                    
                if self.state[(r,c+3)] == self.state[(r+1,c+2)] == self.state[(r+2,c+1)] == self.state[(r+3,c)]:
                    if self.state[(r,c+3)] > 0:
                        num = self.state[(r,c+3)]
                        return num
        
        return 0
    
    def check_draw(self):
        for element in self.state.values():
            if(element==0):
                return False
        return True
            
        
    def update_turn(self):
        if(self.player_id==1):
            self.player_id=2
        else:
            self.player_id=1
           
            
    def update_state(self, row, column):
        
         
         if(self.player_id == 1 and self.state[row,column] == 0):
                 self.state[(row,column)] = 1
                 return True
                 
         elif(self.player_id == 2 and self.state[row,column] == 0):
                self.state[(row,column)] = 2
                return True
         else:
            return False
        
    def reset(self):
        self.player_id = 1

        for i in range(0,self.numrows): 
            for j in range(0,self.numcols): 
                self.state[(i,j)] = 0 
                
    def print_state(self, state):
        print_str = ''
        for i in range(0,self.numrows):
            for j in range(0,self.numcols):
                if(state[(i,j)] == 0):
                    char_to_print = '-'
                if(state[(i,j)] == 1):
                    char_to_print = 'X'
                if(state[(i,j)] == 2):
                    char_to_print = 'O'
                print_str = print_str + char_to_print
            print_str = print_str + '\n'
        print(print_str)
                
    
    def get_valid_moves(self, state):
        
        valid_moves = []
        for j in range(self.numcols):
            for i in range(self.numrows):
                if self.state[(i,j)] != 0:
                    if i != 0:
                        valid_moves.append((i-1,j))
                    break
                elif i == self.numrows - 1 and self.state[(i,j)] == 0:
                    valid_moves.append((self.numrows-1, j))
        return valid_moves
        
    def state_to_number(self, state):
        num= 0
        cnt = 0
        for i in range(0,self.numrows):
            for j in range(0,self.numcols):
                num = num + (3**cnt)*state[(i,j)]
                cnt+=1
        return num    
    
    def number_to_state(self, num):
        state = {}
        for i in range(0,self.numrows):
            for j in range(0,self.numcols):
                state[(i,j)] = 0
        
        divisor = 3**(self.numrows*self.numcols - 1)
        for i in range(self.numrows-1,-1,-1):
            for j in range(self.numcols - 1,-1,-1):
                quotient = num//divisor
                state[(i,j)] = quotient
                num = num%divisor
                divisor = divisor/3
        return state
        
        