import networkx as nx
import numpy as np
from create_network import create_tube
import matplotlib.pyplot as plt
import seaborn as sns


G = create_tube() #Generate the network with stations
G = G.lines() 

stations = list(G.nodes) #Get a list of nodes
stations = list(G.nodes)
name_to_index = {k: v for v, k in enumerate(stations)} #create name to index dictionary
name_to_index['Westminster']
index_to_name = {v: k for k, v in name_to_index.items()} #https://stackoverflow.com/questions/483666/reverse-invert-a-dictionary-mapping
G1 = nx.relabel_nodes(G,name_to_index) #create a network which works by index rather than name

class Tube: 

    def __init__(self, G, destination):
        
        #Initialise the environment, the reward matrix and Q Matrix! 
        self.network = G
        self.N = len(G) #size of environment
        self.tube = -1* np.ones((len(G), len(G))) #can't move to positions with -1 (these are outside of bounds)
        self.position_agent = None 
        self.position_exit = None
        self.destination = destination
        self.time_elapsed = 0
        self.reward = 0
        self.edge_list = list(G.edges(data=True)) #get a list of possible actions from each station

        for edge in G.edges:
            self.tube[edge] = 0 #fill in possible positions and movements
        

        #set position of agent before creating delays and cancellations

        self.position_exit = name_to_index[self.destination] #numerical position of the destination using name to index mapping
       
        self.delays = np.random.randint(0, (self.N*2)-1, size = (self.N//2)) #index of the edges with delays

        e = list(G.edges)

        for d in self.delays:
            self.tube[e[d]] = 1 #Some stations have delays
        
        self.closed = np.random.randint(0,(self.N*2)-1, size = self.N//10) #generates random numbers between 1 and 20 which then is used to index edges that will be closed

        for c in self.closed:
            self.tube[e[c]] = 2 #Some routes are closed! 

        #During initialisation, pick stations at random which will be closed or will have delays
        #End destination is decided upon initialisation
        

       # self.position_agent = a random free node on the system (a station). The choices the agent has are those of its starting position

        self.position_agent = np.random.randint(0, (self.N))
        self.current_station = index_to_name[self.position_agent]
        #Each node is a station and has a 'colour' which corresponds to a new service
        #when we initialise we should show the possible movements for the agent
        self.color = 0

    def reveal_avail_movement(self):
        self.available_pos = []
        self.available_stations = []
        for i in range(0,self.N): 
            if self.tube[self.position_agent][i] != -1 and self.position_agent != i: #if there is a possible movement that isnt the current position
                self.available_pos.append(i) #append index of possible movement to an array 
                self.available_stations.append(index_to_name[i])
        return self.available_stations #return available stations


    def step(self, action):
 
        self.position_agent_new = self.available_pos[action] #This shows the new station that the agent is at
        self.old_position = self.position_agent
        for k in range(0,len(self.edge_list)): #Loop through the list of routes

            if self.edge_list[k][0] == self.position_agent and self.edge_list[k][1] == self.available_pos[action]: #for the route that the agent has taken
                self.new_color = (self.edge_list[k][2]) #This finds what line the agent would take

        if (self.tube[self.position_agent][self.available_pos[action]]) == 0: #this looks to see what the reward will be for the movement
            r = 0
            self.position_agent = self.position_agent_new
            self.current_station = index_to_name[self.position_agent]
        if (self.tube[self.position_agent][self.available_pos[action]]) == 1:
            r = -10
            self.position_agent = self.position_agent_new
            self.current_station = index_to_name[self.position_agent]
        if (self.tube[self.position_agent][self.available_pos[action]]) == 2: 
            r = -20
            print("The route to "+ index_to_name[self.available_pos[action]]+" is closed!")
            self.current_station = index_to_name[self.position_agent] #the agent doesn't move! 

        if self.color != 0: #if you aren't at the first step
            self.old_color = self.color 
            if self.old_color != self.new_color:
                r = r - 5 #check if platform changed
                self.color = self.new_color
        else:
            self.color = self.new_color #This adds a penalty for platform switching to go on different routes
        
        observations = {'Destination': self.destination, 'Current Station': self.current_station, 'Avaialble Movements': self.reveal_avail_movement(), 'Current Line': self.color}
       
        state = self.position_agent #JIC want to output state instead of obs

        
        #TERMINATION CRITERIA

        if self.current_station == self.destination:
            done = 1
            #self.reward = self.reward + r - 1 + self.N**2 #Experimenting with different reward structures
            self.reward = r -1 + 1000
            self.time_elapsed = self.time_elapsed + 1
            print("Destination has been reached")
        else: 
            done = 0
            self.time_elapsed = self.time_elapsed + 1
            self.reward =  r - 1 #self.reward 
        
        if self.time_elapsed == 50 or len(self.available_pos) == 0:
            done = 1
            print("Environment Terminated")

        return observations, self.reward, done
        #Some reset function where the start position of the agent is randomly assigned again
      #  return state, reward, done
    def reset(self): #doesn't reset closed lines, just agent position
        self.time_elapsed = 0
        self.reward = 0
        self.position_agent = np.random.randint(0, (self.N))
        self.current_station = index_to_name[self.position_agent]
        self.reveal_avail_movement()
        self.sleep = 0
        observations = {'Destination': self.destination, 'Current Station': self.current_station, 'Avaialble Movements': self.reveal_avail_movement(), 'Current Line': self.color}
        state = self.position_agent
        return observations

    def plot_experiments(self, gs,  labels, ema = 0.99): #Borrowed and adapted from Lab 7
    
        for i in range(len(gs)):
            x_hat = 0
            list_x_hat = [] 
            
            for index, value in enumerate(gs[i]):
                
                x_hat =  value* (1 - ema) + x_hat * ema

                list_x_hat.append(x_hat)
            
            plt.plot(list_x_hat, '-', label = ("eps:",labels[i][0],"alpha:",labels[i][1],"gamma:", labels[i][2]))
            plt.legend(bbox_to_anchor=(1.5, 0.5),loc = 'center') 

class SleepyTube(Tube): #A Wrapper for Tube where the agent can fall asleep!

    def __init__(self, G, destination):

            super().__init__(G, destination)

            self.sleep = 0
            
                   


    def step(self,action):

            obs, reward, done = super().step(action) #take a step
            state = self.position_agent
            
            if done == 1:
                return state, self.reward, done, obs
            else:
                proba_sleep = np.random.randint(0,9) #generate a number

                if proba_sleep>2: #0.8 chance of staying awake
                    return state, self.reward, done, obs

                elif proba_sleep <= 1 and self.color != 0 and len(self.available_pos) > 1 and self.sleep == 0 : #if agent is asleep and it is not the first movement!              
                    self.sleep = 1
                    
                    for i in range(0, len(self.available_pos)):
                #look through the avaialble actions and take the one which is the same line which doesn't equal the old station
                #need to loop through available positions and the edge list 
                        for j in range(0, len(self.edge_list)):
                                try:

                                    if self.edge_list[j][0] == self.position_agent and self.edge_list[j][1] == self.available_pos[i]:
                                        if self.edge_list[j][1] != self.old_position: 
                                            if self.edge_list[j][2] == self.color: 
                                                #print(i)
                                                #print(stube.available_pos[i])
                                                #print(stube.available_pos)
                                                #print(stube.edge_list[j][0],stube.position_agent)
                                                #print(stube.edge_list[j][1], stube.available_pos[i]) 
                                            
                                                obs, self.reward, done = super().step(i)
                                                state = self.position_agent
                                                
                                                if done != 1:
                                                    print("The agent has fallen asleep and ended up at " + self.current_station)
    
                                                self.sleep = 0
                                                
                                                self.reward +=1
                                                self.time_elapsed -=1
                                                
                                                return state, self.reward, done, obs
                                except:
                                    self.sleep = 0 
                                    #print("The agent has fallen asleep and ended up at " + self.current_station)
                                    break
                                    return state, self.reward, done, obs
                                    
            
                return state, self.reward, done, obs
                                    
            
                    
    def plot_EMA(self, gs,  labels, ema = 0.99): #borrowed from Lab 7 and adapted
    
        for i in range(len(gs)):
            x_hat = 0
            list_x_hat = [] 
            
            for index, value in enumerate(gs[i]):
                
                x_hat =  value* (1 - ema) + x_hat * ema

                list_x_hat.append(x_hat)
            
            plt.plot(list_x_hat, '-', label = ("eps:",labels[i][0],"alpha:",labels[i][1],"gamma:", labels[i][2]))
            plt.legend(bbox_to_anchor=(1.5, 0.5),loc = 'center')     
            plt.xlabel('Episodes')
            plt.ylabel('Exponential Moving Average Reward')              
    def plot_CUMREW(self, gs, labels): #borrowed from Lab 7 and adapted
        for i in range(len(gs)):
                x_hat = 0
                list_x_hat = [] 
                
                for index, value in enumerate(gs[i]):
                    
                    x_hat =  value + x_hat

                    list_x_hat.append(x_hat)
                
                plt.plot(list_x_hat, '-', label = ("eps:",labels[i][0],"alpha:",labels[i][1],"gamma:", labels[i][2]))
                plt.legend(bbox_to_anchor=(1.5, 0.5),loc = 'center')     
                plt.xlabel('Episodes')
                plt.ylabel('Cumulative Reward') 

    def reset(self):

            super().reset()
            state = self.position_agent

            return state