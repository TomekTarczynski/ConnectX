# Take random action out of all eligable actions
class player_negamax:
    environment = ConnectX
    
    def __init__(self, name = 'Negamax'):
        self.name = name
        self.environment_name = 'connectx'
        env = ke.make('connectx')
        self.choose_action = env.agents.negamax