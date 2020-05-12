from kaggle_environments import evaluate, make, utils

env = make("connectx", debug=True)
env.render()

# This agent random chooses a non-empty column.
def my_agent(observation, configuration):
    from random import choice
    print(observation)
    return choice([c for c in range(configuration.columns) if observation.board[c] == 0])


env.reset()
# Play as the first agent against default "random" agent.
xxx = env.run([my_agent, "random"])

# Works only in Jupyter
env.render(mode="ipython", width=500, height=450)
env.play([None, "negamax"], width=500, height=450)


# Play as first position against random agent.
trainer = env.train([None, "random"])

observation = trainer.reset()

while not env.done:
    my_action = my_agent(observation, env.configuration)
    print("My Action", my_action)
    observation, reward, done, info = trainer.step(my_action)
    # env.render(mode="ipython", width=100, height=90, header=False, controls=False)
env.render()




def mean_reward(rewards):
    return sum(r[0] for r in rewards) / float(len(rewards))

# Run multiple episodes to estimate its performance.
print("My Agent vs Random Agent:", mean_reward(evaluate("connectx", [my_agent, "random"], num_episodes=1000)))
print("My Agent vs Negamax Agent:", mean_reward(evaluate("connectx", [my_agent, "negamax"], num_episodes=10)))


import inspect
import os


os.chdir('E:\\Projects\\04_ConnectX')

def write_agent_to_file(function, file):
    with open(file, "a" if os.path.exists(file) else "w") as f:
        f.write(inspect.getsource(function))
        print(function, "written to", file)

write_agent_to_file(my_agent, "submission.py")

import sys
out = sys.stdout
submission = utils.read_file("submission2.py")
agent = utils.get_last_callable(submission)
sys.stdout = out

env = make("connectx", debug=True)
env.run([agent, agent])
print("Success!" if env.state[0].status == env.state[1].status == "DONE" else "Failed...")

