import numpy as np

class SudokuSolver(object):

    def __init__(self,N):
        self.board=np.zeros((9,9))
        self.fillRandom(N)
    
    def fillRandom(self,N):
        count=0
        while(count<N):
            value=np.random.randint(1,10)
            x=np.random.randint(9)
            y=np.random.randint(9)
        
            if self.board[x][y]==0:
                if self.allowed(value,x,y)==True:
                    self.board[x][y]=value
                    count=count+1
    
    def allowed(self,value,x,y):
    
        for i in range(9):
            if i!=x:
                if(self.board[i][y])==value:
                    return False
            
        for j in range(9):
            if j!=y:
                if(self.board[x][j])==value:
                    return False
    
        if(self.boxCheck(value,x,y)==False):
            return False

        return True

    def boxCheck(self,value,x,y): 
        if x%3==0:
            if y%3==0:
                for i in range(3):
                    for j in range(3):
                        if (i==0 and j==0)==False:   
                            if (self.board[x+i][y+j])==value:
                                return False

            elif y%3==1:
                for i in range(3):
                    for j in range(3):
                        if (i==0 and j==1)==False: 
                            if (self.board[x+i][y-1+j])==value:
                                return False
            else:
                for i in range(3):
                    for j in range(3):
                        if (i==0 and j==2)==False: 
                            if (self.board[x+i][y-2+j])==value:
                                return False
        elif x%3==1:
            if y%3==0:
                for i in range(3):
                    for j in range(3):
                        if (i==1 and j==0)==False:  
                            if (self.board[x+i-1][y+j])==value:
                                return False
            elif y%3==1:
                for i in range(3):
                    for j in range(3):
                        if (i==1 and j==1)==False: 
                            if (self.board[x+i-1][y-1+j])==value:
                                return False
            else:
                for i in range(3):
                    for j in range(3):
                        if (i==1 and j==2)==False: 
                            if(self.board[x+i-1][y-2+j])==value:
                                return False
        else:
            if y%3==0:
                for i in range(3):
                    for j in range(3):
                        if (i==2 and j==0)==False: 
                            if(self.board[x+i-2][y+j])==value:
                                return False
            elif y%3==1:
                for i in range(3):
                    for j in range(3):
                        if (i==2 and j==1)==False: 
                            if(self.board[x+i-2][y-1+j])==value:
                                return False
            else:
                for i in range(3):
                    for j in range(3):
                        if (i==2 and j==2)==False: 
                            if(self.board[x+i-2][y-2+j])==value:
                                return False
        return True

    def printBoard(self):

        for i in range(len(self.board)):
            if i%3==0:
                print("")
            for j in range(3):
                if j==0:
                    print(self.board[i][0:3],end=' ')
                elif j==1:
                    print(self.board[i][3:6],end=' ')
                else:
                    print(self.board[i][6:9])

    def solve(self):
            
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col]==0.0:
                    for value in range(1,10):
                        if(self.allowed(value,row,col)==True):
                            self.board[row][col]=value
                            self.solve()
                            self.board[row][col]=0
                    return 
        self.printBoard()
        input("More?")


def main():
    solver= SudokuSolver(10)

    solver.printBoard()
    print("*********************************")
    solver.solve()

if __name__ == '__main__':
    main()