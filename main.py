import pygame
import time
import random
from itertools import cycle


from templateObjects import Deck, Player

#Initializes global variables
pygame.init()

WIDTH = 800
HEIGHT = 750
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

convertW = lambda x: int(x * WIDTH)
convertH = lambda x: int(x * HEIGHT)

GREEN = (0, 123, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTONS = (130, 68, 3)
CARD_COLOUR = (215, 215, 215)
GREY = (100, 100, 100)

cardBack = pygame.image.load('card_back.jpg') # loads card back image
cardBack = pygame.transform.scale(cardBack, (convertW(0.13), convertH(0.2)))


def mainBuild(player: object, computer: object) -> None:
    #Sets basic background
    DISPLAY.fill(GREEN)
    DISPLAY.blit(cardBack, (convertW(0.08), convertH(0.2))) # shows card backs
    DISPLAY.blit(cardBack, (convertW(0.08), convertH(0.5)))

    drawText(str(len(player.hand)), convertW(0.08), 0.01, convertH(0.54), BLACK) # shows how many cards the player has left
    drawText(str(len(computer.hand)), convertW(0.08), 0.01, convertH(0.24), BLACK) # shows how many cards the computer has left

def buildStart(basicDimension: list, start_y: int, quit_y: int) -> None:

    DISPLAY.fill(GREEN) # green background

    pygame.draw.rect(DISPLAY, BUTTONS, [basicDimension[0], start_y, *basicDimension[1:]]) # shows start button
    drawText('PLAY', convertW(0.1), basicDimension[0] + convertW(0.05), start_y + convertH(0.02), BLACK)

    pygame.draw.rect(DISPLAY, BUTTONS, [basicDimension[0], quit_y, *basicDimension[1:]]) # shows quit button
    drawText('QUIT', convertW(0.1), basicDimension[0] + convertW(0.05), quit_y + convertH(0.02), BLACK)

def menuButtons(basicDimension: list, start_y: int, quit_y: int) -> bool:

    xRange = (basicDimension[0], basicDimension[0] + basicDimension[1]) # the range of x values possible
    playButton = (start_y, start_y + basicDimension[2]) # the range of y values possible for start button
    quitButton = (quit_y, quit_y + basicDimension[2]) # the range of y values possible for quit button

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]: # if mouse pressed

        if x in range(*xRange): # if mouse in correct x range

            if y in range(*playButton): # if mouse in correct y range for start button
                return False

            elif y in range(*quitButton): # if mouse in correct y range for quit button
                pygame.quit()
                quit()

    return True

def selectBuild(triangle1: list, triangle2: list, cards: int, continButton: list) -> None:
    
    DISPLAY.fill(GREEN) # background

    pygame.draw.polygon(DISPLAY, WHITE, triangle1)
    pygame.draw.polygon(DISPLAY, WHITE, triangle2) # draws triangles

    drawText(str(cards), convertW(0.1), convertW(0.4), convertH(0.35), BLACK) # draws number of cards

    pygame.draw.rect(DISPLAY, BUTTONS, continButton) # shows continue button
    drawText('CONTINUE', convertW(0.06), continButton[0] + convertW(0.05), continButton[1] + convertH(0.03), BLACK)

def continueButtonPress(dimensions: list) -> bool:
    x, y = pygame.mouse.get_pos() # gets pos of mouse x and y

    if pygame.mouse.get_pressed()[0]: ## if mouse pressed
        if x in range(dimensions[0], dimensions[0] + dimensions[2]) and y in range(dimensions[1], dimensions[1] + dimensions[3]): # if in range of continue button dimensions
            return False

    return True

def changeCards(triangle1: list, triangle2: list, cards: int) -> int:
    possible = list(range(4, 32, 2)) # creates a cycle of possible values for card
    possible.extend(possible) # allows for if cards goes past max

    tri1Range = [(triangle1[1][0], triangle1[2][0]), (triangle1[0][1], triangle1[1][1])] # (x, x + tri width), (y, y + tri Height)
    tri2Range = [(triangle2[1][0], triangle2[2][0]), (triangle2[1][1], triangle2[0][1])] # (x, x + tri width), (y, y + tri Height)

    x, y = pygame.mouse.get_pos() # gets x and y pos of 
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            if x in range(*tri1Range[0]): # same x range
                index = possible.index(cards)

                if y in range(*tri1Range[1]): # if mouse in correct y value
                    cards = possible[index+1]

                elif y in range(*tri2Range[1]): # if mouse in correct y value
                    cards = possible[index-1]

        elif event.type == pygame.QUIT: # checks if quit is pressed
            pygame.quit()
            quit()

    return cards # returns new cards value
            

