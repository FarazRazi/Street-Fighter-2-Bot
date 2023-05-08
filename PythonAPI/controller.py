import socket
import json
from game_state import GameState
#from bot import fight
import sys
from bot import Bot

import argparse
import pandas as pd

def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add the number argument with a default value of 1
    parser.add_argument('number', type=int, help='player number to control')

    # Add the -L argument with a default value of False
    parser.add_argument('-L', '--learning', action='store_true', help='enable learning mode')

    # Add the -R argument with a default value of False
    parser.add_argument('-R', '--random', action='store_true', help='enable random mode')

    # Parse the command-line arguments
    args = parser.parse_args()

    print('Player : ', args.number)

    if (args.number==1):
        client_socket = connect(9999)
    elif (args.number==2):
        client_socket = connect(10000)


    # args has -L tag then toggle learning mode
    learning = args.learning
    
    # args has -R tag then toggle random mode
    # random = args.random
    random = True


    current_game_state = None
    #print( current_game_state.is_round_over )
    bot=Bot()

    if learning:
        bot.learn("csvs/learning.csv")
        
    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state, args.number, random)
        send(client_socket, bot_command)
    
    if ( learning ):
        list = bot.dfs
        bot.dfs = pd.DataFrame(list)

        # read first row of csv
        df = pd.read_csv(bot.file_name, nrows=1)
        # if first column is not 'timer' then add header = True
        header = False
        if ( df.columns[0] != 'timer' ):
            header = True

        bot.dfs.to_csv(bot.file_name, mode='a', header=header, index=False)
    
if __name__ == '__main__':
   main()
