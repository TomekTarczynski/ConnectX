# Take random action out of all eligable actions
class player_random:
    environment = ConnectX
    
    def __init__(self, name = 'Random'):
        self.name = name
        self.environment_name = 'connectx'
        
    def choose_action(self, observation, configuration):
        from random import choice
        eligable_actions = ConnectX.eligable_actions(observation, configuration)
        return choice(eligable_actions)