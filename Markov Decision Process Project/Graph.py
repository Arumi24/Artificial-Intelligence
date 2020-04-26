import pprint
import time

class State(object):

    def __init__(self,reward,start=False):
        
        self.isStart=start
        self.reward=reward
        if start:
            self.x=0
            self.y=0
        else:
            self.x=None
            self.y=None

        self.actions=[]
        self.transitionStates=[]

    def ifStart(self):
        return self.isStart

    def getReward(self):
        
        return self.reward
    
    def getCoordinates(self):

        return self.x,self.y
    
    def updateX(self,x):
        self.x=x
    
    def updateY(self,y):
        self.y=y
    
    def addAction(self,action):
        
        actionTo=[]
        actionTo.append(action[0])
        actionTo.append(action[2])
        self.actions.append(actionTo)
        self.transitionStates.append(action[2])

    def getActions(self):
        
        return self.actions

    def getTransitionStates(self):
        
        return self.transitionStates


class Action(object):

    def __init__(self,fromm,to,action):

        self.action=action
        self.fromm=fromm
        self.to=to

        fromm.addAction(self.getAction())
     
        self.updateToCoordinates(fromm,to,action)
        
    
    def updateToCoordinates(self,fromm,to,action):
        
        if action=="left":
            to.updateX(fromm.getCoordinates()[0])
            to.updateY(fromm.getCoordinates()[1]-1)

        if action=="right":
            to.updateX(fromm.getCoordinates()[0])
            to.updateY(fromm.getCoordinates()[1]+1)

        if action=="up":
            to.updateX(fromm.getCoordinates()[0]-1)
            to.updateY(fromm.getCoordinates()[1])

        if action=="down":
            to.updateX(fromm.getCoordinates()[0]+1)
            to.updateY(fromm.getCoordinates()[1])


    def getFrom(self):

        return self.fromm

    def getTo(self):

        return self.to

    def getAction(self):

        return [self.action,self.fromm,self.to]


class MarkovDecisionGraph(object):

    def __init__(self,start_node):
        
        self.start_node=start_node
        self.pointer=start_node
        self.node_list=[]
        self.node_list.append(self.start_node)
        self.actions=[]
        self.coordinates={}
        self.coordinates[start_node]=[start_node.getCoordinates()[0],start_node.getCoordinates()[1]]

        self.min_y=0
        self.min_x=0


    def createState(self,R):
        state=State(R)
        self.node_list.append(state)

    def addAction(self,fromm,to,action):

        action=Action(fromm,to,action)
        self.actions.append(action)
        self.coordinates[to]=[to.getCoordinates()[0],to.getCoordinates()[1]]

        if to.getCoordinates()[0]<self.min_x:
            self.min_x=to.getCoordinates()[0]
        if to.getCoordinates()[1]<self.min_y:
            self.min_y=to.getCoordinates()[1]

        if to not in self.node_list:
            self.node_list.append(to)

    def getActions(self):

        return self.actions

    def getCoordinates(self):

        return self.coordinates

    def Normalize(self):

        for k in self.coordinates.keys():
          
            if self.min_x<0:
                self.coordinates[k][0]=self.coordinates[k][0]+(-1*self.min_x)

            if self.min_y<0:
                self.coordinates[k][1]=self.coordinates[k][1]+(-1*self.min_y)

    def Gridify(self):

        for k in self.coordinates.keys():
          
            temp=self.coordinates[k][0]
            self.coordinates[k][0]=self.coordinates[k][1]
            self.coordinates[k][1]=temp
            
    
def main():

    start=State(0,True)
    goal1=State(10,False)
    empty1=State(0,False)
    empty2=State(0,False)
    empty3=State(0,False)
    goal2=State(100,False)
    bad1=State(-100,False)

    graph=MarkovDecisionGraph(start)

    graph.addAction(start,goal1,"left")
    graph.addAction(start,empty1,"right")
    graph.addAction(start,bad1,"down")
    graph.addAction(bad1,start,"up")

    graph.addAction(empty1,start,"left")
    graph.addAction(empty1,empty2,"right")


    graph.addAction(empty2,empty1,"left")
    graph.addAction(empty2,empty3,"right")

    graph.addAction(empty3,empty2,"left")
    graph.addAction(empty3,goal2,"right")
  

    pprint.pprint(graph.coordinates)

    graph.Normalize()
    print("")

    pprint.pprint(graph.coordinates)

    #graph.Gridify()

    print("")

    pprint.pprint(graph.coordinates)

   
if __name__ == '__main__':
    main()



