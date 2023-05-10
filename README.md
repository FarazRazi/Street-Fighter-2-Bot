# Street-Fighter-2-Bot

## How to Start
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
