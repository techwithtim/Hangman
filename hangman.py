#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random

pygame.init()
winHeight = 480
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
word = ''
buttons = []
guessed = []
hangmanPics = [
    pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), 
    pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), 
    pygame.image.load('hangman6.png')
]

level_button = []

limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(GREEN)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))



    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()


    
def level():#바뀜
    win.fill(GREEN)
    font = pygame.font.SysFont("monospace", 24)  #폰트 설정
    text = font.render("level 1 -animal_easy",True, BLACK)  #텍스트가 표시된 Surface 를 만듬
    win.blit(text,(200,100))
    text = font.render("level 2 -animal_hard",True,BLACK)  #텍스트가 표시된 Surface 를 만듬
    win.blit(text,(200,150))
    text = font.render("level 3 -location_easy",True,BLACK)  #텍스트가 표시된 Surface 를 만듬
    win.blit(text,(200,200))
    text = font.render("level 4 -location_hard",True,BLACK)  #텍스트가 표시된 Surface 를 만듬
    win.blit(text,(200,250))
    text = font.render("level 5 -food_easy",True,BLACK)  #텍스트가 표시된 Surface 를 만듬
    win.blit(text,(200,300))
    text = font.render("level 6 -food_hard",True,BLACK)  #텍스트가 표시된 Surface 를 만듬
    win.blit(text,(200,350))
    pygame.display.update()
    
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                x, y = clickPos
                if y >= 80 and y <= 120:
                    if x >= 150 and x <= 500:
                        return 'animal_easy.txt'
                if y >= 130 and y <= 170:
                    if x >= 150 and x <= 500:
                        return 'animal_hard.txt'
                if y >= 180 and y <= 220:
                    if x >= 150 and x <= 500:
                        return 'location_easy.txt'
                if y >= 230 and y <= 270:
                    if x >= 150 and x <= 500:
                        return 'location_hard.txt'
                if y >= 280 and y <= 320:
                    if x >= 150 and x <= 500:
                        return 'food_easy.txt'
                if y >= 330 and y <= 380:
                    if x >= 150 and x <= 500:
                        return 'food_hard.txt'
    

    
    

def randomWord(w):#바뀜
    file = open(w)#바뀜
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

#MAINLINE


# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])


inPlay = True#바뀜
redraw_game_window()#바뀜
pygame.time.delay(10)#바뀜
w = level()#바뀜
word = randomWord(w)#바뀜


while inPlay:
    redraw_game_window()
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()

# always quit pygame when done!