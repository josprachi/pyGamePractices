import pygame
import os
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255,20,255)

COLOR_CODE_RED=1
COLOR_CODE_YELLOW=2
COLOR_CODE_BLUE=3
COLOR_CODE_GREEN=4

MAX_NO_PLAYERS=4
MAX_NO_PAWNS=4
_CLI=True


class Player:
    diceValue=None
    pawns=[]
    color=WHITE
    selectedPawn=0
    no_Pawns_In_Castle=0

    def __init__(self,color):
        self.diceValue=None
        self.pawns=[]
        self.color=color
        self.selectedPawn=0
        self.no_Pawns_In_Castle=0
        i=0  
        while i<MAX_NO_PAWNS:
            print("pawn generated",i)
            _pawn=Pawn(self.color)
            self.pawns.append(_pawn)
            i+=1
        print("init")

    def reset(self):
        self.diceValue=None
        self.pawns=[]
        self.color=WHITE
        self.selectedPawn=0
        self.no_Pawns_In_Castle=0        
        print("Reset")

    def movePawn(self,pawnId,squaresToMove):
        self.pawns[pawnId].sqPosition +=squaresToMove

    def killPawn(self,pawnId):
        self.pawns[pawnId].reset()

    def update(self):
        print("update")

    def render(self):
        print("render")    


class Pawn:
    color=WHITE
    sqPosition=0
    inCastle=False
    xPos=0
    yPos=0

    def __init__(self,color):
        self.color=color
        self.sqPosition=0
        self.inCastle=False
        self.xPos=0
        self.yPos=0 



class GameLayer:
    width=0
    height=0
    background_color=WHITE
    border_Thickness=5
    num_Players=0
    players=[]
    colors=[1,2,3,4]

    def __init__(self):
        print("hello")
        pygame.init()
        self.input_Details()
        self.initPlayers()
        self.colors=[1,2,3,4]

    def initPlayers(self):
        i=0
        while i<self.num_Players :
            if _CLI:
                _color_Code=0
                #print("Here",_color_Code)
                while _color_Code not in self.colors:#_color_Code > COLOR_CODE_GREEN or _color_Code < COLOR_CODE_RED:
                    _color_Code=input("Enter Color Code: \n RED :1\n YELLOW :2\n BLUE :3\n GREEN :4\n")
                    #if _color_Code not in self.colors:
                        #_color_Code=input("Color already selected \n select new color code: \n RED :1\n YELLOW :2\n BLUE :3\n GREEN :4\n")    
                    #print(self.colors)
                    #if _color_Code in self.colors:
                    self.colors.pop(self.colors.index(_color_Code))
                            
                
            _player=Player(_color_Code) 
            self.players.append(_player)
            i+=1  

    def input_Details(self):
        self.num_Players=input("enter number of players")

if __name__ == "__main__":
    MainLayer=GameLayer()

