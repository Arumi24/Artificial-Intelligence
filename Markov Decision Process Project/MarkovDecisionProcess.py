from Graph import State,Action,MarkovDecisionGraph
import pprint

class MDP(object):
    
    def __init__(self,data):

        self.data=data
        self.actions_per_states={}
        self.utilities={}
        for key in self.data.keys():
            self.actions_per_states[key]=key.getActions()
            self.utilities[key]=0.0

    def value_iteration(self,iterations,discount_factor):

        for i in range(iterations):
            
            for key in self.utilities.keys():
                
                transition_state_utilities=[]

                for i in self.actions_per_states[key]:
                    
                    transition_state_utilities.append(self.utilities[i[1]])

                
                if len(transition_state_utilities)>0:
                    self.utilities[key]=key.getReward()+discount_factor*max(transition_state_utilities)
                else:
                    self.utilities[key]=key.getReward()






        



def createAgent():
   
    start=State(0,True)

    empty1=State(0,False)
    empty2=State(0,False)
    empty3=State(0,False)

    bad1=State(-100,False)
    bad2=State(-100,False)
    bad3=State(-100,False)
    bad4=State(-100,False)
    bad5=State(-100,False)
    bad6=State(-100,False)


    goal10=State(100,False)
    goal1=State(10,False)
    goal10000=State(300,False)

    graph=MarkovDecisionGraph(start)

    graph.addAction(start,goal1,"left")
    graph.addAction(start,empty1,"right")

    graph.addAction(start,bad1,"up")
    graph.addAction(bad1,start,"down")

    graph.addAction(start,bad2,"down")
    graph.addAction(bad2,start,"up")

    
    graph.addAction(empty1,start,"left")
    graph.addAction(empty1,empty2,"right")
    graph.addAction(empty1,bad3,"up")
    graph.addAction(bad3,empty1,"down")

    graph.addAction(empty1,bad4,"down")

    graph.addAction(bad4,empty1,"up")


    graph.addAction(empty2,goal10,"right")

    graph.addAction(empty2,empty1,"left")
    graph.addAction(empty2,bad5,"up")
    graph.addAction(bad5,empty2,"down")

    graph.addAction(empty2,bad6,"down")
    graph.addAction(bad6,empty2,"up")

    graph.addAction(bad5,empty3,"up")
    graph.addAction(empty3,bad5,"down")


    graph.addAction(empty3,goal10000,"right")
    """
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


    """

    pprint.pprint(graph.coordinates)

    graph.Normalize()
    print("")

    pprint.pprint(graph.coordinates)

    #graph.Gridify()

    print("")

    pprint.pprint(graph.coordinates)

    mdp=MDP(graph.coordinates)

    mdp.value_iteration(1000,0.99)

    for key in mdp.actions_per_states.keys():
        print(key,key.getReward(),mdp.actions_per_states[key])
        print("")
    
   
    pprint.pprint(mdp.utilities)
    """
    game=Game(graph.coordinates)

    


    game.runGame()
    """
    return graph.coordinates,mdp.utilities, mdp.actions_per_states



if __name__ == '__main__':
    main()


    
    