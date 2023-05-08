from command import Command
import numpy as np
from buttons import Buttons
class Bot:

    def __init__(self):
        #< - v + < - v - v + > - > + Y
        self.fire_code=["<","!<","v+<","!v+!<","v","!v","v+>","!v+!>",">+Y","!>+!Y"]
        self.exe_code = 0
        self.start_fire=True
        self.remaining_code=[]
        self.my_command = Command()
        self.buttn= Buttons()
        self.prev = 0
        self.learning = False

    def learn(self, file_name):
        self.file_name = file_name
        self.learning = True
        # list of dataframes
        self.dfs = []

    def save(self, current_game_state, player):
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

        # add the player number
        obj['curr_player'] = player

        # print(obj)

        # # convert the obj to a dataframe
        # df = pd.DataFrame(obj, index=[0])

        # append the dataframe to the dfs list
        self.dfs.append(obj)


    def fight(self,current_game_state,player,random):
        #python Videos\gamebot-competition-master\PythonAPI\controller.py 1
        if player==1:
            #print("1")
            #v - < + v - < + B spinning

            if( self.exe_code!=0  ):
               self.run_command([],current_game_state.player1)
            diff=current_game_state.player2.x_coord - current_game_state.player1.x_coord
            if (  diff > 60 ) :
                toss=np.random.randint(3)
                if (toss==0):
                    #self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player1)
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
                elif ( toss==1 ):
                    self.run_command([">+^+B",">+^+B","!>+!^+!B"],current_game_state.player1)
                else: #fire
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
            elif (  diff < -60 ) :
                toss=np.random.randint(3)
                if (toss==0):#spinning
                    #self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player1)
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
                elif ( toss==1):#
                    self.run_command(["<+^+B","<+^+B","!<+!^+!B"],current_game_state.player1)
                else: #fire
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
            else:
                toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
                if ( toss>=1 ):
                    if (diff>0):
                        self.run_command(["<","<","!<"],current_game_state.player1)
                    else:
                        self.run_command([">",">","!>"],current_game_state.player1)
                else:
                    self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player1)
            self.my_command.player_buttons=self.buttn

        elif player==2:

            if( self.exe_code!=0  ):
               self.run_command([],current_game_state.player2)
            diff=current_game_state.player1.x_coord - current_game_state.player2.x_coord
            if (  diff > 60 ) :
                toss=np.random.randint(3)
                if (toss==0):
                    #self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player2)
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player2)
                elif ( toss==1 ):
                    self.run_command([">+^+B",">+^+B","!>+!^+!B"],current_game_state.player2)
                else:
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player2)
            elif ( diff < -60 ) :
                toss=np.random.randint(3)
                if (toss==0):
                    #self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player2)
                    self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player2)
                elif ( toss==1):
                    self.run_command(["<+^+B","<+^+B","!<+!^+!B"],current_game_state.player2)
                else:
                    self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player2)
            else:
                toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
                if ( toss>=1 ):
                    if (diff<0):
                        self.run_command(["<","<","!<"],current_game_state.player2)
                    else:
                        self.run_command([">",">","!>"],current_game_state.player2)
                else:
                    self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player2)
            self.my_command.player2_buttons=self.buttn
            
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



    def run_command( self , com , player   ):

        if self.exe_code-1==len(self.fire_code):
            self.exe_code=0
            self.start_fire=False
            print ("compelete")
            #exit()
            # print ( "left:",player.player_buttons.left )
            # print ( "right:",player.player_buttons.right )
            # print ( "up:",player.player_buttons.up )
            # print ( "down:",player.player_buttons.down )
            # print ( "Y:",player.player_buttons.Y )

        elif len(self.remaining_code)==0 :

            self.fire_code=com
            #self.my_command=Command()
            self.exe_code+=1

            self.remaining_code=self.fire_code[0:]

        else:
            self.exe_code+=1
            if self.remaining_code[0]=="v+<":
                self.buttn.down=True
                self.buttn.left=True
                print("v+<")
            elif self.remaining_code[0]=="!v+!<":
                self.buttn.down=False
                self.buttn.left=False
                print("!v+!<")
            elif self.remaining_code[0]=="v+>":
                self.buttn.down=True
                self.buttn.right=True
                print("v+>")
            elif self.remaining_code[0]=="!v+!>":
                self.buttn.down=False
                self.buttn.right=False
                print("!v+!>")

            elif self.remaining_code[0]==">+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.right=True
                print(">+Y")
            elif self.remaining_code[0]=="!>+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.right=False
                print("!>+!Y")

            elif self.remaining_code[0]=="<+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.left=True
                print("<+Y")
            elif self.remaining_code[0]=="!<+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.left=False
                print("!<+!Y")

            elif self.remaining_code[0]== ">+^+L" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print(">+^+L")
            elif self.remaining_code[0]== "!>+!^+!L" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.L= False #not (player.player_buttons.L)
                print("!>+!^+!L")

            elif self.remaining_code[0]== ">+^+Y" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print(">+^+Y")
            elif self.remaining_code[0]== "!>+!^+!Y" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.Y= False #not (player.player_buttons.L)
                print("!>+!^+!Y")


            elif self.remaining_code[0]== ">+^+R" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print(">+^+R")
            elif self.remaining_code[0]== "!>+!^+!R" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.R= False #ot (player.player_buttons.R)
                print("!>+!^+!R")

            elif self.remaining_code[0]== ">+^+A" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print(">+^+A")
            elif self.remaining_code[0]== "!>+!^+!A" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.A= False #not (player.player_buttons.A)
                print("!>+!^+!A")

            elif self.remaining_code[0]== ">+^+B" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print(">+^+B")
            elif self.remaining_code[0]== "!>+!^+!B" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.B= False #not (player.player_buttons.A)
                print("!>+!^+!B")

            elif self.remaining_code[0]== "<+^+L" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print("<+^+L")
            elif self.remaining_code[0]== "!<+!^+!L" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.L= False  #not (player.player_buttons.Y)
                print("!<+!^+!L")

            elif self.remaining_code[0]== "<+^+Y" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print("<+^+Y")
            elif self.remaining_code[0]== "!<+!^+!Y" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.Y= False  #not (player.player_buttons.Y)
                print("!<+!^+!Y")

            elif self.remaining_code[0]== "<+^+R" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print("<+^+R")
            elif self.remaining_code[0]== "!<+!^+!R" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!<+!^+!R")

            elif self.remaining_code[0]== "<+^+A" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print("<+^+A")
            elif self.remaining_code[0]== "!<+!^+!A" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.A= False  #not (player.player_buttons.Y)
                print("!<+!^+!A")

            elif self.remaining_code[0]== "<+^+B" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print("<+^+B")
            elif self.remaining_code[0]== "!<+!^+!B" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.B= False  #not (player.player_buttons.Y)
                print("!<+!^+!B")

            elif self.remaining_code[0]== "v+R" :
                self.buttn.down=True
                self.buttn.R= not (player.player_buttons.R)
                print("v+R")
            elif self.remaining_code[0]== "!v+!R" :
                self.buttn.down=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!v+!R")

            else:
                if self.remaining_code[0] =="v" :
                    self.buttn.down=True
                    print ( "down" )
                elif self.remaining_code[0] =="!v":
                    self.buttn.down=False
                    print ( "Not down" )
                elif self.remaining_code[0] =="<" :
                    print ( "left" )
                    self.buttn.left=True
                elif self.remaining_code[0] =="!<" :
                    print ( "Not left" )
                    self.buttn.left=False
                elif self.remaining_code[0] ==">" :
                    print ( "right" )
                    self.buttn.right=True
                elif self.remaining_code[0] =="!>" :
                    print ( "Not right" )
                    self.buttn.right=False

                elif self.remaining_code[0] =="^" :
                    print ( "up" )
                    self.buttn.up=True
                elif self.remaining_code[0] =="!^" :
                    print ( "Not up" )
                    self.buttn.up=False
            self.remaining_code=self.remaining_code[1:]
        return