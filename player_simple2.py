# If agent can win in next move then it chooses it.
# If opponent can win in next move then agent blocks it.    
# Otherwise agent choose random move.
class player_simple2:
    environment = ConnectX
    
    def __init__(self, name = 'Simple2'):
        self.name = name
        self.environment_name = 'connectx'
        
    def is_possible_win(self, observation, configuration, row, column, offset_row, offset_column):
        board = observation['board']
        mark = observation['mark']
        inarow = configuration['inarow']
        result = 0
        for i in range(0, inarow):
            r = row + offset_row * i
            c = column + offset_column * i
            if (
                r < 0
                or r >= configuration.rows
                or c < 0
                or c >= configuration.columns
                or board[c + (r * configuration.columns)] == 3 - mark
            ):
                return 0
            else:
                result += 1 if board[c + (r * configuration.columns)] == mark else 0
        return result * result

    def evaluate(self, observation, configuration, row, col):
        result = 0
        result += self.is_possible_win(observation, configuration, row, col, 1, 0)
        result += self.is_possible_win(observation, configuration, row, col, -1, 0)
        result += self.is_possible_win(observation, configuration, row, col, 0, 1)
        result += self.is_possible_win(observation, configuration, row, col, 0, -1)
        result += self.is_possible_win(observation, configuration, row, col, 1, 1)
        result += self.is_possible_win(observation, configuration, row, col, -1, -1)
        result += self.is_possible_win(observation, configuration, row, col, 1, -1)
        result += self.is_possible_win(observation, configuration, row, col, -1, 1)
        return(result)
    
    def evaluate_board(self, observation, configuration):
        result = 0 
        for col in range(configuration.columns):
            for row in range(configuration.rows):
                result += self.evaluate(observation, configuration, row, col)
        return(result)
        
    def choose_action(self, observation, configuration):
        from random import choice
        
        mark = observation['mark']
        mark_opponent = 3 - mark
        eligable_actions = ConnectX.eligable_actions(observation, configuration)
        inarow = configuration.inarow - 1
        
        for action in eligable_actions:
            if ConnectX.is_win(observation, configuration, action, observation['mark'], has_played = False):
                return(action)
        for action in eligable_actions:
            if ConnectX.is_win(observation, configuration, action, 3 - observation['mark'], has_played = False):
                return(action)    
        
        best_action = eligable_actions[0]
        best_result = -1000
        for action in eligable_actions:  
            result = 0
            new_observation = {'board': observation['board'][:], 'mark': mark}
            ConnectX.play_action(new_observation, configuration, action)
            result += self.evaluate_board(new_observation, configuration)
            new_observation['mark'] = 3 - new_observation['mark']
            result -= self.evaluate_board(new_observation, configuration)                
            if result > best_result:
                best_action = action
                best_result = result
        return(best_action)
