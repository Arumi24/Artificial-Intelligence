import numpy as np
import copy 
import sys
import time

class Board(object):

    def __init__(self,config):
        self.board=config

    def move(self):
        for x in range(len(self.board)):
            if self.board[x]=="_":

                 
                return x

    def swap(self,x,y):
        dummy=copy.deepcopy(self.board)
        temp=dummy[y]
        dummy[y]=dummy[x]
        dummy[x]=temp
        return dummy
    

    def getData(self):
        return self.board

    def isStart(self):
        return self.isStart

    def applyMove(self, number):
        list=[]

       

        if number==0:
            list.append(self.swap(0,1))
            list.append(self.swap(0,3))
        elif number==1:
            list.append(self.swap(1,0))
            list.append(self.swap(1,2))
            list.append(self.swap(1,4))
        elif number==2:
            list.append(self.swap(2,1))
            list.append(self.swap(2,5))
        elif number==3:
            list.append(self.swap(3,0))
            list.append(self.swap(3,4))
            list.append(self.swap(3,6))
        elif number==4:
            list.append(self.swap(4,1))
            list.append(self.swap(4,5))
            list.append(self.swap(4,3))
            list.append(self.swap(4,7))
        elif number==5:
            list.append(self.swap(5,2))
            list.append(self.swap(5,4))
            list.append(self.swap(5,8))
        elif number==6:
            list.append(self.swap(6,3))
            list.append(self.swap(6,7))
        elif number==7:
            list.append(self.swap(7,6))
            list.append(self.swap(7,4))
            list.append(self.swap(7,8))
        else:
            list.append(self.swap(8,5))
            list.append(self.swap(8,7))

        return list

    def printBoard(self):
        board=copy.deepcopy(self.board)
        print(board.reshape(3,3))

class Node(object):

    def __init__(self,data,parent=None):
        self.parent=parent
        self.data=data
        self.children=[]

        if self.parent==None:
            self.depth=0
        else:
            self.depth=self.parent.depth+1
    
    def addChild(self, node):
        self.children.append(node)


    def printData(self):
        print(self.data)

    def getData(self):
        return self.data
    
class Tree(object):

    def __init__(self,root):
        self.root=root
        self.nodes=[]
        self.nodes.append(root)
        self.currentNode=root
        self.currentPointer=0
        self.depth=self.currentNode.depth
        

    def traverseToNext(self):

        self.currentPointer=self.currentPointer+1
        self.currentNode=self.nodes[self.currentPointer]
        self.depth=self.currentNode.depth

    def addChild(self,node):
        
        self.nodes.append(node)
        self.currentNode.addChild(node)

    def printTree(self):

        for x in self.nodes:
            x.printData()
            print(x.depth)
            print("")

class PuzzleSolver(object):

    def __init__(self,initial,goal):
        self.board=Board(initial)
        self.root=Node(self.board)
        self.tree=Tree(self.root)
        self.goal=goal
        self.initial=initial
        self.memoization=[]

    def heuristic(self,state):
        
        manhattan_distance=0

        for i in range(len(state)):
            if state[i]!=self.goal[i]:
                manhattan_distance=manhattan_distance+1
        
        return manhattan_distance
    
    def solvable(self):

        inversions=0
        for i in range(len(self.initial)):  
            if self.initial[i]!='_': 
                for j in range(i+1,len(self.initial)):
                    if self.initial[j]!='_':
                        if int(self.initial[j])<int(self.initial[i]):
                            inversions=inversions+1
        
        if inversions%2==0:
            return True
        else:
            return False

    def printTree(self):

        for x in self.tree.nodes:
            
            print(x.depth)  
            x.getData().printBoard()
            print("")
            
            
    def checkIn(self,array):
        for x in self.memoization:
            if np.array_equal(array,x):
                return True
            
        return False

    def populateTree(self, depth):

        heuristic=self.heuristic(self.initial)

        if self.solvable()==False:
            print("This configuration is unsolvable")
            return
        else:
           
            self.memoization.append(self.board.board)
          
            while(0!=1):

                for x in range(len(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move()))):

                    if (self.checkIn(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move())[x]))==False:

                        if self.heuristic(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move())[x])<=heuristic or self.heuristic(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move())[x])>heuristic:
                            
                          
                            self.memoization.append(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move())[x])
                           

                            self.tree.addChild(Node(Board(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move())[x]),
                                self.tree.currentNode))


                    if (np.array_equal(self.tree.currentNode.data.applyMove(self.tree.currentNode.data.move())[x],self.goal))==True:
                        self.printTree()
                        return
            
                try:
                    self.tree.traverseToNext()

                except IndexError:
                    print("You are cycling through, can't expand tree anymore: goal unreachable")
                    break
           
                if(self.tree.depth>depth):
                
                    print("nothing")
                    break
    
def main():

    solver=PuzzleSolver(np.array(['3','4','7','6','5','1','_','8','2']),np.array(['1','2','3','4','5','6','7','8','_']))

    start = time.time() 
    solver.populateTree(25)

  

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()



