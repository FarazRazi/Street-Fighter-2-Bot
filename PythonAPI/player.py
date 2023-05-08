from buttons import Buttons

class Player:

    def __init__(self, player_dict):
        
        self.dict_to_object(player_dict)
    
    def dict_to_object(self, player_dict):
        
        self.player_id = player_dict['character']
        self.health = player_dict['health']
        self.x_coord = player_dict['x']
        self.y_coord = player_dict['y']
        self.is_jumping = player_dict['jumping']
        self.is_crouching = player_dict['crouching']
        self.player_buttons = Buttons(player_dict['buttons'])
        self.is_player_in_move = player_dict['in_move']
        self.move_id = player_dict['move']

    def object_to_dict(self):
        
        output_dict = {}

        output_dict['character'] = self.player_id
        output_dict['health'] = self.health
        output_dict['x'] = self.x_coord
        output_dict['y'] = self.y_coord
        output_dict['jumping'] = self.is_jumping
        output_dict['crouching'] = self.is_crouching
        output_dict['buttons'] = self.player_buttons.object_to_dict()
        output_dict['in_move'] = self.is_player_in_move
        output_dict['move'] = self.move_id

        return output_dict
