import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        self.trial_num = 1

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        #self.epsilon = self.epsilon - 0.005
        #print "self.trial_num",[self.epsilon,self.trial_num,math.log(100.0/(self.trial_num+1)),math.log(100.0/self.trial_num)]
        if self.epsilon>0.0:
            nr = 10000.0
            self.epsilon = self.epsilon * math.log(nr/(self.trial_num+1))/math.log(nr/self.trial_num)
        else:
            self.epsilon=0.0
        """
        if self.alpha>0.3:
            self.alpha=self.alpha-0.05
        else:
            self.alpha=0.3
            
        """
        self.alpha = self.epsilon + 0.2
        if self.alpha>1.0:
            self.alpha = 1.0
        self.trial_num = self.trial_num + 1
        if testing == True:
            self.epsilon = 0.0
            self.alpha = 0.0
        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        
        # NOTE : you are not allowed to engineer eatures outside of the inputs available.
        # Because the aim of this project is to teach Reinforcement Learning, we have placed 
        # constraints in order for you to learn how to adjust epsilon and alpha, and thus learn about the balance between exploration and exploitation.
        # With the hand-engineered features, this learning process gets entirely negated.
        
        # Set 'state' as a tuple of relevant data for the agent        
        #state = None
        #state={'waypoint':waypoint,'light':inputs['light'],'oncoming':inputs['oncoming'], 'left':inputs['left'] }
        state=(waypoint,inputs['light'], inputs['oncoming'], inputs['left'],inputs['right'] ) 

        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        maxQ = None
        if state in Q:
            actions_dict = Q[state]
        """
        for action, value in actions_dict.iteritems():
                if maxQ==None:
                    maxQ=(value,action)
                elif value>maxQ[0]:
                    maxQ=(value,action)
                elif value<maxQ[0]:
                    pass
                elif value==maxQ[0]:
                    maxQ.add(action)
        """
        for action,value in actions_dict.iteritems():
            if not maxQ:
                maxQ=value
            elif maxQ<value:
                maxQ=value
        return maxQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        if state not in self.Q:
            self.Q[state]={
                    "left": 0.0,
                    "right":0.0,
                    "forward":0.0,
                    None:0.0
                }
            self.Q[state][state[0]]=1.0
        return self.Q


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """
        
        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None
        """action_id = random.randint(0,3)
        action  = self.valid_actions[action_id]
        current_input = self.env.sense(self)
        light_state = current_input['light']
        action =  self.next_waypoint
        print {'light_state':light_state,'self.next_waypoint':self.next_waypoint,'action':action, 'left':current_input['left'] , 'oncoming':current_input['oncoming'],'right':current_input['right']}
        if light_state != 'green':
            if self.next_waypoint != 'right':
                action = None
            else:
                if current_input['left'] == 'forward' or current_input['oncoming'] == 'left':
                    action = None
                else:
                    action =self.next_waypoint
        if light_state == 'green':
            if self.next_waypoint != 'left':
                action = self.next_waypoint
            elif current_input['oncoming']=='forward':
                action = None
#        action_id = random.randint(0,3)
#        action  = self.valid_actions[action_id]
#        print "action:",action,action_id
        """
        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        # Otherwise, choose an action with the highest Q-value for the current state
        # Be sure that when choosing an action with highest Q-value that you randomly select between actions that "tie".
        if random.uniform(0, 1)<self.epsilon:
            return random.choice(self.env.valid_actions)
        if not self.learning:
            return random.choice(self.env.valid_actions)
        
        maxQ=None
        for action,value in self.Q[state].iteritems():
            if not maxQ:
                maxQ = [value,action]
            elif maxQ[0]==value:
                maxQ.append(action)
            elif maxQ[0]<value:
                maxQ = [value,action]
        
        action_to_return =  random.choice(maxQ[1:])
        """if action_to_return==None:
            action_to_return = None"""
        return action_to_return


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives a reward. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        if self.learning:
            self.Q[state][action]=self.alpha*reward +(1-self.alpha)*self.Q[state][action]
        return True


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        #print "taking action:",action,type(action)
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent,learning=True,epsilon=0.8,alpha=0.8)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent,enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    #sim = Simulator(env,update_delay=1,display=True,log_metrics=True)
    sim = Simulator(env,update_delay=0,display=False,log_metrics=True,optimized=True)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=50)


if __name__ == '__main__':
    run()
