import pandas as pd
import numpy as np


def readData(path):
    df = pd.read_csv(path)
    return df


def preProcessData(df):

    # remove rows where round_started is False
    df = df[df['round_started'] == True]

    # remove extra columns
    df = df.drop(['result', 'round_started', 'round_over',
                  'p1_Select', 'p1_Start', 'p2_Select', 'p2_Start'], axis=1)

    # if df is empty return empty df
    if df.empty:
        return df

    # get player in control
    # get first row in player column
    # convert to int
    player = df.iloc[0:1, df.columns.get_loc('player')].astype(int).values[0]

    if player == 1:
        # rename p1 to opponent and p2 to player
        df = df.rename(columns={'p1_character': 'opponent_character', 'p1_jumping': 'opponent_jumping', 'p1_crouching': 'opponent_crouching', 'p1_in_move': 'opponent_in_move', 'p1_x': 'opponent_x', 'p1_y': 'opponent_y',
                                'p1_health': 'opponent_health', 'p2_character': 'player_character', 'p2_jumping': 'player_jumping', 'p2_crouching': 'player_crouching', 'p2_in_move': 'player_in_move', 'p2_x': 'player_x', 'p2_y': 'player_y', 'p2_health': 'player_health'})
        # rename all moves columns
        df = df.rename(columns={'p1_Up': 'opponent_Up', 'p1_Down': 'opponent_Down', 'p1_Right': 'opponent_Right', 'p1_Left': 'opponent_Left', 'p1_Y': 'opponent_Y', 'p1_B': 'opponent_B', 'p1_X': 'opponent_X', 'p1_A': 'opponent_A', 'p1_L': 'opponent_L',
                                'p1_R': 'opponent_R', 'p2_Up': 'player_Up', 'p2_Down': 'player_Down', 'p2_Right': 'player_Right', 'p2_Left': 'player_Left', 'p2_Y': 'player_Y', 'p2_B': 'player_B', 'p2_X': 'player_X', 'p2_A': 'player_A', 'p2_L': 'player_L', 'p2_R': 'player_R'})
        # flip x coordinates
        df['opponent_x'] = df['opponent_x'].apply(lambda x: 1 - x)
        df['player_x'] = df['player_x'].apply(lambda x: 1 - x)
    else:
        # rename p1 to player and p2 to opponent
        df = df.rename(columns={'p1_character': 'player_character', 'p1_jumping': 'player_jumping', 'p1_crouching': 'player_crouching', 'p1_in_move': 'player_in_move', 'p1_x': 'player_x', 'p1_y': 'player_y', 'p1_health': 'player_health',
                                'p2_character': 'opponent_character', 'p2_jumping': 'opponent_jumping', 'p2_crouching': 'opponent_crouching', 'p2_in_move': 'opponent_in_move', 'p2_x': 'opponent_x', 'p2_y': 'opponent_y', 'p2_health': 'opponent_health'})
        # rename all moves columns
        df = df.rename(columns={'p1_Up': 'player_Up', 'p1_Down': 'player_Down', 'p1_Right': 'player_Right', 'p1_Left': 'player_Left', 'p1_Y': 'player_Y', 'p1_B': 'player_B', 'p1_X': 'player_X', 'p1_A': 'player_A', 'p1_L': 'player_L', 'p1_R': 'player_R',
                                'p2_Up': 'opponent_Up', 'p2_Down': 'opponent_Down', 'p2_Right': 'opponent_Right', 'p2_Left': 'opponent_Left', 'p2_Y': 'opponent_Y', 'p2_B': 'opponent_B', 'p2_X': 'opponent_X', 'p2_A': 'opponent_A', 'p2_L': 'opponent_L', 'p2_R': 'opponent_R'})

    # diff between x coordinates
    df['x_diff'] = df['player_x'] - df['opponent_x']
    # drop x coordinates
    df = df.drop(['player_x', 'opponent_x'], axis=1)

    # diff between y coordinates
    df['y_diff'] = df['player_y'] - df['opponent_y']
    # drop y coordinates
    df = df.drop(['player_y', 'opponent_y'], axis=1)

    # convert moves to numbers
    # get player moves
    # up move
    df['player_Up'] = df['player_Up'].astype(int)
    # down move
    df['player_Down'] = df['player_Down'].astype(int)
    # right move
    df['player_Right'] = df['player_Right'].astype(int)
    # left move
    df['player_Left'] = df['player_Left'].astype(int)
    # Y move
    df['player_Y'] = df['player_Y'].astype(int)
    # B move
    df['player_B'] = df['player_B'].astype(int)
    # X move
    df['player_X'] = df['player_X'].astype(int)
    # A move
    df['player_A'] = df['player_A'].astype(int)
    # L move
    df['player_L'] = df['player_L'].astype(int)
    # R move
    df['player_R'] = df['player_R'].astype(int)

    # get opponent moves
    # up move
    df['opponent_Up'] = df['opponent_Up'].astype(int)
    # down move
    df['opponent_Down'] = df['opponent_Down'].astype(int)
    # right move
    df['opponent_Right'] = df['opponent_Right'].astype(int)
    # left move
    df['opponent_Left'] = df['opponent_Left'].astype(int)
    # Y move
    df['opponent_Y'] = df['opponent_Y'].astype(int)
    # B move
    df['opponent_B'] = df['opponent_B'].astype(int)
    # X move
    df['opponent_X'] = df['opponent_X'].astype(int)
    # A move
    df['opponent_A'] = df['opponent_A'].astype(int)
    # L move
    df['opponent_L'] = df['opponent_L'].astype(int)
    # R move
    df['opponent_R'] = df['opponent_R'].astype(int)

    # combine moves to create unique move id with player moves in string
    df['player_moves'] = df['player_Up'].astype(str) + df['player_Down'].astype(str) + df['player_Right'].astype(str) + df['player_Left'].astype(str) + df['player_Y'].astype(
        str) + df['player_B'].astype(str) + df['player_X'].astype(str) + df['player_A'].astype(str) + df['player_L'].astype(str) + df['player_R'].astype(str)
    # combine moves to create unique move id with opponent moves in string
    df['opponent_moves'] = df['opponent_Up'].astype(str) + df['opponent_Down'].astype(str) + df['opponent_Right'].astype(str) + df['opponent_Left'].astype(str) + df['opponent_Y'].astype(
        str) + df['opponent_B'].astype(str) + df['opponent_X'].astype(str) + df['opponent_A'].astype(str) + df['opponent_L'].astype(str) + df['opponent_R'].astype(str)

    # convert string to binary int
    df['player_moves'] = df['player_moves'].apply(lambda x: int(x, 2))
    df['opponent_moves'] = df['opponent_moves'].apply(lambda x: int(x, 2))

    # drop moves
    df = df.drop(['player_Up', 'player_Down', 'player_Right', 'player_Left', 'player_Y', 'player_B', 'player_X', 'player_A', 'player_L', 'player_R', 'opponent_Up',
                 'opponent_Down', 'opponent_Right', 'opponent_Left', 'opponent_Y', 'opponent_B', 'opponent_X', 'opponent_A', 'opponent_L', 'opponent_R'], axis=1)

    # convert other columns to int
    df['player_jumping'] = df['player_jumping'].astype(int)
    df['player_crouching'] = df['player_crouching'].astype(int)
    df['player_in_move'] = df['player_in_move'].astype(int)
    df['opponent_jumping'] = df['opponent_jumping'].astype(int)
    df['opponent_crouching'] = df['opponent_crouching'].astype(int)
    df['opponent_in_move'] = df['opponent_in_move'].astype(int)

    # drop player column
    df = df.drop(['player'], axis=1)
    df = df.drop(['p1_move'], axis=1)
    df = df.drop(['p2_move'], axis=1)

    return df


