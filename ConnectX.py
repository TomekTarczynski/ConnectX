import gym
import kaggle_environments as ke
import numpy as np
import pandas as pd
from tabulate import tabulate
import time

now = time.perf_counter()
for i in range(10000):
    now2 = time.perf_counter()
now2 - now

EMPTY = 0

class ConnectX(gym.Env):
    def __init__(self, configuration = {}, debug = True):
        self.env = ke.make('connectx', configuration = configuration, debug = debug)
        
        # Define required gym fields (examples):
        self.configuration = self.env.configuration
        self.action_space = gym.spaces.Discrete(self.configuration.columns)
        self.observation_space = gym.spaces.MultiDiscrete([3] * self.configuration.columns * self.configuration.rows)

    def step(self, action):
        return self.env.step(action)
    
    def reset(self):
        return self.env.reset()
    
    def render(self, **kwargs):
        return self.env.render(**kwargs)
    
    def run(self, players, output_format = 'np'):
        def choose_action_1(observation, configuration):
            return players[0].choose_action(observation, configuration)
        
        def choose_action_2(observation, configuration):
            return players[1].choose_action(observation, configuration)  
        
        obs = self.env.run([choose_action_1, choose_action_2])
        if output_format == 'np':
            output = {
                'action': np.array([obs[i][1 - i % 2]['action'] for i in range(1, len(obs))]),
                'board': np.array([obs[i][0]['observation']['board'] for i in range(0, len(obs) - 1)]),
                'mark': np.array([2 - i % 2 for i in range(1, len(obs))]),
                'reward_1': np.array([obs[i][0]['reward'] for i in range(1, len(obs))]),
                'reward_2': np.array([obs[i][1]['reward'] for i in range(1, len(obs))]),
                'player_1': players[0].name,
                'player_2': players[1].name}
            return output
        if output_format == 'original':
            return obs
    
    @staticmethod
    def eligable_actions(observation, configuration):
        return([c for c in range(configuration.columns) if observation['board'][c] == 0])
    
    @staticmethod
    def play_action(observation, configuration, action):
        columns = configuration.columns
        rows = configuration.rows
        row = max([r for r in range(rows) if observation['board'][action + (r * columns)] == EMPTY])
        observation['board'][action + (row * columns)] = observation['mark']   
    
    @staticmethod        
    def is_win(observation, configuration, action, mark, has_played = True):
        columns = configuration.columns
        rows = configuration.rows
        inarow = configuration.inarow - 1
        row = (
            min([r for r in range(rows) if observation['board'][action + (r * columns)] == mark])
            if has_played
            else max([r for r in range(rows) if observation['board'][action + (r * columns)] == EMPTY])
        )
    
        def count(offset_row, offset_column):
            for i in range(1, inarow + 1):
                r = row + offset_row * i
                c = action + offset_column * i
                if (
                    r < 0
                    or r >= rows
                    or c < 0
                    or c >= columns
                    or observation['board'][c + (r * columns)] != mark
                ):
                    return i - 1
            return inarow
    
        return (
            count(1, 0) >= inarow  # vertical.
            or (count(0, 1) + count(0, -1)) >= inarow  # horizontal.
            or (count(-1, -1) + count(1, 1)) >= inarow  # top left diagonal.
            or (count(-1, 1) + count(1, -1)) >= inarow  # top right diagonal.
            )
    
    @staticmethod
    def render_np(episode_np):
        env = ke.make('connectx')
        env.reset()
        for i in range(len(episode_np['action'])):
            if i % 2 == 0:
                actions = [int(episode_np['action'][i]), 0]
            else:
                actions = [0, int(episode_np['action'][i])]
        env.render(mode="ipython", width=500, height=450)

    
comp = competition(n_episodes = 30)    
p_random = player_random()
p_simple2 = player_simple2()
p_simple1 = player_simple1()    
p_negamax = player_negamax()   
comp.add_player(p_random)
comp.add_player(p_simple1)
comp.add_player(p_simple2)
comp.add_player(p_negamax)
tbl = comp.table()
print(tabulate(tbl, headers='keys', tablefmt='psql', showindex = False))

game = ConnectX()

#game.run([p_simple2, p_simple1])

result2 = evaluate([p_simple1, p_simple2], n_episodes = 100)
result3 = evaluate([p_random, p_simple2], n_episodes = 100)
result = simulation([p_random, p_simple1])


obs = game.reset()


result = simulation([p1, p2])
res = game.run([p1, p2])
ConnectX.render_np(res)


game = ConnectX()
p_simple2 = player_simple2()
status = game.reset()
obs = status[0]['observation']
conf = game.configuration
ConnectX.play_action(obs, conf, 0)
ConnectX.play_action(obs, conf, 1)
obs['mark'] = 2
ConnectX.play_action(obs, conf, 2)
obs['mark'] = 1
#p_simple2.is_possible_win(obs, conf, 5, 0, 0, 1)
#p_simple2.evaluate(obs, conf, 5, 0)
p_simple2.evaluate_board(obs, conf)






    



res = game.run([my_agent2, my_agent])
print(len(res))
env.render(mode="ipython", width=500, height=450)

res2 = {
  'action': np.array([res[i][1 - i % 2]['action'] for i in range(1, len(res))]),
  'board': np.array([res[i][0]['observation']['board'] for i in range(0, len(res) - 1)]),
  'mark': np.array([2 - i % 2 for i in range(1, len(res))]),
  'reward_1': np.array([res[i][0]['reward'] for i in range(1, len(res))]),
  'reward_2': np.array([res[i][1]['reward'] for i in range(1, len(res))])}

res2  = [0] * len(action)
for i in range(len(res2)):
    res2[i] = {}
    res2[i]['action'] = action[i]
    res2[i]['board'] = board[i]
    res2[i]['mark'] = mark[i]
    res2[i]['reward_1'] = reward_1[i]
    res2[i]['reward_2'] = reward_2[i]

trainer = env.train([None, my_agent])

observation = trainer.reset()

while not env.done:
    my_action = my_agent2(observation, env.configuration)
    print("My Action", my_action)
    observation, reward, done, info = trainer.step(my_action)
    env.render()
print("Reward", reward)



def mean_reward(rewards):
    return sum(r[0] for r in rewards) / float(len(rewards))
print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", ["negamax", my_agent2], num_episodes=10)))
print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [my_agent2, "negamax"], num_episodes=10)))


print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [my_agent, "random"], num_episodes=100)))
print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", ["random", my_agent], num_episodes=100)))

print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [my_agent2, "random"], num_episodes=100)))
print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", ["random", my_agent2], num_episodes=100)))

print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [my_agent2, my_agent], num_episodes=100)))
print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [my_agent, my_agent2], num_episodes=100)))



ConnectX.eligable_moves(obs[0]['observation']['board'], game.configuration)

obs = game.step([2, 125])
game.render()    
game.step([152, 1])
game.render()   




import inspect
import os

print(inspect.getsource(env.agents["negamax"].__globals__["play"]))
print(inspect.getsource(ke.utils.Struct))

xxx = ke.utils.Struct()