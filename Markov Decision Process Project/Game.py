
import pygame
import os
import math
import MarkovDecisionProcess as mpd
import time

class Game(object):

    
    def __init__(self,data,utilities,actions):

        self.utilities=utilities
        self.actions=actions
        self.PICTURE=pygame.image.load(os.path.join('res','game.png'))

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

    # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 48
        self.HEIGHT = 48
 
    # This sets the margin between each cell
        self.MARGIN = 2
        
        self.data=data
        self.states=list(data.keys())

        self.grid = []
        for row in range(10):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(10):
                self.grid[row].append(2)  # Append a cell
        
        size_x,size_y=self.getSize()
        self.WINDOW_SIZE = [(size_y+1)*50, (size_x+1)*50]

        for key in data.keys():
            
            if key.ifStart():
                
                self.start_x,self.start_y=data[key][0],data[key][1]

                print("X pos is {}".format(self.start_x))
                print("Y pos is {}".format(self.start_y))

            print(key.getReward())
            
            if key.getReward()==-100 or key.getReward()>=0:
        
                self.grid[data[key][0]][data[key][1]]=0

        self.grid[self.start_x][self.start_y]=1


    def getSize(self):

        max_x=0
        max_y=0

        for k in self.data.keys():
            if self.data[k][0]>max_x:
                max_x=self.data[k][0]
            if self.data[k][1]>max_y:
                max_y=self.data[k][1]
        
        return max_x,max_y
    
    def getNodeAt(self,y,x):
        
        for k in self.data.keys():
            if self.data[k][0]==x and self.data[k][1]==y:
                return k   

        return False

    def runGame(self):


        length=len(self.utilities)
        mdp=False

        pygame.init()
        font = pygame.font.Font(None, 20)
        screen = pygame.display.set_mode(self.WINDOW_SIZE)

        pygame.display.set_caption("Markov Decision")

        done = False
 
        clock = pygame.time.Clock()

        Reward=0
       
        while not done:
            
            if mdp==False:
                for event in pygame.event.get():  # User did something

                
                    print("POSITION IS {},{} and Reward is {} ".format(self.start_x,self.start_y,self.getNodeAt(self.start_y,self.start_x).reward))
                
              
                    if event.type == pygame.QUIT:  # If user clicked close
                        done = True  # Flag that we are done so we exit this loop

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_LEFT and self.start_y-1>=0:
                      
                            if not self.getNodeAt(self.start_y-1,self.start_x)==False:

                                self.grid[self.start_x][self.start_y-1]=1
                                self.grid[self.start_x][self.start_y]=0
                                self.start_y=self.start_y-1
                       

                        if event.key == pygame.K_RIGHT and self.start_y+1<self.WINDOW_SIZE[0]/(self.WIDTH+self.MARGIN) :
                       
                            if not self.getNodeAt(self.start_y+1,self.start_x)==False:
                                self.grid[self.start_x][self.start_y+1]=1
                                self.grid[self.start_x][self.start_y]=0
                                self.start_y=self.start_y+1
                        

                        if event.key == pygame.K_UP and self.start_x-1>=0 :

                            if not self.getNodeAt(self.start_y,self.start_x-1)==False:
                                self.grid[self.start_x-1][self.start_y]=1
                                self.grid[self.start_x][self.start_y]=0
                                self.start_x=self.start_x-1
                        

                        if event.key == pygame.K_DOWN and self.start_x+1<self.WINDOW_SIZE[1]/(self.HEIGHT+self.MARGIN) :
                        
                            if not self.getNodeAt(self.start_y,self.start_x+1)==False:
                                self.grid[self.start_x+1][self.start_y]=1
                                self.grid[self.start_x][self.start_y]=0
                                self.start_x=self.start_x+1


                        if event.key == pygame.K_SPACE :
                            
                            mdp=True
            else:
         
                for event in pygame.event.get(): 

                    if self.getNodeAt(self.start_y,self.start_x)==False:
                        
                        done = True


                    if event.key == pygame.K_SPACE :
                        if self.getNodeAt(self.start_y,self.start_x).getReward()<=0:
                            pygame.time.wait(1000)
                     
                            move=self.findBestMove(self.getNodeAt(self.start_y,self.start_x))

                            if move=='left':
                                self.grid[self.start_x][self.start_y-1]=1
                                self.grid[self.start_x][self.start_y]=0
                                self.start_y=self.start_y-1

                            if move=='right':
                                
                                    self.grid[self.start_x][self.start_y+1]=1
                                    self.grid[self.start_x][self.start_y]=0
                                    self.start_y=self.start_y+1

                            if move=='up':

                                    self.grid[self.start_x-1][self.start_y]=1
                                    self.grid[self.start_x][self.start_y]=0
                                    self.start_x=self.start_x-1


                            if move=='down':
                                    self.grid[self.start_x+1][self.start_y]=1
                                    self.grid[self.start_x][self.start_y]=0
                                    self.start_x=self.start_x+1
                    

        
            screen.fill(self.BLACK)

            for row in range(10):
                for column in range(10):
                    color = self.WHITE

                    pygame.draw.rect(screen,
                    color,[(self.MARGIN + self.WIDTH) * column + self.MARGIN,(self.MARGIN + self.HEIGHT) * row + self.MARGIN,self.WIDTH,self.HEIGHT])
                    
                    
                    if not self.getNodeAt(column,row)==False:
                        
                        if self.getNodeAt(column,row).reward>0:
                            value=font.render("+"+str(self.getNodeAt(column,row).reward), True,(0, 0, 0))
                        else:
                            value=font.render(str(self.getNodeAt(column,row).reward), True,(0, 0, 0))
                        utility=font.render(str(0.0), True,(0, 0, 0))

                        screen.blit(value, [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT])
                    
                        screen.blit(utility, [(self.MARGIN + self.WIDTH) * column + self.MARGIN+17.5,
                                    (self.MARGIN + self.HEIGHT) * row + self.MARGIN+20,
                                    self.WIDTH,
                                    self.HEIGHT])
                    
                    if self.grid[row][column] == 1:
                        pygame.draw.rect(screen,
                            color,[(self.MARGIN + self.WIDTH) * column + self.MARGIN,(self.MARGIN + self.HEIGHT) * row + self.MARGIN,self.WIDTH,self.HEIGHT])
                        screen.blit(self.PICTURE, [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT])

            
                    if self.grid[row][column] == 2:
                        pygame.draw.rect(screen,
                            self.BLACK,[(self.MARGIN + self.WIDTH) * column + self.MARGIN,(self.MARGIN + self.HEIGHT) * row + self.MARGIN,self.WIDTH,self.HEIGHT])

            clock.tick(1000)
   
            pygame.display.flip()
        
        pygame.quit()


  
   
    def findBestMove(self,state):

    
   
        maxim=0
        move=''
    
        for action in self.actions[state]:
            if self.utilities[action[1]]>maxim:
                maxim=self.utilities[action[1]]
                move=action[0]
        
        return move

        
def main():
    print("hello")
    coordindates,utilities,actions=mpd.createAgent()
    game=Game(coordindates,utilities,actions)


    game.runGame()


if __name__ == '__main__':
    main()
