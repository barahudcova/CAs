import numpy as np
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation
np.set_printoptions(threshold=sys.maxsize)




#different neighborhood implementations
def neumann(K, i, j):
    m = K.shape[0]
    return(bin_to_dec([K[(i-1)%m,j], K[i, (j-1)%m], K[i, j], K[i, (j+1)%m], K[(i+1)%m, j]]))

def moore(K, i, j):
    m = K.shape[0]
    return(bin_to_dec([K[(i-1)%m, (j-1)%m], K[(i-1)%m, j], K[(i-1)%m, (j+1)%m], 
                K[i, (j-1)%m], K[i, j], K[i, (j+1)%m],
                K[(i+1)%m, (j-1)%m], K[(i+1)%m, j], K[(i+1)%m, (j+1)%m]]))



#helper functions
def bin_to_dec(state):
    total = 0
    for i,j in enumerate(state[::-1]):
        total += j<<i
    return total

def dec_to_bin(num, size):
    return tuple([int(x) for x in np.binary_repr(num, size)])




# an automaton keeps track of the rule, initial condition and an actual state the automaton is in
class Automaton():
    def __init__(self, rule, init):
        self.rule = rule
        self.init = init
        self.state = init  
       
        
    def simulate(self, time):
        l = len(self.state)
        for t in range(time):
            new_state = np.zeros((l,l), dtype=np.int)
            for i in range(l):
                for j in range(l):
                    # znamena to, ze posledni pozice v listu rule odpovida stavu samych (tj. deviti) jednicek
                    new_state[i][j] = self.rule[moore(self.state, i, j)]
            self.state = new_state
            
            
            

# game_of_life rule generation, stored in a list         
def game_of_life():
    game_of_life = []
    for i in range(2**9):
        arr = dec_to_bin(i, 9)
        if arr[4] == 1 and (sum(arr) == 3 or sum(arr) == 4):
            game_of_life.append(1)
        elif arr[4] == 0 and sum(arr) == 3:
            game_of_life.append(1)
        else:
            game_of_life.append(0)
    return game_of_life




# random rule generation, can choose between moore and neumann neighborhood
def random_rule(neighborhood):
    if neighborhood == "moore":
        rule = np.random.randint(2, size=2**(2**9))
    elif neighborhood == "neumann":
        rule = np.random.randint(2, size=2**(2**5))
    return rule




#generate an initial grid configuration; can be padded if zeros, if so, the size of the padding has to be specified
def generate_initial_configuration(grid_size, padding=0):
    initial_config = np.random.randint(2, size=(grid_size, grid_size))
    if padding:
        initial_config = np.pad(initial_config, padding, 'constant', constant_values=0)
    return initial_config




# animation part
def init():
    global initial
    matrice.set_data(initial)
    return state
            
def animate(i):
    global matrice, state, rule
    l = state.shape[0]
    new_state = np.zeros((l,l), dtype=np.int)
    for i in range(l):
        for j in range(l):
            # last element in the rule table corresponds to the input of all ones
            new_state[i][j] = rule[moore(state, i, j)]
    state = new_state
    
    #print(state)
    matrice.set_array(state)
    return state


GRID_SIZE = 100
PADDING = 10

# set up rule and initial configuration
rule = game_of_life()
initial = generate_initial_configuration(GRID_SIZE, PADDING)

# set up animation
state = initial
fig, ax = plt.subplots()
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
matrice = ax.matshow(initial, cmap="binary", aspect="auto")
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=1000, interval=1, repeat=False)
plt.show()   

  
  
  
  
  
  
  
  
  
  