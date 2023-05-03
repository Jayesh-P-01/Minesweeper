from guizero import *
import random
app = App()
top_cont = Box(app, layout = 'grid') # this will contain all of the things that are 
#not part of the game, such as the timer, and the bomb counter
game_cont = Box(app, layout = 'grid') # this will store the acctual game, so this is 
#where the grid will go

def select_level():
    selected_difficulty = select_diff.value
    start.destroy()
    select_diff.destroy()
    instructions.destroy()
    challenge.destroy()
    if selected_difficulty == 'Easy':
        game = Easy_Game()
        game.set_up_grid()
    elif selected_difficulty == 'Medium':
        game = Med_Game()
        game.set_up_grid()
    elif selected_difficulty == 'Hard':
        game = Hard_Game()
        game.set_up_grid()

start = PushButton(top_cont, text = 'start', grid = [0,0], command = select_level)
select_diff = ButtonGroup(top_cont, options= ['Easy','Medium','Hard'], selected= 'Easy', grid = [0,1])
instructions = Text(top_cont, text = 'When you press start, a grid will appear. To place a flag, right click. To reveal a square, left click.', grid = [0,2])
challenge = Text(top_cont, text = "Do you think you have what it takes to navigate a minefield and detect all of the bombs laid down by enemy forces. Well let's find out!", grid = [0,3])


