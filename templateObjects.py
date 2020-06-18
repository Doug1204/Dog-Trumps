import random
import os
from typing import no_type_check

#dogPictures = list(range(len([1 for directory in os.listdir() if os.path.splitext(directory)[1] == '.png'])))

class CustomError(Exception):
    pass

class Deck:
    def __init__(self) -> None:
        #Initializes empty deck
        self.content = []
    
    def shuffle(self) -> None:
        #Shuffles deck
        random.shuffle(self.content)
    
    def createCards(self, numberOfCards: int) -> None:
        #badInput = True
        #CARD_RANGE = (4, 30)
        """
        while badInput:
            #Checks user input
            userInput = input('How many cards would you like to play with? (4-30): ')
            if userInput.isdigit(): # check if it's a number
                userInput = int(userInput)
                if userInput < CARD_RANGE[0] or userInput > CARD_RANGE[1]: # checks if in range
                    print('Please enter a number wich is in the range 4-30')
                elif userInput % 2 != 0: # checks if even
                    print('Please enter an even number.')
                else: # The number is allowed
                    numberOfCards = userInput
                    badInput = False
            else: #if not a number
                print('Please enter a number')
        """
        for _ in range(numberOfCards): # adds cards to deck
            self.content.append(Card(self))

class Card:
    @no_type_check
    def __init__(self, DeckInstance: 'Instance of Deck class'):
        #defines stats for individual card
        self.NAME = self._getName(DeckInstance)
        self.STATS = self._getStats()
        self.EXERSIZE, self.INTELLIGENCE, self.FRIENDLINESS, self.DROOL = self.STATS
        self.STAT_NAMES = ['exersize', 'intelligence', 'friendliness', 'drool']
    
    def _getName(self, DeckInstance) -> str:
        #finds and retrieves a unique name for the dog
        NameFile = 'dogs.txt'
        with open(NameFile, 'r') as f:
            names = f.read().split('\n')
        takenNames = [dog.NAME for dog in DeckInstance.content]
        random.shuffle(names)
        for name in names:
            if name not in takenNames:
                return name
        else:
            raise CustomError('Not enough names in', NameFile)
    
    def _getStats(self) -> tuple:
        #creates random stats for card
        exersize = random.randint(1, 5)
        intelligence = random.randint(1, 100)
        friendliness = random.randint(1, 100)
        drool = random.randint(1, 10)
        return exersize, intelligence, friendliness, drool

class Player:
    @no_type_check
    def __init__(self, DeckInstance: 'Instance of Deck class', computer=False):
        halfDeck = len(DeckInstance.content) // 2
        if halfDeck and not computer: # if normal player and cards in deck
            self.hand = DeckInstance.content[:halfDeck]
        elif halfDeck and computer: # if computer and cards in deck
            self.hand = DeckInstance.content[halfDeck:]
        else: # no cards in deck
            raise CustomError("No content in deck")
    
    def checkVictor(self, other: object, stat: str) -> None:
        playerStat = getattr(self.hand[0], stat.upper())
        compStat = getattr(other.hand[0], stat.upper())
        if stat != 'drool':
            return playerStat >= compStat
        return playerStat < compStat
    
    def win(self, other: object) -> None:
        self.hand = [*self.hand[1:], self.hand[0], other.hand[0]]
        other.hand.pop(0)

    




if __name__ == '__main__':
    pass


