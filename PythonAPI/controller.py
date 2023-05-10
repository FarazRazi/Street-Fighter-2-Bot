import os
import socket
import json
from game_state import GameState
# from bot import fight
import sys
from bot import Bot

import argparse
import pandas as pd
import src.model as model


def connect(port):
    # For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print("Connected to game!")
    return client_socket


def send(client_socket, command):
    # This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)


def receive(client_socket):
    # receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state


columns = ["timer", "result", "round_started", "round_over", "p1_character", "p1_health", "p1_x", "p1_y", "p1_jumping", "p1_crouching", "p1_in_move", "p1_move", "p1_Up", "p1_Down", "p1_Right", "p1_Left", "p1_Select", "p1_Start", "p1_Y", "p1_B",
           "p1_X", "p1_A", "p1_L", "p1_R", "p2_character", "p2_health", "p2_x", "p2_y", "p2_jumping", "p2_crouching", "p2_in_move", "p2_move", "p2_Up", "p2_Down", "p2_Right", "p2_Left", "p2_Select", "p2_Start", "p2_Y", "p2_B", "p2_X", "p2_A", "p2_L", "p2_R", "player"]


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add the number argument with a default value of 1
    parser.add_argument('number', type=int, help='player number to control')

    # Add the -L argument with a default value of False
    parser.add_argument('-L', '--learning',
                        action='store_true', help='enable learning mode')

    # Add the -R argument with a default value of False
    parser.add_argument('-R', '--random', action='store_true',
                        help='enable random mode')

    # Add argument for file name
    parser.add_argument('-F', '--file', type=str,
                        help='file name to save learning data')

    # Add argument for model name
    parser.add_argument('-M', '--model', type=str,
                        help='Model name to load', choices=['DT'], default='DT')

    # Add argument for model name
    parser.add_argument('-T', '--train', action='store_true',
                        help='enable initial training')

    if (parser.parse_args().train):
        print("Training mode enabled")
        md = model.ModelHandler()
        md.train_model_from_csv("./csvs/learning.csv")

    if (parser.parse_args().file is not None):
        file_name = parser.parse_args().file
    else:
        file_name = "learning"

    # Parse the command-line arguments
    args = parser.parse_args()

    print('Player : ', args.number)

    # args has -L tag then toggle learning mode
    if args.learning:
        print('Learning mode enabled')

    learning = args.learning

    current_game_state = None

    if (args.model is not None and args.random is False):
        print("Model mode enabled : "+args.model+" model")
        model_name = args.model
        bot = Bot(model_name)
        random = False
    else:
        print("Random mode enabled")
        bot = Bot()
        random = True

    if (args.number == 1):
        client_socket = connect(9999)
    elif (args.number == 2):
        client_socket = connect(10000)

    if learning:
        bot.learn("csvs/"+file_name+".csv")
        # create a new csv file
        if not os.path.isfile(bot.file_name):
            temp = pd.DataFrame(columns=columns)
            temp.to_csv(bot.file_name, header=True, index=False)

    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state, args.number, random)
        send(client_socket, bot_command)

    if (learning):
        list = bot.dfs
        bot.dfs = pd.DataFrame(list)

        bot.dfs.to_csv(bot.file_name, header=False, mode='a', index=False)


if __name__ == '__main__':
    main()