def showCard(player, computer, comparing: bool, computerTurn: bool) -> None:

    basicDimension = convertW(0.3), convertH(0.4) # width and height for base card
    if comparing:

        if player.checkVictor(computer, comparing): # checks winner of round
            text = 'You Win!'
            computerTurn = False
        else:
            text = 'You Lose.'
            computerTurn = True
        drawText(text, convertH(0.1), convertW(0.4), convertH(0.1), BLACK) # shows round winner

        Y = convertH(0.3) # y of both cards
        playerDimensions = [convertW(0.27), Y, *basicDimension]# Dimensions for player's card
        compDimensions = [convertW(0.65), Y, *basicDimension] # Dimensions for computer's card

        pygame.draw.rect(DISPLAY, CARD_COLOUR, playerDimensions)
        showValues(player, playerDimensions, comparing) # shows player's card

        pygame.draw.rect(DISPLAY, CARD_COLOUR, compDimensions)
        showValues(computer, compDimensions, comparing) # shows computer's card

        drawText(f'The catogory chosen was {comparing}', convertW(0.06), convertW(0.1), convertH(0.8), BLACK) # shows which category was chosen

        if text == 'You Win!': player.win(computer) # moves cards from loser's deck to back of winner's deck
        else: computer.win(player)


        stall(4)
        comparing = False

    else:

        if computerTurn: # shows that the computer is choosing
            drawText('Computer is choosing...', convertW(0.1), convertW(0.15), convertH(0.05), BLACK)

        dimensions = [convertW(0.4), convertH(0.5), *basicDimension] # x, y, width, height of card
        pygame.draw.rect(DISPLAY, CARD_COLOUR, dimensions) # draws white card background
        comparing = showValues(player, dimensions, comparing, computerTurn=computerTurn) # shows values and returns category if a category is pressed

        compCard = convertW(0.45), convertH(0.1) # x, y of computer's card
        DISPLAY.blit(cardBack, compCard) # shows back of computer's card

    return comparing, computerTurn

def showValues(player: object, dimensions: list, comparing: bool, computerTurn=False) -> None:

    drawText(player.hand[0].NAME, convertH(0.1), dimensions[0] + dimensions[2] * (0.85 / len(player.hand[0].NAME)), dimensions[1] + dimensions[3] * 0.2, BLACK) # shows card name

    y = dimensions[1] + dimensions[3] // 2 # base y
    deltaY = convertH(0.05) # change in y

    label = lambda dimensions: [convertH(0.03), dimensions[0] * 1.04, y] # base dimensions for showing stat values
    statLabel = lambda dimensions: [convertH(0.03), dimensions[0] + dimensions[2] * 0.85, y]
    box = lambda dimensions: [int(dimensions[0] + convertW(0.005)), int(y - convertH(0.015)), int(dimensions[2] * 0.93), deltaY]

    if not comparing: # checks if stat pressed
        comparing = select(player, dimensions, label, statLabel)

    for name, stat in zip(player.hand[0].STAT_NAMES, player.hand[0].STATS): # draws stats
        drawText(name, *label(dimensions), BLACK)
        drawText(str(stat), *statLabel(dimensions), BLACK)

        pygame.draw.rect(DISPLAY, BLACK, box(dimensions), 3)

        y += deltaY
    

    if computerTurn: # if computers turn, stall and choose random stat
        stall(2.5)
        comparing = random.choice(player.hand[0].STAT_NAMES)

    return comparing

