#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random
from time import sleep

pygame.init()
winHeight = 640
winWidth = 960
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
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

limbs = 0
output = ""
mini_game = 0

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


def randomWord():
    file = open('words.txt')
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
    lostTxt = 'You Lost, See you next time...'
    winTxt = 'Congratulations! YOU WINNER!'
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

#rock paper scissors game
class Button():
    def __init__(self, x, y, pos, width, height):
        self.x = x
        self.y = y
        self.pos = pos
        self.width = width
        self.height = height
        
        
    def clicked(self, pos):
        self.pos = pygame.mouse.get_pos()
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width:
            if self.pos[1] > self.y and self.pos[1] < self.y + self.height:
                return True
        return False


class RpsGame():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Rock Paper Scissors")

        self.bg = pygame.image.load("rps/bg.png")
        self.bg = pygame.transform.scale(self.bg, (960, 640))
        self.r_btn = pygame.image.load("rps/rock.png").convert_alpha()
        self.p_btn = pygame.image.load("rps/paper.png").convert_alpha()
        self.s_btn = pygame.image.load("rps/scissors.png").convert_alpha()

        self.choose_rock = pygame.image.load("rps/r.png").convert_alpha()
        self.choose_rock = pygame.transform.scale(self.choose_rock, (150, 150))
        self.choose_paper = pygame.image.load("rps/p.png").convert_alpha()
        self.choose_paper = pygame.transform.scale(self.choose_paper, (150, 150))
        self.choose_scissors = pygame.image.load("rps/s.png").convert_alpha()
        self.choose_scissors = pygame.transform.scale(self.choose_scissors, (150, 150))

        self.tie = pygame.image.load("rps/tie.png").convert_alpha()
        self.win = pygame.image.load("rps/win.png").convert_alpha()
        self.lose = pygame.image.load("rps/lose.png").convert_alpha()
        self.pc_random_choice = ""

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.r_btn, (20, 500))
        self.screen.blit(self.p_btn, (330, 500))
        self.screen.blit(self.s_btn, (640, 500))

        self.rock_btn = Button(30, 520, (30, 520), 250, 100)
        self.paper_btn = Button(340, 520, (340, 520), 250, 100)
        self.scissors_btn = Button(640, 520, (640, 520), 250, 100)


    

    def output(self):
        global pc
        pc = self.pc_random_choice
        output = ""
        
        if self.rock_btn.clicked(30):
            self.p_option = "rock"
            self.screen.blit(self.choose_rock, (200, 200))
            if pc == "rock":
                self.screen.blit(self.tie, (360, 50))
            elif pc == "paper":
                self.screen.blit(self.lose, (360, 50))
                output = "lose"
            elif pc == "scissors":
                self.screen.blit(self.win, (360, 50))
                output = "win"
        elif self.paper_btn.clicked(30):
            self.p_option = "paper"
            self.screen.blit(self.choose_paper, (200, 200))
            if pc == "rock":
                self.screen.blit(self.win, (360, 50))
                output = "win"
            elif pc == "paper":
                self.screen.blit(self.tie, (360, 50))
            elif pc == "scissors":
                self.screen.blit(self.lose, (360, 50))
                output = "lose"
        elif self.scissors_btn.clicked(30):
            self.p_option = "scissors"
            self.screen.blit(self.choose_scissors, (200, 200))
            if pc == "rock":
                self.screen.blit(self.lose, (360, 50))
                output = "lose"
            elif pc == "paper":
                self.screen.blit(self.win, (360, 50))
                output = "win"
            elif pc == "scissors":
                self.screen.blit(self.tie, (360, 50))

        return output
        

    def computer(self):
        self.pc_random_choice = " "
        option = ["rock", "paper", "scissors"]
        pc_choice = random.choice(list(option))
        if pc_choice == "rock":
            self.pc_random_choice = "rock"
            pc_choice = self.choose_rock
        elif pc_choice == "paper":
            self.pc_random_choice = "paper"
            pc_choice = self.choose_paper
        else:
            self.pc_random_choice = "scissors"
            pc_choice = self.choose_scissors
        pc_option = self.screen.blit(pc_choice, (600, 200))
        return pc_option




    def image_reset(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.r_btn, (20, 500))
        self.screen.blit(self.p_btn, (330, 500))
        self.screen.blit(self.s_btn, (640, 500))
        pass

    def game_loop(self):
        run = True
        clock = pygame.time.Clock()
        rps_game = RpsGame()
        
        while run:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rock_btn.clicked(30) or self.paper_btn.clicked(340) or self.scissors_btn.clicked(640):
                        rps_game.image_reset()
                        rps_game.computer()
                        output = rps_game.output()
                        if output == "win":
                            print("You win! Now you have 2 chances...")
                            run = False
                        elif output == "lose":
                            print("You lose... ending the game...")
                            run = False
                        pc = self.pc_random_choice
                        
            pygame.display.flip()
            if run == False:
                sleep(1.5)
            clock.tick(30)


        return output
        pygame.init()         


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

word = randomWord()
inPlay = True
mini_game = 0

while inPlay:
    redraw_game_window()

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
                        if mini_game == 0:
                            mini_game += 1
                            pygame.init()
                            game = RpsGame()
                            output = game.game_loop()
                            if output == "win":
                                limbs = 4
                            elif output == "lose":
                                end()
                        elif mini_game >= 1:
                            end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()
# always quit pygame when done!


