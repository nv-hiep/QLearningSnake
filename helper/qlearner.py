import os
import random
import json
import itertools

import dataclasses

from helper.tools import Point

@dataclasses.dataclass
class StateData:
    d_to_apple: tuple
    position: tuple
    env: str
    apple: Point


class QLearning(object):
    def __init__(self, screen_width, screen_height, dot_size):
        # Game parameters
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.dot_size      = dot_size

        # Learning parameters
        self.epsilon  = 0.1
        self.lr       = 0.7
        self.discount = .5

        # State/Action history
        self.qvalues = self.get_qvalues()
        self.history = []

        # Action space
        self.actions = {
            0:'left',
            1:'right',
            2:'up',
            3:'down'
        }

    def reset(self):
        self.history = []

    def load_qvalues(self, path='data/qvalues.json'):
        with open(path, 'r') as f:
            qvalues = json.load(f)
        return qvalues

    

    def save_qvalues(self, path='data/qvalues.json'):
        with open(path, 'w') as f:
            json.dump(self.qvalues, f)
            
    


    def act(self, snake, apple):
        state = self.get_state(snake, apple)

        # Epsilon greedy
        rand = random.uniform(0,1)
        if rand < self.epsilon:
            action_key = random.choices(list(self.actions.keys()))[0]
        else:
            state_scores = self.qvalues[self.state2str(state)]
            action_key = state_scores.index(max(state_scores))
        action_val = self.actions[action_key]
        
        # Remember the actions it took at each state
        self.history.append({
            'state': state,
            'action': action_key
            })
        return action_val
    
    


    def update_qvalues(self, reason):
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            
            # if dead -> penalize
            if reason:
                state     = history[0]['state']
                action    = history[0]['action']
                state_str = self.state2str(state)
                reward    = -1
                self.qvalues[state_str][action] *= (1-self.lr)      # Bellman equation - there is no future state since game is over
                self.qvalues[state_str][action] += self.lr * reward # Bellman equation - there is no future state since game is over
                reason = None
            else:
                current_state = h['state'] # current state
                prev_state    = history[i+1]['state'] # previous state
                prev_action   = history[i+1]['action'] # action taken at previous state
                
                dx0 = prev_state.d_to_apple[0] # x distance_to_apple at previous state
                dy0 = prev_state.d_to_apple[1] # y distance_to_apple at previous state
    
                dx1 = current_state.d_to_apple[0] # x distance_to_apple at current state
                dy1 = current_state.d_to_apple[1] # y distance_to_apple at current state
                
                if prev_state.apple != current_state.apple: # Snake ate a apple, positive reward
                    reward = 1
                elif (abs(dx0) > abs(dx1) or abs(dy0) > abs(dy1)): # Snake is closer to the apple, positive reward
                    reward = 1
                else:
                    reward = -1 # Snake is further from the apple, negative reward
                    
                state_str     = self.state2str(prev_state)
                new_state_str = self.state2str(current_state)
                self.qvalues[state_str][prev_action] *= (1-self.lr)
                self.qvalues[state_str][prev_action] += self.lr * (reward + self.discount*max(self.qvalues[new_state_str])) # Bellman equation


    def get_state(self, snake, apple):
        snake_head = snake[-1]
        dist_x = apple.x - snake_head.x
        dist_y = apple.y - snake_head.y

        if dist_x > 0:
            pos_x = 1 # apple is to the right of the snake
        elif dist_x < 0:
            pos_x = -1 # apple is to the left of the snake
        else:
            pos_x = 0 # apple and snake are on the same X file

        if dist_y > 0:
            pos_y = 1 # apple is below snake
        elif dist_y < 0:
            pos_y = -1 # apple is above snake
        else:
            pos_y = 0 # apple and snake are on the same Y file

        sqs = [ (snake_head.x-self.dot_size, snake_head.y),
                (snake_head.x+self.dot_size, snake_head.y),
                (snake_head.x, snake_head.y-self.dot_size),
                (snake_head.x, snake_head.y+self.dot_size) ]
        
        env = ''
        for sq in sqs:
            if sq[0] < 0 or sq[1] < 0: # off screen left or top
                env += '1'
            elif sq[0] >= self.screen_width or sq[1] >= self.screen_height: # off screen right or bottom
                env += '1'
            elif sq in snake[:-1]: # part of tail, note snake[-1] is head
                env += '1'
            else:
                env += '0'

        return StateData((dist_x, dist_y), (pos_x, pos_y), env, apple)

    def state2str(self, state):
        return str(state.position[0]) + ',' + str(state.position[1]) + state.env

    def init_qvalues(self):
        q = {}
        for xi in [-1, 0, 1]:
            for yi in [-1, 0, 1]:
                for envi in [''.join(s) for s in list( itertools.product('01', repeat = 4) )]:
                    q[str(xi) + ',' + str(yi) + envi ] = [0.]*4
        return q

    def get_qvalues(self):
        if os.path.isfile('data/qvalues.json'):
            return self.load_qvalues()
        else:
            return self.init_qvalues()