class Hard_Game:
    def __init__(self):
        pass

    def set_up_grid(self):
        self.squares_remaining = 324
        self.click_count = 0 # this will be used to determine when the game is started, when this goes up to one, the game will know that this is the first click
        self.button_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this will store all of the buttons in a list, so that it can easily be accessed, so that you can change the picture easily
        self.bomb_count = 40
        self.time = 0 # this will increase, and this will be used for the timer
        self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0]) # this will be changed as the game progresses, but this is currently a lable telling the user how many flags they have left to place
        self.time_lable = Text(top_cont, text = 'Time Elapsed: '+str(self.time), grid = [1,0]) # this tells the user how much time has elepsed
        self.time_lable.repeat(1000, self.increase_time) # this means that each second, self.increase_time will be called
        for i in range(0,18):
            for j in range(0,18):
                coords = str(str(i)+','+str(j)) # this will be assigned to the text, and it goes x,y but the lists work y,x
                #of the button, which can then be accessed later, which will be useful
                exec("button{}{} = PushButton(game_cont, grid = [{},{}], width = 25, height = 25, image = 'lightgrey.png', text = coords)".format(str(i), str(j), i,j))
                exec('button{}{}.when_right_button_pressed = self.place_flag'.format(str(i), str(j)))
                exec('button{}{}.when_left_button_pressed = self.left_clicked'.format(str(i), str(j)))
                exec('self.button_list[{}].append(button{}{})'.format(str(j),str(i),str(j)))

    def increase_time(self): # this controls the timer
        self.time += 1
        self.time_lable = Text(top_cont, text = 'Time Elapsed: '+str(self.time), grid = [1,0])

    def place_flag(self,event_data):
        self.to_split = (event_data.widget.text)
        self.split = self.to_split.split(',')
        self.button_x = self.split[0] # this will store the x coordinate of the button that has been pressed
        self.button_y = self.split[1] # this will store the y coordinate of the button that has been pressed
        if self.button_list[int(self.button_y)][int(self.button_x)].image != 'flagged2.png' and self.bomb_count > 0 and self.button_list[int(self.button_y)][int(self.button_x)].enabled == True: # the following will be executed if the current button has just the normal backgroup, and there are still flags left that can be placed
            exec("self.button_list[{}][{}].image = 'flagged2.png'".format(int(self.button_y), int(self.button_x))) # this will find the button in the list, and then change the image that it holds to a flag
            exec("self.button_list[{}][{}].enabled = False".format(int(self.button_y), int(self.button_x)))
            self.bomb_count -= 1 # this means that they will have one less flag to place
            self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0]) # this displays how many flags there are left to place
        elif self.button_list[int(self.button_y)][int(self.button_x)].image == 'flagged2.png': # this will check if this square has already been flaged, and if it has, then the flag will be removed, and then the count of the flags left will be increased by one
            exec("self.button_list[{}][{}].image = 'lightgrey.png'".format(int(self.button_y), int(self.button_x)))
            exec("self.button_list[{}][{}].enabled = True".format(int(self.button_y), int(self.button_x)))
            self.bomb_count += 1
            self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0])

    def left_clicked(self,event_data):
        self.to_split = (event_data.widget.text)
        self.split = self.to_split.split(',')
        self.button_x = self.split[0] # this will store the x coordinate of the button that has been pressed
        self.button_y = self.split[1]
        self.click_count += 1
        if self.click_count == 1: # this means that this is the first go
            self.create_game(self.to_split) # if it is the first go, then it will create the game, and figure out where the bombs are going ot be, and bassically create the game
            self.master_first_click()
        elif self.click_count > 1:
            if self.bomb_cont[int(self.button_y)][int(self.button_x)] == '0':
                if self.bomb_touch[int(self.button_y)][int(self.button_x)] == 0:
                    self.first_square_two() # this will deal with everything that needs to be done for the first square   
                    while len(self.outside_list)>0: # this whole process will be repeated until there are no squares left on the outside list, which means that there is nothing more to be done on this first turn
                        for i in range(0,len(self.outside_list)):
                            self.opperating_list.append(self.outside_list[i]) # this means that after the first click has been done, and the surrounding squares of the first square have been collected, you can now operate on them
                        self.outside_list = [] # all of the information has been transfered out of this list, and now it means thata we can find all of the new outside squares
                        for i in range(0,len(self.opperating_list)):
                            self.other_squares(i)
                        for i in range(0,len(self.opperating_list)):
                            self.finished_list.append(self.opperating_list[i])
                    self.squares_remaining = 324 # we need to reset this so that we can now look at all of the squares that are no longer enabled and work out the new squares remaining value
                    for i in range(0,len(self.button_list)):
                        for j in range(0,len(self.button_list[i])):
                            if self.button_list[i][j].image != 'lightgrey.png' and self.button_list[i][j].image != 'flagged2.png':
                                self.squares_remaining -= 1
                elif self.bomb_touch[int(self.button_y)][int(self.button_x)] != 0:
                    self.when_not_zero_two(int(self.button_y),int(self.button_x))
            elif self.bomb_cont[int(self.button_y)][int(self.button_x)] == '1':
                self.bomb_handler()
            if self.squares_remaining <= 40:
                self.remain_ckeck()
                

    def remain_ckeck(self): # this rechecks that there are only 40 squares left, and none have been removed becaues something was clicked twice while the program was laggingr
        for i in range(0,len(self.button_list)):
            for j in range(0,len(self.button_list[i])):
                if self.button_list[i][j].enabled == False:
                    self.squares_remaining -= 1
                    if self.squares_remaining == 0:
                        self.completed_handler()
                else:
                    pass

    def master_first_click(self):
        self.outside_list = [] # this stores all of the squares that are on the outside of the map that need to be looked at
        self.opperating_list = [] # this will store all of the squares that are being worked on in a cycle of working
        self.finished_list = [] # this will store the information for all of the squares that have already been dealt with, so that we don't get an infinate loop
        self.surrounding_list = [] # this will store the surrounding squares of one square, and this will be used lots
        self.first_square() # this will deal with everything that needs to be done for the first square   
        while len(self.outside_list)>0: # this whole process will be repeated until there are no squares left on the outside list, which means that there is nothing more to be done on this first turn
            for i in range(0,len(self.outside_list)):
                self.opperating_list.append(self.outside_list[i]) # this means that after the first click has been done, and the surrounding squares of the first square have been collected, you can now operate on them
            self.outside_list = [] # all of the information has been transfered out of this list, and now it means thata we can find all of the new outside squares
            for i in range(0,len(self.opperating_list)):
                self.other_squares(i)
            for i in range(0,len(self.opperating_list)):
                self.finished_list.append(self.opperating_list[i])
        for i in range(0,len(self.button_list)):
            for j in range(0,len(self.button_list[i])):
                if self.button_list[i][j].enabled == False:
                    self.squares_remaining -= 1 # this is so that we can check how many squares are left to be clicked
                
                
    def first_square(self): # this will do everything needed for the first square
        self.surrounding_list = [[int(self.button_y)-1,int(self.button_x)-1],[int(self.button_y)-1,int(self.button_x)],[int(self.button_y)-1,int(self.button_x)+1],
        [int(self.button_y),int(self.button_x)-1],[int(self.button_y),int(self.button_x)+1],
        [int(self.button_y)+1,int(self.button_x)-1],[int(self.button_y)+1,int(self.button_x)],[int(self.button_y)+1,int(self.button_x)+1],]
        i = 0
        l = len(self.surrounding_list)
        while i < l:
            if self.surrounding_list[i][0] < 0 or self.surrounding_list[i][0] > 17 or self.surrounding_list[i][1] < 0 or self.surrounding_list[i][1] > 17:
                del self.surrounding_list[i]
                l = len(self.surrounding_list)
            else:
                i += 1
        self.button_list[int(self.button_y)][int(self.button_x)].image = '0_res.png'
        self.button_list[int(self.button_y)][int(self.button_x)].enabled = False
        for i in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[i])
        self.finished_list.append([int(self.button_y),int(self.button_x)]) # this makes the first button go into the finished list, and this means that this will not be looked at in the future   

    def other_squares(self,track): # this will be done for the other squares of the first click
        self.track = track # track will be used to know which position in self.operating_list we are looking at, and this will just be the value of i in the for loop that controls this
        self.yval = self.opperating_list[self.track][0]
        self.xval = self.opperating_list[self.track][1]
        try:
            if self.bomb_touch[self.yval][self.xval] == 0:
                self.button_list[self.yval][self.xval].image = '0_res.png'
                self.button_list[self.yval][self.xval].enabled = False
                self.when_zero() # this calls the handeler when the value of the bomb touch for that square is 0
            else: # this handles when there is a bomb that this square is touching 
                self.when_not_zero()
        except:
            pass

    def when_zero(self): # this will handle if the value of the square on the bomb touch list is zero
        self.surrounding_list = [[self.yval-1,self.xval-1],[self.yval-1,self.xval],[self.yval-1,self.xval+1],
        [self.yval,self.xval-1],[self.yval,self.xval+1],
        [self.yval+1,self.xval-1],[self.yval+1,self.xval],[self.yval+1,self.xval+1]]
        x = 0
        l = len(self.surrounding_list)
        while x < l: # this one removes any squares that are not in the grid
            if self.surrounding_list[x][0] < 0 or self.surrounding_list[x][0] > 17 or self.surrounding_list[x][1] < 0 or self.surrounding_list[x][1] > 17:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        x = 0
        l = len(self.surrounding_list)
        while x<l: # this will remove all of the elements that are in another list
            if self.surrounding_list[x] in self.outside_list or self.surrounding_list[x] in self.opperating_list or self.surrounding_list[x] in self.finished_list:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        for a in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[a])
        
    def when_not_zero(self):
        if self.bomb_touch[self.yval][self.xval] == 1:
            self.button_list[self.yval][self.xval].image = '1_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 2:
            self.button_list[self.yval][self.xval].image = '2_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 3:
            self.button_list[self.yval][self.xval].image = '3_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 4:
            self.button_list[self.yval][self.xval].image = '4_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 5:
            self.button_list[self.yval][self.xval].image = '5_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 6:
            self.button_list[self.yval][self.xval].image = '6_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 7:
            self.button_list[self.yval][self.xval].image = '7_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 8:
            self.button_list[self.yval][self.xval].image = '8_res.png'
        self.button_list[self.yval][self.xval].enabled = False

    def when_not_zero_two(self,button_y,button_x):
        self.button_y = button_y
        self.button_x = button_x
        if self.bomb_touch[self.button_y][self.button_x] == 1:
            self.button_list[self.button_y][self.button_x].image = '1_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 2:
            self.button_list[self.button_y][self.button_x].image = '2_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 3:
            self.button_list[self.button_y][self.button_x].image = '3_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 4:
            self.button_list[self.button_y][self.button_x].image = '4_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 5:
            self.button_list[self.button_y][self.button_x].image = '5_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 6:
            self.button_list[self.button_y][self.button_x].image = '6_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 7:
            self.button_list[self.button_y][self.button_x].image = '7_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 8:
            self.button_list[self.button_y][self.button_x].image = '8_res.png'
        self.button_list[self.button_y][self.button_x].enabled = False
        self.squares_remaining -= 1

    def first_square_two(self):
        self.surrounding_list = [[int(self.button_y)-1,int(self.button_x)-1],[int(self.button_y)-1,int(self.button_x)],[int(self.button_y)-1,int(self.button_x)+1],
        [int(self.button_y),int(self.button_x)-1],[int(self.button_y),int(self.button_x)+1],
        [int(self.button_y)+1,int(self.button_x)-1],[int(self.button_y)+1,int(self.button_x)],[int(self.button_y)+1,int(self.button_x)+1],]
        i = 0
        l = len(self.surrounding_list)
        while i < l:
            if self.surrounding_list[i][0] < 0 or self.surrounding_list[i][0] > 17 or self.surrounding_list[i][1] < 0 or self.surrounding_list[i][1] > 17:
                del self.surrounding_list[i]
                l = len(self.surrounding_list)
            else:
                i += 1
        
        x = 0
        l = len(self.surrounding_list)
        while x<l: # this will remove all of the elements that are in another list
            if self.surrounding_list[x] in self.outside_list or self.surrounding_list[x] in self.opperating_list or self.surrounding_list[x] in self.finished_list:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        self.button_list[int(self.button_y)][int(self.button_x)].image = '0_res.png'
        self.button_list[int(self.button_y)][int(self.button_x)].enabled = False
        for i in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[i])
        self.finished_list.append([int(self.button_y),int(self.button_x)])

    def bomb_handler(self):
        app.info('Bomb', 'you have hit a mine, you lose :(')
        app.destroy()
    
    def completed_handler(self):
        app.info('You win!', 'Congratulations, you have completed the game in ' +str(self.time)+ ' seconds!')
        app.destroy()

    def create_game(self,event_data): # this will look at the square that the user clicked on, and then randomly generate where the bombs will be placed
       
        #the following is code that will choose where the bombs are going down, in response to the first click
        self.split = self.to_split.split(',')
        self.button_x = self.split[0]
        self.button_y = self.split[1] 
        self.bomb_cont = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this is a list that will store where the bombs are located
        for i in range(0,18): # everything in this for loop will create a blank template list, and this will be for storing the information about where the bombs are located
            for i in range(0,18):
                self.bomb_cont[i].append('0') # all of the sqaures that have a 0 are squares with no bombs on them, and squares with a 1 will be ones with bombs on them. The initial square that is clicked on will be an 'S', meaning Safe, and this is because the user cannot lose on their first go, which means that a bomb cannot be placed there
        self.bomb_cont[int(self.button_y)][int(self.button_x)] = 'S' # this means that this square can never have a bomb on it for the rest of the game
        try: # all of the following try except statements find the surrounding squares for the square that has just been clicked, and then put an 'S' on it, so taht there cannot be a bomb placed there, because otherwise you could get stuck right at the beggining of the game, which would not be ideal
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)+1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)][int(self.button_x)+1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)+1] = 'S'
        except:
            pass
        i = 0
        while i < 40:
            randomx = random.randint(0,17)
            randomy = random.randint(0,17) # this and randomx will be used to determine where the next bomb is going to go
            if self.bomb_cont[randomy][randomx] == '0':
                self.bomb_cont[randomy][randomx] = '1'
                i += 1
            elif self.bomb_cont[randomy][randomx] == '1' or self.bomb_cont[randomy][randomx] == 'S':
                pass
        store = 0
        for i in range(0,18):
            for j in range(0,18):
                if self.bomb_cont[i][j] == '1':
                    store += 1
        if store == 39: # there is a chance that there will end up being only 39 bombs, a small chance, but it could happen
            while i == 0:
                randomx = random.randint(0,17)
                randomy = random.randint(0,17)
                if self.bomb_cont[randomy][randomx] == '0':
                    self.bomb_cont[randomy][randomx] = '1'
                    i += 1
                elif self.bomb_cont[randomy][randomx] == '1' or self.bomb_cont[randomy][randomx] == 'S':
                    pass
        self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0])
        
        #the following code will come up with a list that will contain the number of bombs that each square is touching
        self.bomb_touch = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this is the containor, and when there is a number in a position, it means that there are that many bombs touching that square
        for i in range(0,18): # the following will just put positions in the list so that they can be edited later 
            for j in range(0,18):
                self.bomb_touch[i].append(0) # now every position is filled with 0, which means it can now be editied
        
        for i in range(1,17): # this creates all of the information on how many bombs are touching all of the squares that are not on the edges
            for j in range(1,17):
                self.analyse_center(j,i)
        
        for i in range(1,17): # this makes all of the boxes on the top line contain the numeber of bombs that that one is touching
            self.analyse_top_line(i)

        for i in range(1,17):
            self.analyse_bottom_line(i)

        for i in range(1,17):
            self.analyse_left(i)
        
        for i in range(1,17):
            self.analyse_right(i)

        self.left_corner()
        self.right_corner()
        self.btm_left()
        self.btm_right()

    def analyse_center(self,xval,yval):
        self.xval = xval
        self.yval = yval
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval-1][self.xval-1],self.bomb_cont[self.yval-1][self.xval],
            self.bomb_cont[self.yval-1][self.xval+1],self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval][self.xval+1],
            self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval],self.bomb_cont[self.yval+1][self.xval+1],]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count
        
    def analyse_top_line(self,xval):
        self.xval = xval
        self.yval = 0
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[0][self.xval-1],self.bomb_cont[0][self.xval+1],
            self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval],
            self.bomb_cont[self.yval+1][self.xval+1]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def analyse_bottom_line(self, xval):
        self.xval = xval
        self.yval = 17
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval][self.xval+1],
            self.bomb_cont[self.yval-1][self.xval-1],self.bomb_cont[self.yval-1][self.xval],
            self.bomb_cont[self.yval-1][self.xval+1]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def analyse_left(self,yval):
        self.yval = yval
        self.xval = 0
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval+1][0],self.bomb_cont[self.yval+1][1],self.bomb_cont[self.yval][1],
            self.bomb_cont[self.yval-1][1],self.bomb_cont[self.yval-1][0]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count
        
    def analyse_right(self,yval):
        self.yval = yval
        self.xval = 17
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval-1][self.xval],self.bomb_cont[self.yval-1][self.xval-1],
            self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def left_corner(self):
        if self.bomb_cont[0][0] == '1':
            self.bomb_touch[0][0] = 9
        else:
            self.touching_list = [self.bomb_cont[0][1],self.bomb_cont[1][1],self.bomb_cont[1][0]]
            count = self.touching_list.count('1')
            self.bomb_touch[0][0] = count
    
    def right_corner(self):
        if self.bomb_cont[0][17] == '1':
            self.bomb_touch[0][17] = 9
        else:
            self.touching_list = [self.bomb_cont[0][16],self.bomb_cont[1][16],self.bomb_cont[1],[17]]
            count = self.touching_list.count('1')
            self.bomb_touch[0][17] = count
    
    def btm_left(self):
        if self.bomb_cont[17][0] == '1':
            self.bomb_touch[17][0] = 9
        else:
            self.touching_list = [self.bomb_cont[16][0],self.bomb_cont[16][1],self.bomb_cont[17][1]]
            count = self.touching_list.count('1')
            self.bomb_touch[17][0] = count

    def btm_right(self):
        if self.bomb_cont[17][17] == '1':
            self.bomb_touch[17][17] = 9
        else:
            self.touching_list = [self.bomb_cont[16][17],self.bomb_cont[16][16],self.bomb_cont[17],[16]]
            count = self.touching_list.count('1')
            self.bomb_touch[17][17] = count
    
