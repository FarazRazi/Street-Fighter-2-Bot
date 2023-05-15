# Street-Fighter-2-Bot

Welcome to our AI project - Street Fighter 2 Bot! In this project, we have developed an intelligent bot that can play Street Fighter 2, a popular fighting game. Our bot utilizes machine learning techniques to analyze the game state and make strategic moves in response to the opponent's actions.

## Data Preparation and Feature Engineering

To train our bot, we collected a dataset that captures the game states and corresponding moves. The dataset includes both player 1's moves and the resulting moves made by player 2. We performed feature engineering to extract meaningful features from the available columns, including the timer, opponent character, opponent health, opponent movement, opponent button presses, player character, player health, player movement, player button presses, and position differences. These features effectively capture the game state and provide valuable information for decision-making.

## Data Preprocessing and Model Selection

Before training the model, we preprocessed the dataset by normalizing numeric features, encoding categorical features, and splitting the data into training and testing sets. We performed various preprocessing steps such as removing irrelevant rows and columns, identifying the player in control, flipping X coordinates for consistency, calculating coordinate differences, converting moves to numbers, combining moves into unique move IDs, and converting data types.

For the analysis, we selected the decision tree classifier as our model of choice. The decision tree classifier is well-suited for our problem and dataset, allowing us to make predictions based on the game state and generate suitable counter moves for player 2.

## Prediction and Integration

After training and evaluating the model, we integrated it into the game logic to generate counter moves for player 2. Our bot processes each frame, predicts an action using the decision tree classifier, and executes the action accordingly. This integration enables dynamic decision-making based on the current game state, enhancing player experience and gameplay. The bot's predictions also facilitate learning and improvement over time as the current game state is saved for potential future analysis.

Overall, our AI-based Street Fighter 2 Bot showcases the power of machine learning and its application in the gaming domain. We believe this project contributes to the advancement of AI in gaming and opens up new possibilities for creating intelligent and adaptive virtual opponents.

## How to Start *(Instructions for game tournament)*
Here's an example of how you can run the code using the provided command-line arguments:
``` bash
python controller.py 1 -h
```
### As Player 1: 
``` bash
python controller.py 1
```
### As Player 2: 
``` bash
python controller.py 2 
```
This command will execute the controller.py script with the argument 1 for the player number, and the -h flag to display the help message and exit.

To run the code with different options, you can use the following command format:

``` bash
python controller.py [player_number] [options]
```

Replace [player_number] with the desired player number (e.g., 1 or 2).

Here is a description of the available options:

-h, --help: Displays the help message and exits.

-L, --learning: Enables learning mode.

-R, --random: Enables random mode.

-F FILE, --file FILE: Specifies the file name to save learning data.

-M {DT}, --model {DT}: Specifies the model name to load.

-T, --train: Enables initial training.

You can include these options along with the player number to customize the behavior of the script.

Please note that the provided usage information assumes the script is named controller.py and that it is located in the current working directory. Adjust the command accordingly if the script is in a different location.

If you need further assistance or have any questions, feel free to ask! @farazrazi432@gmail.com
