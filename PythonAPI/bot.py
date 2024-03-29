from command import Command
import numpy as np
import pandas as pd
from buttons import Buttons
from src.model import ModelHandler
from src.preprocessing import preProcessAndGetXy


class Bot:

    def __init__(self, model_name=None):
        # < - v + < - v - v + > - > + Y
        self.fire_code = ["<", "!<", "v+<", "!v+!<",
                          "v", "!v", "v+>", "!v+!>", ">+Y", "!>+!Y"]
        self.exe_code = 0
        self.start_fire = True
        self.remaining_code = []
        self.my_command = Command()
        self.buttn = Buttons()
        self.prev = 0
        self.learning = False
        self.modelHandler = ModelHandler(model_name)
        self.actions = []
        self.framesCount = 0

    def learn(self, file_name):
        self.file_name = file_name
        self.learning = True
        # list of dataframes
        self.dfs = []

    def convert_to_obj(self, current_game_state, player):
        # make a dataframe from the current game state

        # get obj from the game state
        obj = current_game_state.object_to_dict()

        # save p1 and p2 as separate rows
        p1 = obj['p1']
        # name the columns with p1 prefix
        p1 = {f'p1_{k}': v for k, v in p1.items()}

        p2 = obj['p2']
        # name the columns with p2 prefix
        p2 = {f'p2_{k}': v for k, v in p2.items()}

        # get buttons from p1 and p2
        p1_buttons = p1['p1_buttons']
        # name the buttons with p1 prefix
        p1_buttons = {f'p1_{k}': v for k, v in p1_buttons.items()}

        p2_buttons = p2['p2_buttons']
        # name the buttons with p2 prefix
        p2_buttons = {f'p2_{k}': v for k, v in p2_buttons.items()}

        # remove buttons from p1 and p2
        del p1['p1_buttons']
        del p2['p2_buttons']

        # add all buttons to p1 and p2
        p1.update(p1_buttons)
        p2.update(p2_buttons)

        # remove p1 and p2 from the obj
        del obj['p2']
        del obj['p1']

        # add all p1 and p2 columns to the obj
        obj.update(p1)
        obj.update(p2)

        # add new attributes to the obj
        obj['player'] = player

        return obj

    def save(self, current_game_state, player):
        # print(obj)
        obj = self.convert_to_obj(current_game_state, player)
        # append the dataframe to the dfs list
        self.dfs.append(obj)

    def encodeAction(self, actions):
        # action are list of buttons pressed
        # [[0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]]
        # 'player_Up', 'player_Down', 'player_Right', 'player_Left', 'player_Y', 'player_B', 'player_X', 'player_A', 'player_L', 'player_R'
        # '^', 'v', '>', '<', 'Y', 'B', 'X', 'A', 'L', 'R'

        # convert the action to symbols list
        # print(actions)
        symbols = []
        pressed = []
        for action in actions:
            added = False
            symbol = ""

            for i in range(len(action)):
                remove = True
                # if pressed has move and in next action it is not present
                # add '!' to the current move
                # remove from pressed
                if action[i] != 0:
                    if added:
                        symbol += "+"

                if i in pressed and action[i] == 0:
                    if added:
                        symbol += "+"
                    symbol += "!"
                    action[i] = 1
                    pressed.remove(i)
                    remove = False

                if action[i] != 0:
                    if i == 0:
                        symbol += "^"
                    elif i == 1:
                        symbol += "v"
                    elif i == 2:
                        symbol += ">"
                    elif i == 3:
                        symbol += "<"
                    elif i == 4:
                        symbol += "Y"
                    elif i == 5:
                        symbol += "B"
                    elif i == 6:
                        symbol += "X"
                    elif i == 7:
                        symbol += "A"
                    elif i == 8:
                        symbol += "L"
                    elif i == 9:
                        symbol += "R"
                    added = True
                    if i not in pressed and remove:
                        pressed.append(i)
            if symbol == "":
                symbol = "-"

            symbols.append(symbol)
        return symbols

    def playRandom(self, current_game_state, player):
        # python Videos\gamebot-competition-master\PythonAPI\controller.py 1
        if player == 1:
            # print("1")
            # v - < + v - < + B spinning
            if (self.exe_code != 0):
                self.run_command([], current_game_state.player1)
            diff = current_game_state.player2.x_coord - current_game_state.player1.x_coord
            if (diff > 60):
                toss = np.random.randint(6)
                if (toss == 0):
                    # self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player1)
                    self.run_command([">", "-", "!>", "v+>", "-", "!v+!>", "v", "-", "!v",
                                     "v+<", "-", "!v+!<", "<+Y", "-", "!<+!Y"], current_game_state.player1)
                elif (toss == 1):
                    self.run_command(
                        [">+^+B", ">+^+B", "!>+!^+!B"], current_game_state.player1)
                elif (toss == 2):
                    self.run_command(["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v",
                                     "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"], current_game_state.player2)
                else:
                    if (diff < 0):
                        self.run_command(["<", "<", "!<"],
                                         current_game_state.player2)
                    else:
                        self.run_command([">", ">", "!>"],
                                         current_game_state.player2)
            elif (diff < -60):
                toss = np.random.randint(6)
                if (toss == 0):  # spinning
                    # self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player1)
                    self.run_command(["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v",
                                     "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"], current_game_state.player1)
                elif (toss == 1):
                    self.run_command(
                        ["<+^+B", "<+^+B", "!<+!^+!B"], current_game_state.player1)
                elif (toss == 2):
                    self.run_command(["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v",
                                     "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"], current_game_state.player2)
                else:
                    if (diff < 0):
                        self.run_command(["<", "<", "!<"],
                                         current_game_state.player2)
                    else:
                        self.run_command([">", ">", "!>"],
                                         current_game_state.player2)
            else:
                toss = np.random.randint(5)
                if (toss >= 1):
                    if (diff > 0):
                        self.run_command(["<", "<", "!<"],
                                         current_game_state.player1)
                    else:
                        self.run_command([">", ">", "!>"],
                                         current_game_state.player1)
                else:
                    self.run_command(["v+R", "v+R", "v+R", "!v+!R"],
                                     current_game_state.player1)
            self.my_command.player_buttons = self.buttn

        elif player == 2:

            if (self.exe_code != 0):
                self.run_command([], current_game_state.player2)
            diff = current_game_state.player1.x_coord - current_game_state.player2.x_coord
            if (diff > 60):
                toss = np.random.randint(6)
                if (toss == 0):
                    # self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player2)
                    self.run_command([">", "-", "!>", "v+>", "-", "!v+!>", "v", "-", "!v",
                                     "v+<", "-", "!v+!<", "<+Y", "-", "!<+!Y"], current_game_state.player2)
                elif (toss == 1):
                    self.run_command(
                        [">+^+B", ">+^+B", "!>+!^+!B"], current_game_state.player2)
                elif (toss == 2):
                    self.run_command(["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v",
                                     "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"], current_game_state.player2)
                else:
                    if (diff > 0):
                        self.run_command(["<", "<", "!<"],
                                         current_game_state.player2)
                    else:
                        self.run_command([">", ">", "!>"],
                                         current_game_state.player2)
            elif (diff < -60):
                toss = np.random.randint(6)
                if (toss == 0):
                    # self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player2)
                    self.run_command(["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v",
                                     "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"], current_game_state.player2)
                elif (toss == 1):
                    self.run_command(
                        ["<+^+B", "<+^+B", "!<+!^+!B"], current_game_state.player2)
                elif (toss == 2):
                    self.run_command([">", "-", "!>", "v+>", "-", "!v+!>", "v", "-", "!v",
                                     "v+<", "-", "!v+!<", "<+Y", "-", "!<+!Y"], current_game_state.player2)
                else:
                    if (diff > 0):
                        self.run_command(["<", "<", "!<"],
                                         current_game_state.player2)
                    else:
                        self.run_command([">", ">", "!>"],
                                         current_game_state.player2)
            else:
                # anyFightActionIsTrue(current_game_state.player2.player_buttons)
                toss = np.random.randint(5)
                if (toss >= 1):
                    if (diff < 0):
                        self.run_command(["<", "<", "!<"],
                                         current_game_state.player2)
                    else:
                        self.run_command([">", ">", "!>"],
                                         current_game_state.player2)
                else:
                    self.run_command(
                        ["v+R", "v+R", "v+R", "!v+!R"], current_game_state.player2)
            self.my_command.player2_buttons = self.buttn

        # if game is in play and learning is on, save the current game state
        # after every second
        # curr = current_game_state.timer
        # if (current_game_state.is_round_over == False and self.learning == True):
        #     if (curr != self.prev):
        #         self.save(current_game_state)
        #         self.prev = curr

        # after every frame
    def combineFrames(self, current_game_state, player):
        # print(obj)
        obj = self.convert_to_obj(current_game_state, player)
        # append the dataframe to the dfs list
        self.actions.append(obj)

    def playModel(self, current_game_state, player):
        if (self.exe_code != 0):
            self.run_command([], current_game_state.player2)

        self.framesCount += 1

        if self.framesCount >= 100:
            self.playRandom(current_game_state, player)
            self.framesCount = 0
            return

        self.combineFrames(current_game_state, player)

        if self.framesCount % np.random.randint(1, 9) == 0:

            # obj = self.convert_to_obj(current_game_state, player)

            # convert the obj to a DataFrame
            df = pd.DataFrame(self.actions)

            # print(df)

            # preprocess the dataframe
            X, y = preProcessAndGetXy(df)

            if X is None:
                print("No Data")
                return

            # predict the action
            action = self.modelHandler.predict_DT_CLF(X)

            # print(action)

            # endecode the action
            action = self.encodeAction(action)

            # print(action)

            # run the action
            if player == 1:
                self.run_command(action, current_game_state.player1)
                self.my_command.player_buttons = self.buttn
            elif player == 2:
                self.run_command(action, current_game_state.player2)
                self.my_command.player2_buttons = self.buttn

            if self.framesCount % 9 == 0:
                self.buttn = Buttons()

            # if action has "-" increase the frames count
            if action[0] == "-":
                self.framesCount += 6

            self.actions = []

    def fight(self, current_game_state, player, random):

        if random:
            self.playRandom(current_game_state, player)
        else:
            self.playModel(current_game_state, player)

        # if game is in play and learning is on, save the current game state
        # after every second
        # curr = current_game_state.timer
        # if (current_game_state.is_round_over == False and self.learning == True):
        #     if (curr != self.prev):
        #         self.save(current_game_state)
        #         self.prev = curr

        # after every frame
        if (current_game_state.is_round_over == False and self.learning == True):
            self.save(current_game_state, player)

        return self.my_command

    def run_command(self, com, player):
        button_mapping = {
            "^": ("up", True),
            "!^": ("up", False),
            "v": ("down", True),
            "!v": ("down", False),
            ">": ("right", True),
            "!>": ("right", False),
            "<": ("left", True),
            "!<": ("left", False),
            "Y": ("Y", not player.player_buttons.Y),
            "!Y": ("Y", False),
            "B": ("B", not player.player_buttons.B),
            "!B": ("B", False),
            "X": ("X", not player.player_buttons.X),
            "!X": ("X", False),
            "A": ("A", not player.player_buttons.A),
            "!A": ("A", False),
            "L": ("L", not player.player_buttons.L),
            "!L": ("L", False),
            "R": ("R", not player.player_buttons.R),
            "!R": ("R", False),
        }

        print(com)

        if len(self.remaining_code) == 0:
            self.fire_code = com
            self.exe_code += 1
            self.remaining_code = self.fire_code[0:]
        elif self.exe_code - 1 == len(self.fire_code):
            self.exe_code = 0
            self.start_fire = False
            # print("complete")
        else:
            self.exe_code += 1
            command = self.remaining_code[0]
            if command != "-":
                for symbol in command.split("+"):
                    button, status = button_mapping[symbol]
                    setattr(self.buttn, button, status)

            self.remaining_code = self.remaining_code[1:]

        return