class Med_Game:
    def __init__(self):
        pass

    def set_up_grid(self):
        self.squares_remaining = 225
        self.click_count = 0 # this will be used to determine when the game is started, when this goes up to one, the game will know that this is the first click
        self.button_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this will store all of the buttons in a list, so that it can easily be accessed, so that you can change the picture easily
        self.bomb_count = 25
        self.time = 0 # this will increase, and this will be used for the timer
        self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0]) # this will be changed as the game progresses, but this is currently a lable telling the user how many flags they have left to place
        self.time_lable = Text(top_cont, text = 'Time Elapsed: '+str(self.time), grid = [1,0]) # this tells the user how much time has elepsed
        self.time_lable.repeat(1000, self.increase_time) # this means that each second, self.increase_time will be called
        for i in range(0,15):
            for j in range(0,15):
                coords = str(str(i)+','+str(j)) # this will be assigned to the text, and it goes x,y but the lists work y,x
                #of the button, which can then be accessed later, which will be useful
                exec("button{}{} = PushButton(game_cont, grid = [{},{}], width = 25, height = 25, image = 'lightgrey.png', text = coords)".format(str(i), str(j), i,j))
                exec('button{}{}.when_right_button_pressed = self.place_flag'.format(str(i), str(j)))
                exec('button{}{}.when_left_button_pressed = self.left_clicked'.format(str(i), str(j)))
                exec('self.button_list[{}].append(button{}{})'.format(str(j),str(i),str(j)))

    def increase_time(self): # this controls the timer
        self.time += 1
        self.time_lable = Text(top_cont, text = 'Time Elapsed: '+str(self.time), grid = [1,0])

    def place_flag(self,event_data):
        self.to_split = (event_data.widget.text)
        self.split = self.to_split.split(',')
        self.button_x = self.split[0] # this will store the x coordinate of the button that has been pressed
        self.button_y = self.split[1] # this will store the y coordinate of the button that has been pressed
        if self.button_list[int(self.button_y)][int(self.button_x)].image != 'flagged2.png' and self.bomb_count > 0 and self.button_list[int(self.button_y)][int(self.button_x)].enabled == True: # the following will be executed if the current button has just the normal backgroup, and there are still flags left that can be placed
            exec("self.button_list[{}][{}].image = 'flagged2.png'".format(int(self.button_y), int(self.button_x))) # this will find the button in the list, and then change the image that it holds to a flag
            exec("self.button_list[{}][{}].enabled = False".format(int(self.button_y), int(self.button_x)))
            self.bomb_count -= 1 # this means that they will have one less flag to place
            self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0]) # this displays how many flags there are left to place
        elif self.button_list[int(self.button_y)][int(self.button_x)].image == 'flagged2.png': # this will check if this square has already been flaged, and if it has, then the flag will be removed, and then the count of the flags left will be increased by one
            exec("self.button_list[{}][{}].image = 'lightgrey.png'".format(int(self.button_y), int(self.button_x)))
            exec("self.button_list[{}][{}].enabled = True".format(int(self.button_y), int(self.button_x)))
            self.bomb_count += 1
            self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0])

    def left_clicked(self,event_data):
        self.to_split = (event_data.widget.text)
        self.split = self.to_split.split(',')
        self.button_x = self.split[0] # this will store the x coordinate of the button that has been pressed
        self.button_y = self.split[1]
        self.click_count += 1
        if self.click_count == 1: # this means that this is the first go
            self.create_game(self.to_split) # if it is the first go, then it will create the game, and figure out where the bombs are going ot be, and bassically create the game
            self.master_first_click()
        elif self.click_count > 1:
            if self.bomb_cont[int(self.button_y)][int(self.button_x)] == '0':
                if self.bomb_touch[int(self.button_y)][int(self.button_x)] == 0:
                    self.first_square_two() # this will deal with everything that needs to be done for the first square   
                    while len(self.outside_list)>0: # this whole process will be repeated until there are no squares left on the outside list, which means that there is nothing more to be done on this first turn
                        for i in range(0,len(self.outside_list)):
                            self.opperating_list.append(self.outside_list[i]) # this means that after the first click has been done, and the surrounding squares of the first square have been collected, you can now operate on them
                        self.outside_list = [] # all of the information has been transfered out of this list, and now it means thata we can find all of the new outside squares
                        for i in range(0,len(self.opperating_list)):
                            self.other_squares(i)
                        for i in range(0,len(self.opperating_list)):
                            self.finished_list.append(self.opperating_list[i])
                    self.squares_remaining = 225 # we need to reset this so that we can now look at all of the squares that are no longer enabled and work out the new squares remaining value
                    for i in range(0,len(self.button_list)):
                        for j in range(0,len(self.button_list[i])):
                            if self.button_list[i][j].image != 'lightgrey.png' and self.button_list[i][j].image != 'flagged2.png':
                                self.squares_remaining -= 1
                elif self.bomb_touch[int(self.button_y)][int(self.button_x)] != 0:
                    self.when_not_zero_two(int(self.button_y),int(self.button_x))
            elif self.bomb_cont[int(self.button_y)][int(self.button_x)] == '1':
                self.bomb_handler()
            if self.squares_remaining <= 25:
                self.remain_ckeck()
                

    def remain_ckeck(self): # this rechecks that there are only 40 squares left, and none have been removed becaues something was clicked twice while the program was laggingr
        for i in range(0,len(self.button_list)):
            for j in range(0,len(self.button_list[i])):
                if self.button_list[i][j].enabled == False:
                    self.squares_remaining -= 1
                    if self.squares_remaining == 0:
                        self.completed_handler()
                else:
                    pass

    def master_first_click(self):
        self.outside_list = [] # this stores all of the squares that are on the outside of the map that need to be looked at
        self.opperating_list = [] # this will store all of the squares that are being worked on in a cycle of working
        self.finished_list = [] # this will store the information for all of the squares that have already been dealt with, so that we don't get an infinate loop
        self.surrounding_list = [] # this will store the surrounding squares of one square, and this will be used lots
        self.first_square() # this will deal with everything that needs to be done for the first square   
        while len(self.outside_list)>0: # this whole process will be repeated until there are no squares left on the outside list, which means that there is nothing more to be done on this first turn
            for i in range(0,len(self.outside_list)):
                self.opperating_list.append(self.outside_list[i]) # this means that after the first click has been done, and the surrounding squares of the first square have been collected, you can now operate on them
            self.outside_list = [] # all of the information has been transfered out of this list, and now it means thata we can find all of the new outside squares
            for i in range(0,len(self.opperating_list)):
                self.other_squares(i)
            for i in range(0,len(self.opperating_list)):
                self.finished_list.append(self.opperating_list[i])
        for i in range(0,len(self.button_list)):
            for j in range(0,len(self.button_list[i])):
                if self.button_list[i][j].enabled == False:
                    self.squares_remaining -= 1 # this is so that we can check how many squares are left to be clicked
                
                
    def first_square(self): # this will do everything needed for the first square
        self.surrounding_list = [[int(self.button_y)-1,int(self.button_x)-1],[int(self.button_y)-1,int(self.button_x)],[int(self.button_y)-1,int(self.button_x)+1],
        [int(self.button_y),int(self.button_x)-1],[int(self.button_y),int(self.button_x)+1],
        [int(self.button_y)+1,int(self.button_x)-1],[int(self.button_y)+1,int(self.button_x)],[int(self.button_y)+1,int(self.button_x)+1],]
        i = 0
        l = len(self.surrounding_list)
        while i < l:
            if self.surrounding_list[i][0] < 0 or self.surrounding_list[i][0] > 17 or self.surrounding_list[i][1] < 0 or self.surrounding_list[i][1] > 17:
                del self.surrounding_list[i]
                l = len(self.surrounding_list)
            else:
                i += 1
        self.button_list[int(self.button_y)][int(self.button_x)].image = '0_res.png'
        self.button_list[int(self.button_y)][int(self.button_x)].enabled = False
        for i in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[i])
        self.finished_list.append([int(self.button_y),int(self.button_x)]) # this makes the first button go into the finished list, and this means that this will not be looked at in the future   

    def other_squares(self,track): # this will be done for the other squares of the first click
        self.track = track # track will be used to know which position in self.operating_list we are looking at, and this will just be the value of i in the for loop that controls this
        self.yval = self.opperating_list[self.track][0]
        self.xval = self.opperating_list[self.track][1]
        try:
            if self.bomb_touch[self.yval][self.xval] == 0:
                self.button_list[self.yval][self.xval].image = '0_res.png'
                self.button_list[self.yval][self.xval].enabled = False
                self.when_zero() # this calls the handeler when the value of the bomb touch for that square is 0
            else: # this handles when there is a bomb that this square is touching 
                self.when_not_zero()
        except:
            pass

    def when_zero(self): # this will handle if the value of the square on the bomb touch list is zero
        self.surrounding_list = [[self.yval-1,self.xval-1],[self.yval-1,self.xval],[self.yval-1,self.xval+1],
        [self.yval,self.xval-1],[self.yval,self.xval+1],
        [self.yval+1,self.xval-1],[self.yval+1,self.xval],[self.yval+1,self.xval+1]]
        x = 0
        l = len(self.surrounding_list)
        while x < l: # this one removes any squares that are not in the grid
            if self.surrounding_list[x][0] < 0 or self.surrounding_list[x][0] > 17 or self.surrounding_list[x][1] < 0 or self.surrounding_list[x][1] > 17:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        x = 0
        l = len(self.surrounding_list)
        while x<l: # this will remove all of the elements that are in another list
            if self.surrounding_list[x] in self.outside_list or self.surrounding_list[x] in self.opperating_list or self.surrounding_list[x] in self.finished_list:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        for a in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[a])
        
    def when_not_zero(self):
        if self.bomb_touch[self.yval][self.xval] == 1:
            self.button_list[self.yval][self.xval].image = '1_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 2:
            self.button_list[self.yval][self.xval].image = '2_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 3:
            self.button_list[self.yval][self.xval].image = '3_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 4:
            self.button_list[self.yval][self.xval].image = '4_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 5:
            self.button_list[self.yval][self.xval].image = '5_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 6:
            self.button_list[self.yval][self.xval].image = '6_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 7:
            self.button_list[self.yval][self.xval].image = '7_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 8:
            self.button_list[self.yval][self.xval].image = '8_res.png'
        self.button_list[self.yval][self.xval].enabled = False

    def when_not_zero_two(self,button_y,button_x):
        self.button_y = button_y
        self.button_x = button_x
        if self.bomb_touch[self.button_y][self.button_x] == 1:
            self.button_list[self.button_y][self.button_x].image = '1_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 2:
            self.button_list[self.button_y][self.button_x].image = '2_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 3:
            self.button_list[self.button_y][self.button_x].image = '3_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 4:
            self.button_list[self.button_y][self.button_x].image = '4_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 5:
            self.button_list[self.button_y][self.button_x].image = '5_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 6:
            self.button_list[self.button_y][self.button_x].image = '6_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 7:
            self.button_list[self.button_y][self.button_x].image = '7_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 8:
            self.button_list[self.button_y][self.button_x].image = '8_res.png'
        self.button_list[self.button_y][self.button_x].enabled = False
        self.squares_remaining -= 1

    def first_square_two(self):
        self.surrounding_list = [[int(self.button_y)-1,int(self.button_x)-1],[int(self.button_y)-1,int(self.button_x)],[int(self.button_y)-1,int(self.button_x)+1],
        [int(self.button_y),int(self.button_x)-1],[int(self.button_y),int(self.button_x)+1],
        [int(self.button_y)+1,int(self.button_x)-1],[int(self.button_y)+1,int(self.button_x)],[int(self.button_y)+1,int(self.button_x)+1],]
        i = 0
        l = len(self.surrounding_list)
        while i < l:
            if self.surrounding_list[i][0] < 0 or self.surrounding_list[i][0] > 14 or self.surrounding_list[i][1] < 0 or self.surrounding_list[i][1] > 14:
                del self.surrounding_list[i]
                l = len(self.surrounding_list)
            else:
                i += 1
        
        x = 0
        l = len(self.surrounding_list)
        while x<l: # this will remove all of the elements that are in another list
            if self.surrounding_list[x] in self.outside_list or self.surrounding_list[x] in self.opperating_list or self.surrounding_list[x] in self.finished_list:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        self.button_list[int(self.button_y)][int(self.button_x)].image = '0_res.png'
        self.button_list[int(self.button_y)][int(self.button_x)].enabled = False
        for i in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[i])
        self.finished_list.append([int(self.button_y),int(self.button_x)])

    def bomb_handler(self):
        app.info('Bomb', 'you have hit a mine, you lose :(')
        app.destroy()
    
    def completed_handler(self):
        app.info('You win!', 'Congratulations, you have completed the game in ' +str(self.time)+ ' seconds!')
        app.destroy()

    def create_game(self,event_data): # this will look at the square that the user clicked on, and then randomly generate where the bombs will be placed
       
        #the following is code that will choose where the bombs are going down, in response to the first click
        self.split = self.to_split.split(',')
        self.button_x = self.split[0]
        self.button_y = self.split[1] 
        self.bomb_cont = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this is a list that will store where the bombs are located
        for i in range(0,15): # everything in this for loop will create a blank template list, and this will be for storing the information about where the bombs are located
            for i in range(0,15):
                self.bomb_cont[i].append('0') # all of the sqaures that have a 0 are squares with no bombs on them, and squares with a 1 will be ones with bombs on them. The initial square that is clicked on will be an 'S', meaning Safe, and this is because the user cannot lose on their first go, which means that a bomb cannot be placed there
        self.bomb_cont[int(self.button_y)][int(self.button_x)] = 'S' # this means that this square can never have a bomb on it for the rest of the game
        try: # all of the following try except statements find the surrounding squares for the square that has just been clicked, and then put an 'S' on it, so taht there cannot be a bomb placed there, because otherwise you could get stuck right at the beggining of the game, which would not be ideal
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)+1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)][int(self.button_x)+1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)+1] = 'S'
        except:
            pass
        i = 0
        while i < 25:
            randomx = random.randint(0,14)
            randomy = random.randint(0,14) # this and randomx will be used to determine where the next bomb is going to go
            if self.bomb_cont[randomy][randomx] == '0':
                self.bomb_cont[randomy][randomx] = '1'
                i += 1
            elif self.bomb_cont[randomy][randomx] == '1' or self.bomb_cont[randomy][randomx] == 'S':
                pass
        store = 0
        for i in range(0,15):
            for j in range(0,15):
                if self.bomb_cont[i][j] == '1':
                    store += 1
        if store == 24: # there is a chance that there will end up being only 39 bombs, a small chance, but it could happen
            while i == 0:
                randomx = random.randint(0,14)
                randomy = random.randint(0,14)
                if self.bomb_cont[randomy][randomx] == '0':
                    self.bomb_cont[randomy][randomx] = '1'
                    i += 1
                elif self.bomb_cont[randomy][randomx] == '1' or self.bomb_cont[randomy][randomx] == 'S':
                    pass
        self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0])
        
        #the following code will come up with a list that will contain the number of bombs that each square is touching
        self.bomb_touch = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this is the containor, and when there is a number in a position, it means that there are that many bombs touching that square
        for i in range(0,15): # the following will just put positions in the list so that they can be edited later 
            for j in range(0,15):
                self.bomb_touch[i].append(0) # now every position is filled with 0, which means it can now be editied
        
        for i in range(1,14): # this creates all of the information on how many bombs are touching all of the squares that are not on the edges
            for j in range(1,14):
                self.analyse_center(j,i)
        
        for i in range(1,14): # this makes all of the boxes on the top line contain the numeber of bombs that that one is touching
            self.analyse_top_line(i)

        for i in range(1,14):
            self.analyse_bottom_line(i)

        for i in range(1,14):
            self.analyse_left(i)
        
        for i in range(1,14):
            self.analyse_right(i)

        self.left_corner()
        self.right_corner()
        self.btm_left()
        self.btm_right()

    def analyse_center(self,xval,yval):
        self.xval = xval
        self.yval = yval
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval-1][self.xval-1],self.bomb_cont[self.yval-1][self.xval],
            self.bomb_cont[self.yval-1][self.xval+1],self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval][self.xval+1],
            self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval],self.bomb_cont[self.yval+1][self.xval+1],]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count
        
    def analyse_top_line(self,xval):
        self.xval = xval
        self.yval = 0
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[0][self.xval-1],self.bomb_cont[0][self.xval+1],
            self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval],
            self.bomb_cont[self.yval+1][self.xval+1]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def analyse_bottom_line(self, xval):
        self.xval = xval
        self.yval = 14
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval][self.xval+1],
            self.bomb_cont[self.yval-1][self.xval-1],self.bomb_cont[self.yval-1][self.xval],
            self.bomb_cont[self.yval-1][self.xval+1]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def analyse_left(self,yval):
        self.yval = yval
        self.xval = 0
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval+1][0],self.bomb_cont[self.yval+1][1],self.bomb_cont[self.yval][1],
            self.bomb_cont[self.yval-1][1],self.bomb_cont[self.yval-1][0]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count
        
    def analyse_right(self,yval):
        self.yval = yval
        self.xval = 14
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval-1][self.xval],self.bomb_cont[self.yval-1][self.xval-1],
            self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def left_corner(self):
        if self.bomb_cont[0][0] == '1':
            self.bomb_touch[0][0] = 9
        else:
            self.touching_list = [self.bomb_cont[0][1],self.bomb_cont[1][1],self.bomb_cont[1][0]]
            count = self.touching_list.count('1')
            self.bomb_touch[0][0] = count
    
    def right_corner(self):
        if self.bomb_cont[0][14] == '1':
            self.bomb_touch[0][14] = 9
        else:
            self.touching_list = [self.bomb_cont[0][13],self.bomb_cont[1][13],self.bomb_cont[1],[14]]
            count = self.touching_list.count('1')
            self.bomb_touch[0][14] = count
    
    def btm_left(self):
        if self.bomb_cont[14][0] == '1':
            self.bomb_touch[14][0] = 9
        else:
            self.touching_list = [self.bomb_cont[13][0],self.bomb_cont[13][1],self.bomb_cont[13][1]]
            count = self.touching_list.count('1')
            self.bomb_touch[14][0] = count

    def btm_right(self):
        if self.bomb_cont[14][14] == '1':
            self.bomb_touch[14][14] = 9
        else:
            self.touching_list = [self.bomb_cont[13][14],self.bomb_cont[13][13],self.bomb_cont[14],[13]]
            count = self.touching_list.count('1')
            self.bomb_touch[14][14] = count
    
