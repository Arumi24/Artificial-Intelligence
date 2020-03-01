import numpy as np
import pprint


class N_Queens(object):
    
    def __init__(self,size):
        self.size=size
        self.board=np.zeros(shape=(size,size))

    def printBoard(self):
        pprint.pprint(self.board)
    
    def possible(self,x,y):
        count=0

        # veritcal
        for i in range(0,self.size):
            if i!=x:
                if self.board[i][y]==1:
                    count=count+1
        
        # horizontal
        for i in range(0,self.size):
            if i!=y:
                if self.board[x][i]==1:
                    count=count+1
          
        # diagonal 1
        for i in range(0,y):
            if ((x-i-1>=0) and (x-i-1<=self.size-1)) and ((y-i-1>=0) and (y-i-1<=self.size-1)):
                if self.board[x-i-1][y-i-1]==1:
                    count=count+1
        
        for i in range(y+1,self.size):
            if ((x+(i-y)>=0) and (x+(i-y)<=self.size-1)) and ((y+(i-y)>=0) and (y+(i-y)<=self.size-1)):
                if self.board[x+(i-y)][y+(i-y)]==1:
                    count=count+1
                  
        # diagonal 2
        for i in range(0,y):
            if ((x+i+1>=0) and (x+i+1<=self.size-1)) and ((y-i-1>=0) and (y-i-1<=self.size-1)):
                if self.board[x+i+1][y-i-1]==1:
                    count=count+1
        
        for i in range(y+1,self.size):
            if ((x-(i-y)>=0) and (x-(i-y)<=self.size-1)) and ((y+(i-y)>=0) and (y+(i-y)<=self.size-1)):
                if self.board[x-(i-y)][y+(i-y)]==1:
                    count=count+1

        if count==0:
            return True
        else:
            return False

        
    def solve(self,col):

        if col>=self.size:
            return True
        
        for x in range(self.size):
            if (self.possible(x,col))==True:
                self.board[x][col]=1

                if self.solve(col+1)==True:
                    return True
                
                self.board[x][col]=0
        
        return False


def main():
    board=N_Queens(8)
    
    if board.solve(0):
        board.printBoard()
    else:
        print("No Solutions Found")
    
if __name__ == '__main__':
    main()

