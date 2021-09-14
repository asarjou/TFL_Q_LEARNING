import numpy as np 
import random
class E_greedy_policy():
    
    def __init__(self, envir, epsilon, decay):
        self.epsilon = epsilon
        self.decay = decay 
        self.epsilon_init = self.epsilon
       
    def __call__(self, envir, state, q_values):
        
          if random.random() < self.epsilon: #if value greater than epsilon

          
            action = np.random.randint(0,len(envir.available_pos)) #random movement
            return action
          #

          else:
            action = E_greedy_policy.greedy_selection(self, envir, state, q_values) #otherwise act greedily
           
            return action #return the action!
          

    def greedy_selection(self, envir, state, q_values):
      
      best_action_index = np.argmax(q_values[state]) #Find the index (destination station) of the max q_value for the state that the agent is in
            #print(best_action_index)
      for idx, val in enumerate(envir.available_pos): #loop through the available positions 
            # print(val)
            #  print(best_action_index)
        if best_action_index == val: #if the station of the best action has the same value as one of the avaiable movements 
                #print(action)

          a = idx #action is the index of the available position
          return a
          
    def update_epsilon(self, timestep): 
        if timestep % 3: 

          self.epsilon = self.epsilon * (1-self.decay)

    def reset(self): 
        self.epsilon = self.epsilon_init