from player import Player

class GameState:

    def __init__(self, input_dict):

        self.dict_to_object(input_dict)

    def dict_to_object(self, input_dict):

        self.player1 = Player(input_dict['p1'])
        self.player2 = Player(input_dict['p2'])
        self.timer = input_dict['timer']
        self.fight_result = input_dict['result']
        self.has_round_started = input_dict['round_started']
        self.is_round_over = input_dict['round_over']

    def object_to_dict(self):
        
        output_dict = {}

        output_dict['p1'] = self.player1.object_to_dict()
        output_dict['p2'] = self.player2.object_to_dict()
        output_dict['timer'] = self.timer
        output_dict['result'] = self.fight_result
        output_dict['round_started'] = self.has_round_started
        output_dict['round_over'] = self.is_round_over

        return output_dict