target_columns = ['player_moves']
all_columns = ['timer', 'opponent_character', 'opponent_health', 'opponent_jumping',
               'opponent_crouching', 'opponent_in_move', 'player_character',
               'player_health', 'player_jumping', 'player_crouching', 'player_in_move',
               'x_diff', 'y_diff', 'player_moves', 'opponent_moves']


def create_timer_slices(data):
    timer_slices = []
    # Initialize current timer value to the first frame's timer value
    current_timer_val = data[0, 0]
    # Initialize current timer slice with the first frame
    current_timer_slice = [data[0]]
    for frame in data[1:]:
        if frame[0] >= current_timer_val:
            # Add frame to current timer slice
            current_timer_slice.append(frame)
            current_timer_val = frame[0]
        else:
            # Append current timer slice to timer slices
            timer_slices.append(np.array(current_timer_slice))
            current_timer_val = frame[0]
            # Start new timer slice with the current frame
            current_timer_slice = [frame]
    # Append final timer slice to timer slices
    timer_slices.append(np.array(current_timer_slice))
    return timer_slices


def create_window_slices(timer_slices, window_size):
    window_slices = []
    for timer_slice in timer_slices:
        num_frames = len(timer_slice)
        if num_frames >= window_size:
            for i in range(num_frames - window_size + 1):
                window_slice = timer_slice[i:i+window_size]
                # make dataframes
                window_slice = pd.DataFrame(window_slice, columns=['timer', 'opponent_character', 'opponent_health', 'opponent_jumping',
                                                                   'opponent_crouching', 'opponent_in_move', 'player_character',
                                                                   'player_health', 'player_jumping', 'player_crouching', 'player_in_move',
                                                                   'x_diff', 'y_diff', 'player_moves', 'opponent_moves'])
                window_slices.append(window_slice)
    return window_slices


def reShapeData(df):
    # convert to numpy array
    data = df.to_numpy()

    # create timer slices
    timer_slices = create_timer_slices(data)

    # create window slices
    window_slices = create_window_slices(timer_slices, 3)

    return window_slices


def getXy(df):
    X = df[all_columns].values
    y = df[target_columns].values

    return X, y


def getXyWindows(df):
    X = df
    # get target columns extracted from window_slices using target_columns
    y = df[:, :, all_columns.isin(target_columns)]
    # reshape y
    y = y.reshape(y.shape[0] * y.shape[1], y.shape[2])

    # Decrease window slice dimension
    X = X.reshape(X.shape[0] * X.shape[1], X.shape[2])

    return X, y


def create_window_slices_of_data(df):

    # create timer slices
    timer_slices = create_timer_slices(df)

    # create window slices
    window_slices = create_window_slices(timer_slices, 3)

    return window_slices


def preProcessAndGetXy(df):
    # preprocess data
    df = preProcessData(df)

    if df.empty:
        return None, None

    # Get X and y
    X, y = getXy(df)

    return X, y


def preProcessAndMakeWindows():
    # read data
    df = readData('./csvs/learning.csv')

    # preprocess data
    df = preProcessData(df)

    # convert to numpy array
    data = df.to_numpy()

    # create timer slices
    timer_slices = create_timer_slices(data)

    # create window slices
    window_slices = create_window_slices(timer_slices, 3)

    # save window slices
    for i, window_slice in enumerate(window_slices):
        window_slice.to_csv('csvs/window' + str(i) + '.csv', index=False)

    return window_slices