class Easy_Game:
    def __init__(self):
        pass

    def set_up_grid(self):
        self.squares_remaining = 100
        self.click_count = 0 # this will be used to determine when the game is started, when this goes up to one, the game will know that this is the first click
        self.button_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this will store all of the buttons in a list, so that it can easily be accessed, so that you can change the picture easily
        self.bomb_count = 10
        self.time = 0 # this will increase, and this will be used for the timer
        self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0]) # this will be changed as the game progresses, but this is currently a lable telling the user how many flags they have left to place
        self.time_lable = Text(top_cont, text = 'Time Elapsed: '+str(self.time), grid = [1,0]) # this tells the user how much time has elepsed
        self.time_lable.repeat(1000, self.increase_time) # this means that each second, self.increase_time will be called
        for i in range(0,10):
            for j in range(0,10):
                coords = str(str(i)+','+str(j)) # this will be assigned to the text, and it goes x,y but the lists work y,x
                #of the button, which can then be accessed later, which will be useful
                exec("button{}{} = PushButton(game_cont, grid = [{},{}], width = 25, height = 25, image = 'lightgrey.png', text = coords)".format(str(i), str(j),i,j))
                exec('button{}{}.when_right_button_pressed = self.place_flag'.format(str(i), str(j)))
                exec('button{}{}.when_left_button_pressed = self.left_clicked'.format(str(i), str(j)))
                exec('self.button_list[{}].append(button{}{})'.format(str(j),str(i),str(j)))

    def increase_time(self): # this controls the timer
        self.time += 1
        self.time_lable = Text(top_cont, text = 'Time Elapsed: '+str(self.time), grid = [1,0])

    def place_flag(self,event_data):
        self.to_split = (event_data.widget.text)
        self.split = self.to_split.split(',')
        self.button_x = self.split[0] # this will store the x coordinate of the button that has been pressed
        self.button_y = self.split[1] # this will store the y coordinate of the button that has been pressed
        if self.button_list[int(self.button_y)][int(self.button_x)].image != 'flagged2.png' and self.bomb_count > 0 and self.button_list[int(self.button_y)][int(self.button_x)].enabled == True: # the following will be executed if the current button has just the normal backgroup, and there are still flags left that can be placed
            exec("self.button_list[{}][{}].image = 'flagged2.png'".format(int(self.button_y), int(self.button_x))) # this will find the button in the list, and then change the image that it holds to a flag
            exec("self.button_list[{}][{}].enabled = False".format(int(self.button_y), int(self.button_x)))
            self.bomb_count -= 1 # this means that they will have one less flag to place
            self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0]) # this displays how many flags there are left to place
        elif self.button_list[int(self.button_y)][int(self.button_x)].image == 'flagged2.png': # this will check if this square has already been flaged, and if it has, then the flag will be removed, and then the count of the flags left will be increased by one
            exec("self.button_list[{}][{}].image = 'lightgrey.png'".format(int(self.button_y), int(self.button_x)))
            exec("self.button_list[{}][{}].enabled = True".format(int(self.button_y), int(self.button_x)))
            self.bomb_count += 1
            self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0])

    def left_clicked(self,event_data):
        self.to_split = (event_data.widget.text)
        self.split = self.to_split.split(',')
        self.button_x = self.split[0] # this will store the x coordinate of the button that has been pressed
        self.button_y = self.split[1]
        self.click_count += 1
        if self.click_count == 1: # this means that this is the first go
            self.create_game(self.to_split) # if it is the first go, then it will create the game, and figure out where the bombs are going ot be, and bassically create the game
            self.master_first_click()
        elif self.click_count > 1:
            if self.bomb_cont[int(self.button_y)][int(self.button_x)] == '0':
                if self.bomb_touch[int(self.button_y)][int(self.button_x)] == 0:
                    self.first_square_two() # this will deal with everything that needs to be done for the first square   
                    while len(self.outside_list)>0: # this whole process will be repeated until there are no squares left on the outside list, which means that there is nothing more to be done on this first turn
                        for i in range(0,len(self.outside_list)):
                            self.opperating_list.append(self.outside_list[i]) # this means that after the first click has been done, and the surrounding squares of the first square have been collected, you can now operate on them
                        self.outside_list = [] # all of the information has been transfered out of this list, and now it means thata we can find all of the new outside squares
                        for i in range(0,len(self.opperating_list)):
                            self.other_squares(i)
                        for i in range(0,len(self.opperating_list)):
                            self.finished_list.append(self.opperating_list[i])
                    self.squares_remaining = 100 # we need to reset this so that we can now look at all of the squares that are no longer enabled and work out the new squares remaining value
                    for i in range(0,len(self.button_list)):
                        for j in range(0,len(self.button_list[i])):
                            if self.button_list[i][j].image != 'lightgrey.png' and self.button_list[i][j].image != 'flagged2.png':
                                self.squares_remaining -= 1
                elif self.bomb_touch[int(self.button_y)][int(self.button_x)] != 0:
                    self.when_not_zero_two(int(self.button_y),int(self.button_x))
            elif self.bomb_cont[int(self.button_y)][int(self.button_x)] == '1':
                self.bomb_handler()
            if self.squares_remaining <= 10:
                self.remain_check()
                

    def remain_check(self): # this rechecks that there are only 10 squares left, and none have been removed becaues something was clicked twice while the program was laggingr
        for i in range(0,len(self.button_list)):
            for j in range(0,len(self.button_list[i])):
                if self.button_list[i][j].enabled == False:
                    self.squares_remaining -= 1
                    if self.squares_remaining == 0:
                        self.completed_handler()
                else:
                    pass

    def master_first_click(self):
        self.outside_list = [] # this stores all of the squares that are on the outside of the map that need to be looked at
        self.opperating_list = [] # this will store all of the squares that are being worked on in a cycle of working
        self.finished_list = [] # this will store the information for all of the squares that have already been dealt with, so that we don't get an infinate loop
        self.surrounding_list = [] # this will store the surrounding squares of one square, and this will be used lots
        self.first_square() # this will deal with everything that needs to be done for the first square   
        while len(self.outside_list)>0: # this whole process will be repeated until there are no squares left on the outside list, which means that there is nothing more to be done on this first turn
            for i in range(0,len(self.outside_list)):
                self.opperating_list.append(self.outside_list[i]) # this means that after the first click has been done, and the surrounding squares of the first square have been collected, you can now operate on them
            self.outside_list = [] # all of the information has been transfered out of this list, and now it means thata we can find all of the new outside squares
            for i in range(0,len(self.opperating_list)):
                self.other_squares(i)
            for i in range(0,len(self.opperating_list)):
                self.finished_list.append(self.opperating_list[i])
        for i in range(0,len(self.button_list)):
            for j in range(0,len(self.button_list[i])):
                if self.button_list[i][j].enabled == False:
                    self.squares_remaining -= 1 # this is so that we can check how many squares are left to be clicked
                
                
    def first_square(self): # this will do everything needed for the first square
        self.surrounding_list = [[int(self.button_y)-1,int(self.button_x)-1],[int(self.button_y)-1,int(self.button_x)],[int(self.button_y)-1,int(self.button_x)+1],
        [int(self.button_y),int(self.button_x)-1],[int(self.button_y),int(self.button_x)+1],
        [int(self.button_y)+1,int(self.button_x)-1],[int(self.button_y)+1,int(self.button_x)],[int(self.button_y)+1,int(self.button_x)+1],]
        i = 0
        l = len(self.surrounding_list)
        while i < l:
            if self.surrounding_list[i][0] < 0 or self.surrounding_list[i][0] > 9 or self.surrounding_list[i][1] < 0 or self.surrounding_list[i][1] > 9:
                del self.surrounding_list[i]
                l = len(self.surrounding_list)
            else:
                i += 1
        self.button_list[int(self.button_y)][int(self.button_x)].image = '0_res.png'
        self.button_list[int(self.button_y)][int(self.button_x)].enabled = False
        for i in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[i])
        self.finished_list.append([int(self.button_y),int(self.button_x)]) # this makes the first button go into the finished list, and this means that this will not be looked at in the future   

    def other_squares(self,track): # this will be done for the other squares of the first click
        self.track = track # track will be used to know which position in self.operating_list we are looking at, and this will just be the value of i in the for loop that controls this
        self.yval = self.opperating_list[self.track][0]
        self.xval = self.opperating_list[self.track][1]
        try:
            if self.bomb_touch[self.yval][self.xval] == 0:
                self.button_list[self.yval][self.xval].image = '0_res.png'
                self.button_list[self.yval][self.xval].enabled = False
                self.when_zero() # this calls the handeler when the value of the bomb touch for that square is 0
            else: # this handles when there is a bomb that this square is touching 
                self.when_not_zero()
        except:
            pass

    def when_zero(self): # this will handle if the value of the square on the bomb touch list is zero
        self.surrounding_list = [[self.yval-1,self.xval-1],[self.yval-1,self.xval],[self.yval-1,self.xval+1],
        [self.yval,self.xval-1],[self.yval,self.xval+1],
        [self.yval+1,self.xval-1],[self.yval+1,self.xval],[self.yval+1,self.xval+1]]
        x = 0
        l = len(self.surrounding_list)
        while x < l: # this one removes any squares that are not in the grid
            if self.surrounding_list[x][0] < 0 or self.surrounding_list[x][0] > 9 or self.surrounding_list[x][1] < 0 or self.surrounding_list[x][1] > 9:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        x = 0
        l = len(self.surrounding_list)
        while x<l: # this will remove all of the elements that are in another list
            if self.surrounding_list[x] in self.outside_list or self.surrounding_list[x] in self.opperating_list or self.surrounding_list[x] in self.finished_list:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        for a in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[a])
        
    def when_not_zero(self):
        if self.bomb_touch[self.yval][self.xval] == 1:
            self.button_list[self.yval][self.xval].image = '1_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 2:
            self.button_list[self.yval][self.xval].image = '2_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 3:
            self.button_list[self.yval][self.xval].image = '3_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 4:
            self.button_list[self.yval][self.xval].image = '4_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 5:
            self.button_list[self.yval][self.xval].image = '5_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 6:
            self.button_list[self.yval][self.xval].image = '6_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 7:
            self.button_list[self.yval][self.xval].image = '7_res.png'
        elif self.bomb_touch[self.yval][self.xval] == 8:
            self.button_list[self.yval][self.xval].image = '8_res.png'
        self.button_list[self.yval][self.xval].enabled = False

    def when_not_zero_two(self,button_y,button_x):
        self.button_y = button_y
        self.button_x = button_x
        if self.bomb_touch[self.button_y][self.button_x] == 1:
            self.button_list[self.button_y][self.button_x].image = '1_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 2:
            self.button_list[self.button_y][self.button_x].image = '2_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 3:
            self.button_list[self.button_y][self.button_x].image = '3_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 4:
            self.button_list[self.button_y][self.button_x].image = '4_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 5:
            self.button_list[self.button_y][self.button_x].image = '5_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 6:
            self.button_list[self.button_y][self.button_x].image = '6_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 7:
            self.button_list[self.button_y][self.button_x].image = '7_res.png'
        elif self.bomb_touch[self.button_y][self.button_x] == 8:
            self.button_list[self.button_y][self.button_x].image = '8_res.png'
        self.button_list[self.button_y][self.button_x].enabled = False
        self.squares_remaining -= 1

    def first_square_two(self):
        self.surrounding_list = [[int(self.button_y)-1,int(self.button_x)-1],[int(self.button_y)-1,int(self.button_x)],[int(self.button_y)-1,int(self.button_x)+1],
        [int(self.button_y),int(self.button_x)-1],[int(self.button_y),int(self.button_x)+1],
        [int(self.button_y)+1,int(self.button_x)-1],[int(self.button_y)+1,int(self.button_x)],[int(self.button_y)+1,int(self.button_x)+1],]
        i = 0
        l = len(self.surrounding_list)
        while i < l:
            if self.surrounding_list[i][0] < 0 or self.surrounding_list[i][0] > 9 or self.surrounding_list[i][1] < 0 or self.surrounding_list[i][1] > 9:
                del self.surrounding_list[i]
                l = len(self.surrounding_list)
            else:
                i += 1
        
        x = 0
        l = len(self.surrounding_list)
        while x<l: # this will remove all of the elements that are in another list
            if self.surrounding_list[x] in self.outside_list or self.surrounding_list[x] in self.opperating_list or self.surrounding_list[x] in self.finished_list:
                del self.surrounding_list[x]
                l = len(self.surrounding_list)
            else:
                x += 1

        self.button_list[int(self.button_y)][int(self.button_x)].image = '0_res.png'
        self.button_list[int(self.button_y)][int(self.button_x)].enabled = False
        for i in range(0,len(self.surrounding_list)):
            self.outside_list.append(self.surrounding_list[i])
        self.finished_list.append([int(self.button_y),int(self.button_x)])

    def bomb_handler(self):
        app.info('Bomb', 'you have hit a mine, you lose :(')
        app.destroy()
    
    def completed_handler(self):
        app.info('You win!', 'Congratulations, you have completed the game in ' +str(self.time)+ ' seconds!')
        app.destroy()

    def create_game(self,event_data): # this will look at the square that the user clicked on, and then randomly generate where the bombs will be placed
       
        #the following is code that will choose where the bombs are going down, in response to the first click
        self.split = self.to_split.split(',')
        self.button_x = self.split[0]
        self.button_y = self.split[1] 
        self.bomb_cont = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this is a list that will store where the bombs are located
        for i in range(0,10): # everything in this for loop will create a blank template list, and this will be for storing the information about where the bombs are located
            for i in range(0,10):
                self.bomb_cont[i].append('0') # all of the sqaures that have a 0 are squares with no bombs on them, and squares with a 1 will be ones with bombs on them. The initial square that is clicked on will be an 'S', meaning Safe, and this is because the user cannot lose on their first go, which means that a bomb cannot be placed there
        self.bomb_cont[int(self.button_y)][int(self.button_x)] = 'S' # this means that this square can never have a bomb on it for the rest of the game
        try: # all of the following try except statements find the surrounding squares for the square that has just been clicked, and then put an 'S' on it, so taht there cannot be a bomb placed there, because otherwise you could get stuck right at the beggining of the game, which would not be ideal
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)-1][int(self.button_x)+1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)][int(self.button_x)+1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)-1] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)] = 'S'
        except:
            pass
        try:
            self.bomb_cont[int(self.button_y)+1][int(self.button_x)+1] = 'S'
        except:
            pass
        i = 0
        while i < 10:
            randomx = random.randint(0,9)
            randomy = random.randint(0,9) # this and randomx will be used to determine where the next bomb is going to go
            if self.bomb_cont[randomy][randomx] == '0':
                self.bomb_cont[randomy][randomx] = '1'
                i += 1
            elif self.bomb_cont[randomy][randomx] == '1' or self.bomb_cont[randomy][randomx] == 'S':
                pass
        store = 0
        for i in range(0,10):
            for j in range(0,10):
                if self.bomb_cont[i][j] == '1':
                    store += 1
        if store == 9: # there is a chance that there will end up being only 39 bombs, a small chance, but it could happen
            while i == 0:
                randomx = random.randint(0,9)
                randomy = random.randint(0,9)
                if self.bomb_cont[randomy][randomx] == '0':
                    self.bomb_cont[randomy][randomx] = '1'
                    i += 1
                elif self.bomb_cont[randomy][randomx] == '1' or self.bomb_cont[randomy][randomx] == 'S':
                    pass
        self.bomb_lable = Text(top_cont, text = 'Flags Left: '+str(self.bomb_count)+'   ', grid = [0,0])
        
        #the following code will come up with a list that will contain the number of bombs that each square is touching
        self.bomb_touch = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # this is the containor, and when there is a number in a position, it means that there are that many bombs touching that square
        for i in range(0,10): # the following will just put positions in the list so that they can be edited later 
            for j in range(0,10):
                self.bomb_touch[i].append(0) # now every position is filled with 0, which means it can now be editied
        
        for i in range(1,9): # this creates all of the information on how many bombs are touching all of the squares that are not on the edges
            for j in range(1,9):
                self.analyse_center(j,i)
        
        for i in range(1,9): # this makes all of the boxes on the top line contain the numeber of bombs that that one is touching
            self.analyse_top_line(i)

        for i in range(1,9):
            self.analyse_bottom_line(i)

        for i in range(1,9):
            self.analyse_left(i)
        
        for i in range(1,9):
            self.analyse_right(i)

        self.left_corner()
        self.right_corner()
        self.btm_left()
        self.btm_right()

    def analyse_center(self,xval,yval):
        self.xval = xval
        self.yval = yval
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval-1][self.xval-1],self.bomb_cont[self.yval-1][self.xval],
            self.bomb_cont[self.yval-1][self.xval+1],self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval][self.xval+1],
            self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval],self.bomb_cont[self.yval+1][self.xval+1],]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count
        
    def analyse_top_line(self,xval):
        self.xval = xval
        self.yval = 0
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[0][self.xval-1],self.bomb_cont[0][self.xval+1],
            self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval],
            self.bomb_cont[self.yval+1][self.xval+1]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def analyse_bottom_line(self, xval):
        self.xval = xval
        self.yval = 9
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval][self.xval+1],
            self.bomb_cont[self.yval-1][self.xval-1],self.bomb_cont[self.yval-1][self.xval],
            self.bomb_cont[self.yval-1][self.xval+1]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def analyse_left(self,yval):
        self.yval = yval
        self.xval = 0
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval+1][0],self.bomb_cont[self.yval+1][1],self.bomb_cont[self.yval][1],
            self.bomb_cont[self.yval-1][1],self.bomb_cont[self.yval-1][0]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count
        
    def analyse_right(self,yval):
        self.yval = yval
        self.xval = 9
        if self.bomb_cont[self.yval][self.xval] == '1':
            self.bomb_touch[self.yval][self.xval] = 9
        else:
            self.touching_list = [self.bomb_cont[self.yval-1][self.xval],self.bomb_cont[self.yval-1][self.xval-1],
            self.bomb_cont[self.yval][self.xval-1],self.bomb_cont[self.yval+1][self.xval-1],self.bomb_cont[self.yval+1][self.xval]]
            count = self.touching_list.count('1')
            self.bomb_touch[self.yval][self.xval] = count

    def left_corner(self):
        if self.bomb_cont[0][0] == '1':
            self.bomb_touch[0][0] = 9
        else:
            self.touching_list = [self.bomb_cont[0][1],self.bomb_cont[1][1],self.bomb_cont[1][0]]
            count = self.touching_list.count('1')
            self.bomb_touch[0][0] = count
    
    def right_corner(self):
        if self.bomb_cont[0][9] == '1':
            self.bomb_touch[0][9] = 9
        else:
            self.touching_list = [self.bomb_cont[0][8],self.bomb_cont[1][8],self.bomb_cont[1],[9]]
            count = self.touching_list.count('1')
            self.bomb_touch[0][9] = count
    
    def btm_left(self):
        if self.bomb_cont[9][0] == '1':
            self.bomb_touch[9][0] = 9
        else:
            self.touching_list = [self.bomb_cont[8][0],self.bomb_cont[8][1],self.bomb_cont[9][1]]
            count = self.touching_list.count('1')
            self.bomb_touch[9][0] = count

    def btm_right(self):
        if self.bomb_cont[9][9] == '1':
            self.bomb_touch[9][9] = 9
        else:
            self.touching_list = [self.bomb_cont[8][9],self.bomb_cont[8][8],self.bomb_cont[9],[8]]
            count = self.touching_list.count('1')
            self.bomb_touch[9][9] = count
    
app.display()