def select(player, dimensions: list, label, statLabel) -> bool:
    mouse_x, mouse_y = pygame.mouse.get_pos() # x and y of mouse
    y = dimensions[1] + dimensions[3] // 2 # base y for where stats are displayed
    deltaY = convertH(0.05) # change in y for each stat
    
    box = [int(dimensions[0] + convertW(0.005)), int(dimensions[2] * 0.93)] # basic dimensions of surrounding box

    if mouse_x in range(box[0], box[0] + box[1]): # if mouse in correct x pos
        for stat_name in player.hand[0].STAT_NAMES: # loops through stat names
            if mouse_y in range(y - convertH(0.015), y + deltaY - convertH(0.015)): # checks where mouse y is
                pygame.draw.rect(DISPLAY, GREY, [int(dimensions[0] + convertW(0.005)), int(y - convertH(0.015)), int(dimensions[2] * 0.93), deltaY]) # boc turns grey when mouse if hovering over stat
                if pygame.mouse.get_pressed()[0]: # if mouse pressed
                    return stat_name # returns the stat which was clicked
            y += deltaY # go down a section

    return False

def checkWin(player: object, computer: object):
    if not len(player.hand): # if player has no cards
        return 'You Lose.'
    elif not len(computer.hand): # if computer has no cards
        return 'You Win!'
    return False

def stall(seconds: int) -> None: # useful as it allows pygame to wait whilst still (responding)

    looking = True
    start = time.time() # starts timer

    while looking:

        if time.time() - start >= seconds:  # checks if timer has exceeded max seconds
            looking = False

        buttons() # if quit pressed

        pygame.display.update()

def drawText(text: str, size: int, x: int, y: int, colour: tuple) -> None: # renders and blits text
    font = pygame.font.SysFont(None, size)
    text = font.render(text, True, colour)
    DISPLAY.blit(text, (int(x), int(y)))

def buttons() -> None:
    for event in pygame.event.get(): # loops through events
        if event.type == pygame.QUIT: # if quit button pressed
            pygame.quit() # uninitilizes pygame modules
            quit()

def startMenu():
    menu = True

    buttonDimensions = [convertW(0.35), convertW(0.3), convertH(0.1)] # x, width, height
    start_y = convertH(0.3) # different y values
    quit_y = convertH(0.5)

    while menu:

        buildStart(buttonDimensions, start_y, quit_y)  # draws buttons

        menu = menuButtons(buttonDimensions, start_y, quit_y) # checks if buttons pressed

        buttons() # if quit is presses

        pygame.display.update()

def chooseCards():
    cards = 16 # base number of cards
    selecting = True

    triangle1 = [[convertW(0.6), convertH(0.3)], [convertW(0.55), convertH(0.35)], [convertW(0.65), convertH(0.35)]] # middle, left, right to form triangle  # up
    triangle2 = [[convertW(0.6), convertH(0.45)], [convertW(0.55), convertH(0.4)], [convertW(0.65), convertH(0.4)]] # middle, left, right to form triangle  # down
    continueButton = [convertW(0.33), convertH(0.5), convertW(0.33), convertH(0.1)] # dimensions for continue button

    while selecting: # main loop for selecting num of cards

        selectBuild(triangle1, triangle2, cards, continueButton) # draws the buttons, number of cards and continue button

        cards = changeCards(triangle1, triangle2, cards) # checks if a triangle is pressed and return new number of cards (increases/decreases cards)

        selecting = continueButtonPress(continueButton) # checks if continue is pressed

        pygame.display.update()
    
    return cards # returns number of chosen cards 

def mainGame(player: object, computer: object) -> str:
    computerTurn = False
    comparing = False
    winner = False
    while not winner: # main Game loop

        mainBuild(player, computer) # base background
        comparing, computerTurn = showCard(player, computer, comparing, computerTurn) # displays card for player to choose catogory or compares them

        winner = checkWin(player, computer) # checks for winner

        buttons() # checks if buttons pressed

        pygame.display.update() # updates display
    
    return winner

def gameOver(won: str) -> None: # end game screen

    DISPLAY.fill(GREEN) # green background
    drawText(won, convertH(0.2), convertW(0.2), convertH(0.3), BLACK) # Shows error message

    stall(4)  # Allows player to quit whilst the game allows them to read end message


def main():

    while True: # Main game loop

        startMenu() # can play game or quit
        cards = chooseCards() # Chooses how many cards in the deck

        deck = Deck() # initialize empty deck
        deck.createCards(cards) # requests number of cards in deck then creates cards
        deck.shuffle() # shuffles deck
        player = Player(deck) # initializes player
        computer = Player(deck, computer=True) # initalizes computer

        won = mainGame(player, computer) # plays game and then returns whether the player won or lost

        gameOver(won) # Displays end game message: whether you have won or not
        

if __name__ == '__main__':
    main()