'''
Created on Nov 6, 2016

@author: bashar.alhafni
'''
from tkinter import *
import tkinter
import random

class mine_sweeper:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.resizable(width=False, height=False)
        self.window.title('Mine Sweeper!')
        self.upper_frame = tkinter.Frame(self.window)
        self.upper_frame.pack(side = tkinter.TOP)        
        self.start_game_img = PhotoImage(file="c:\\temp\\new_game_button.png")
        self.end_game_image = PhotoImage(file ="c:\\temp\\lost.png")
        self.win_game_image = PhotoImage(file = "c:\\temp\\won.png")
        self.plain_img = PhotoImage(file="c:\\temp\\plain.gif")
        self.mine_image = PhotoImage(file="c:\\temp\\mine.png")
        self.red_mine_image = PhotoImage(file ="c:\\temp\\mine_source.png")
        self.flag_image = PhotoImage(file = "c:\\temp\\flag.png")
        self.clicked_image = PhotoImage(file = "c:\\temp\\tile_clicked.gif")
        self.gamebtn = Button(image = self.start_game_img)
        self.gamebtn.configure(command = self.start_game)      
        self.gamebtn.pack()
        self.lower_frame = tkinter.Frame(self.window)
        self.lower_frame.pack(side = tkinter.BOTTOM)
        self.game_over = False
        self.count = 0
        self.start_game()
        self.window.mainloop()
    
    
    def start_game(self):
        self.count = 0
        '''creates a 2D list of btn_info and set the btns to be in a grid. Also it binds all the btns to the flag_it even'''
        self.game_over = False
        self.btns = [[0 for x in range(9)] for x in range(9)]
        txt = ""
        self.gamebtn.configure(image = self.start_game_img)
        for i in range (9):
            for j in range (9):
                self.btns[i][j] = btn_info(self.lower_frame, text = txt, command = lambda row=i, column=j: self.open_cell(row, column))
                self.btns[i][j].configure(image = self.plain_img)
                self.btns[i][j].grid(row = i, column = j)
                self.btns[i][j].is_flagged = False
                self.btns[i][j].bind('<Button-3>', self.flag_it)
                

        
        self.randomize()
        
        self.get_neighbors()
        
        self.win_game()
    
    
        
    def open_cell(self,row,col):
        
        '''Checks if the btns are mines, neighbors or neither recursively'''
        
        if not self.game_over:
            
                
            if self.btns[row][col].is_mine == True and not self.btns[row][col].is_clicked and not self.btns[row][col].is_flagged:
                self.set_mines_imgs()
                self.btns[row][col].configure(image = self.red_mine_image)
                self.game_over = True
                self.lose_game()
                return
                
            if self.btns[row][col].is_neighbor and not self.btns[row][col].is_flagged:
                self.btns[row][col].configure(image = self.btns[row][col].btnImage)
                self.change_state(row, col)
                self.btns[row][col].is_clicked = True
                self.count += 1
            if self.btns[row][col].is_mine == False and self.btns[row][col].is_neighbor == False and not self.btns[row][col].is_flagged:
                self.btns[row][col].configure(image = self.clicked_image)
                self.change_state(row, col)
                self.btns[row][col].is_clicked = True
                self.count +=1
                if row + 1 < 9 :
                    if(not self.btns[row+1][col].is_clicked and not self.btns[row+1][col].is_mine):
                       
                        self.open_cell(row + 1, col)
                if col + 1 < 9 :
                    if(not self.btns[row][col+1].is_clicked and not self.btns[row][col+1].is_mine):
                        
                        self.open_cell(row, col + 1)
                if row - 1 >=0 :
                    if(not self.btns[row-1][col].is_clicked and not self.btns[row-1][col].is_mine):
                        
                        self.open_cell(row - 1, col)
                if col - 1 >=0 :
                    if(not self.btns[row][col-1].is_clicked and not self.btns[row][col-1].is_mine):
                       
                        self.open_cell(row, col - 1)
                if row + 1 < 9 and col + 1 < 9:
                    if(not self.btns[row+1][col+1].is_clicked and not self.btns[row+1][col+1].is_mine):
                        
                        self.open_cell(row+1, col+1)
                if row + 1 <9 and col - 1 >=0 :
                    if(not self.btns[row+1][col-1].is_clicked and not self.btns[row+1][col-1].is_mine):
                        
                        self.open_cell(row+1, col - 1)
                if row - 1 >=0 and col - 1 >=0 :
                    if(not self.btns[row-1][col-1].is_clicked and not self.btns[row-1][col-1].is_mine):
                        self.open_cell(row - 1, col -1)
                if row - 1 >=0 and col + 1 <9:
                    if(not self.btns[row-1][col+1].is_clicked and not self.btns[row-1][col+1].is_mine):
                        self.open_cell(row -1 , col + 1)       
    
            self.win_game()
            
    def randomize(self):
        '''it picks the mines randomly from the list'''
        for i in range(10):
            row = random.randrange(0,9)
            col = random.randrange(0,9)
            if self.btns[row][col].is_mine == True:
                row = random.randrange(0,9)
                col = random.randrange(0,9)
                self.btns[row][col].is_mine =True
            else:
                self.btns[row][col].is_mine = True
    
  
    def set_mines_imgs(self):       
        '''set the images of the mines one the mines get clicked'''
        for i in range (9):
            for j in range (9):
                if self.btns[i][j].is_mine == True:
                    self.btns[i][j].configure(image = self.mine_image)
                    self.btns[i][j].is_clicked = True
                    self.change_state(i, j)
                    
                    
                    
    def change_state(self,row,column):
        '''unbinds the btn from the flag_it function and make it sunken'''
        (self.btns[row][column]).unbind('<Button-3>')
        (self.btns[row][column])["relief"] = tkinter.SUNKEN
        
    
    
    
    
    def get_neighbors(self):
        '''getting the neighbors of a mine'''
        for i in range (9):
            for j in range (9):
                if self.btns[i][j].is_mine == True:
                    if ( (i + 1) < 9): #down
                        if not self.btns[i+1][j].is_mine: 
                            self.mine_num(self.btns[i+1][j])
                            self.btns[i+1][j].is_neighbor = True
                            
                    if( (j + 1) < 9):#right
                        if not self.btns[i][j+1].is_mine:
                            self.mine_num(self.btns[i][j+1])
                            self.btns[i][j+1].is_neighbor = True
                        
                    if((i-1) >= 0):#up
                        if not self.btns[i-1][j].is_mine:
                            self.mine_num(self.btns[i-1][j])
                            self.btns[i-1][j].is_neighbor = True
                        
                    if((j-1) >= 0):#left
                        if not self.btns[i][j-1].is_mine:
                            self.mine_num(self.btns[i][j-1])
                            self.btns[i][j-1].is_neighbor = True
                        
                    if  i+1 <9 and j+1 < 9:#down-right diagonal
                        if not self.btns[i+1][j+1].is_mine:
                            self.mine_num(self.btns[i+1][j+1])
                            self.btns[i+1][j+1].is_neighbor = True
            
                    if  i+1 <9 and j-1 >= 0:#down-left Diagonal
                        if not self.btns[i+1][j-1].is_mine:
                            self.mine_num(self.btns[i+1][j-1])
                            self.btns[i+1][j-1].is_neighbor = True
                      
                    if i - 1 >= 0 and j - 1 >= 0: #up-left Diagonal
                        if not self.btns[i-1][j-1].is_mine:
                            self.mine_num(self.btns[i-1][j-1])
                            self.btns[i-1][j-1].is_neighbor = True
                        
                        
                    if i -1 >= 0 and j + 1 < 9 :#up-right Diagonal
                        if not self.btns[i-1][j+1].is_mine:
                            self.mine_num(self.btns[i-1][j+1])
                            self.btns[i-1][j+1].is_neighbor = True
                        
                        
    def mine_num(self,btn):
        '''setting the tiles to the correct images'''
        if btn.tile_num == '':
            btn.tile_num = 'c:\\temp\\tile_1.gif'
            
        elif btn.tile_num == 'c:\\temp\\tile_1.gif':
            btn.tile_num = 'c:\\temp\\tile_2.gif'
            
        elif btn.tile_num == 'c:\\temp\\tile_2.gif':
            btn.tile_num = 'c:\\temp\\tile_3.gif'
            
        elif btn.tile_num == 'c:\\temp\\tile_3.gif':
            btn.tile_num = 'c:\\temp\\tile_4.gif'
            
        elif btn == 'c:\\temp\\tile_4.gif':
            btn.tile_num = 'c:\\temp\\tile_5.gif'
            
        elif btn == 'c:\\temp\\tile_5.gif':
            btn.tile_num = 'c:\\temp\\tile_6.gif'
            
        elif btn.tile_num == 'c:\\temp\\tile_6.gif':
            btn.tile_num = 'c:\\temp\\tile_7.gif'
            
        elif btn.tile_num == 'c:\\temp\\tile_7.gif':
            btn.tile_num = 'c:\\temp\\tile_8.gif'
            
        btn.btnImage = PhotoImage(file = btn.tile_num)
        
    
    def flag_it(self,event):
        '''changes the button image to a flag'''
        if not self.game_over:
            (event.widget).configure(image = self.flag_image)
            (event.widget)["relief"] = tkinter.SUNKEN
            if (event.widget).is_flagged == True:
                (event.widget).is_clicked = False
                (event.widget).is_flagged = False
                (event.widget).configure(image = self.plain_img)
                (event.widget)["relief"] = tkinter.RAISED
                return
            (event.widget).is_flagged = True
            #(event.widget).is_clicked = True
            self.win_game()
            
        
    
    def win_game(self):
        '''checks if the user wins the game'''
        
        for row in range(9):
            for col in range(9):
                        if self.count == 71:
                            self.game_over= True
                            self.gamebtn.configure(image = self.win_game_image)
                            
                    
    def lose_game(self):
        '''check if the user loses the game'''
        self.gamebtn.configure(image = self.end_game_image)
        
class btn_info(tkinter.Button):
    '''a class that inherits the button class'''
    def __init__(self, master=None, cnf={}, **kw):
        Widget.__init__(self, master, 'button', cnf, kw)
        self.is_mine = False
        self.is_clicked = False
        self.is_neighbor = False
        self.tile_num = ''
        self.btnImage = None
        self.is_flagged = False
            

if __name__ == '__main__':
    m = mine_sweeper()
    


    