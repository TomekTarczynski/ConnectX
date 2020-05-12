def simulation(players, shuffle_players = "switch", n_episodes = 10, output_format = 'np'):
    if len(players) != 2:
        raise Exception('Number of players different than two.')
    if players[0].environment != players[1].environment:
        raise Exception('Players have different environment.')
    if players[0].name == players[1].name:
        raise Exception('Players must have different names.')
    game = players[0].environment()
    result = []
    for i in range(n_episodes):
        result += [game.run(players, output_format = output_format)]
        if shuffle_players == "switch":
            players = players[::-1]
    return(result)

def evaluate(players, shuffle_players = "switch", n_episodes = 10):
    result = simulation(players, shuffle_players, n_episodes, output_format = 'np')
    result_dict = {
        players[0].name: np.array([np.sum(r['reward_1']) if r['player_1'] == players[0].name else np.sum(r['reward_2']) for r in result]),
        players[1].name: np.array([np.sum(r['reward_1']) if r['player_1'] == players[1].name else np.sum(r['reward_2']) for r in result]),
        'player_1': [r['player_1'] for r in result],
        'player_2': [r['player_2'] for r in result]}
    return(result_dict)


class competition:
    def __init__(self, n_episodes):
        self.n_episodes = n_episodes
        self.players = {}
        self.results = []
        
    def add_player(self, player):
        if player.name in self.players.keys():
            raise Exception('Player {} already in competition'.format(player.name))
        self.players[player.name] = {}
        self.players[player.name]['player'] = player
        self.players[player.name]['games'] = 0
        self.players[player.name]['reward'] = 0
        if len(self.players.keys()) > 1:
            for p in self.players.keys():
                if p != player.name:
                    self.evaluate(player.name, p)

    def evaluate(self, player_1_name, player_2_name):
        result = evaluate([self.players[player_1_name]['player'], self.players[player_2_name]['player']], n_episodes = self.n_episodes)
        self.players[player_1_name]['games'] += self.n_episodes
        self.players[player_1_name]['reward'] += np.sum(result[player_1_name])
        self.players[player_2_name]['games'] += self.n_episodes
        self.players[player_2_name]['reward'] += np.sum(result[player_2_name])
        self.results += result
        
    def table(self):
        player_names = list(self.players.keys())
        games = [self.players[p]['games'] for p in player_names]
        reward = [self.players[p]['reward'] for p in player_names]
        df = pd.DataFrame({'player': player_names, 'games': games, 'reward': reward})
        df['avg_reward'] = round(df['reward'] / df['games'], 3)
        df = df.sort_values(by=['avg_reward'], ascending = False)
        return(df)