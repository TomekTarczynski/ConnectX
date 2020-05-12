# If agent can win in next move then it chooses it.
# If opponent can win in next move then agent blocks it.    
# Otherwise agent choose random move.
class player_simple1:
    environment = ConnectX
    
    def __init__(self, name = 'Simple1'):
        self.name = name
        self.environment_name = 'connectx'
        
    def choose_action(self, observation, configuration):
        from random import choice
        eligable_actions = ConnectX.eligable_actions(observation, configuration)
        for action in eligable_actions:
            if ConnectX.is_win(observation, configuration, action, observation['mark'], has_played = False):
                return(action)
        for action in eligable_actions:
            if ConnectX.is_win(observation, configuration, action, 3 - observation['mark'], has_played = False):
                return(action)    
        return choice(eligable_actions)
