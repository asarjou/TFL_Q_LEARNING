import numpy as np
import matplotlib.pyplot as plt

class Q_LEARNING: 
    def __init__(self, envir, epsilon, decay, alpha, gamma, G1):
        #initialise values
        self.size_environment = envir.N
        self.decay = decay
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha

        self.q_values = -5000 * np.ones((self.size_environment,self.size_environment)) #make impossible movements -5000 so they don't get chosen
        self.value_mat =  np.zeros((self.size_environment,self.size_environment)) #create another copy of the Q_Matrix for visualisation
        for edge in G1.edges:
 
            self.q_values[edge] = 0  #set possible positions
   
    def update_values(self, s_current, a_next, r_next, s_next, a_next_next): 
        
        self.q_values[s_current, a_next] = self.q_values[s_current, a_next] + self.alpha * (r_next + (self.gamma * self.q_values[s_next, a_next_next])) - self.q_values[s_current, a_next] #Q Learning Equation where a_next_next is chosen using target policy

        self.value_mat[s_current, a_next] = self.value_mat[s_current, a_next] + self.alpha * (r_next + (self.gamma * self.value_mat[s_next, a_next_next])) - self.value_mat[s_current, a_next] #for viewing



    def display_values(self):

        plt.imshow(self.value_mat)
        plt.colorbar()
        plt.show()

    def Q_learning_episode(self, E_pol, envir):

        s = envir.reset() #reseet
        done = False
        total_reward = 0
        while not done:
        
            a_next = E_pol(envir, s, self.q_values) #find index of next action
            E_pol.update_epsilon(envir.time_elapsed) #update epsilon
        # print("pos 1: " , envir.available_pos)
            action_next = envir.available_pos[a_next] #take action out of the available pos array
            #print(a_next)available_pos
            #print(action)  
        
            s_next, r, done, _ = envir.step(a_next) #take a step
            #print(r) 

            a_next_next = E_pol.greedy_selection(envir, s_next, self.q_values) #imagine the next step using greedy selection on target policy
            
            action_next_next = envir.available_pos[a_next_next] #find the index of station of next next action
        
                
            self.update_values(s, action_next, r, s_next, action_next_next) #Update the Q Matrix
            
            #print(stube.current_station)
            #print(r)
            
            
            s = s_next #move to next state
            

            total_reward += r
            #print(envir.time_elapsed)
            #print(total_reward)
        return total_reward