#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random

pygame.init()

class Hangman():
    def __init__(self):
        self.winHeight = 480
        self.winWidth = 700
        self.win=pygame.display.set_mode((self.winWidth,self.winHeight))
        self.BLACK = (0,0, 0)
        self.WHITE = (255,255,255)
        self.RED = (255,0, 0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.LIGHT_BLUE = (102,255,255)

        self.btn_font = pygame.font.SysFont("arial", 20)
        self.guess_font = pygame.font.SysFont("monospace", 24)
        self.lost_font = pygame.font.SysFont('arial', 45)
        self.word = ''
        self.buttons = []
        self.guessed = []
        self.hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

        self.limbs = 0


    def redraw_game_window(self):
        self.win.fill(self.GREEN)
        # Buttons
        for i in range(len(self.buttons)):
            if self.buttons[i][4]:
                pygame.draw.circle(self.win, self.BLACK, (self.buttons[i][1], self.buttons[i][2]), self.buttons[i][3])
                pygame.draw.circle(self.win, self.buttons[i][0], (self.buttons[i][1], self.buttons[i][2]), self.buttons[i][3] - 2
                                )
                label = self.btn_font.render(chr(self.buttons[i][5]), 1, self.BLACK)
                self.win.blit(label, (self.buttons[i][1] - (label.get_width() / 2), self.buttons[i][2] - (label.get_height() / 2)))

        spaced = self.spacedOut(self.word, self.guessed)
        label1 = self.guess_font.render(spaced, 1, self.BLACK)
        rect = label1.get_rect()
        length = rect[2]
        
        self.win.blit(label1,(self.winWidth/2 - length/2, 400))

        pic = self.hangmanPics[self.limbs]
        self.win.blit(pic, (self.winWidth/2 - pic.get_width()/2 + 20, 150))
        pygame.display.update()


    def randomWord(self):
        file = open('words.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)

        return f[i][:-1]


    def hang(self, guess):
        if guess.lower() not in self.word.lower():
            return True
        else:
            return False


    def spacedOut(self, word, guessed=[]):
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
                

    def buttonHit(self, x, y):
        for i in range(len(self.buttons)):
            if x < self.buttons[i][1] + 20 and x > self.buttons[i][1] - 20:
                if y < self.buttons[i][2] + 20 and y > self.buttons[i][2] - 20:
                    return self.buttons[i][5]
        return None


    def end(self, winner=False):
        lostTxt = 'You Lost, press any key to play again...'
        winTxt = 'WINNER!, press any key to play again...'
        self.redraw_game_window()
        pygame.time.delay(1000)
        self.win.fill(self.GREEN)

        if winner == True:
            label = self.lost_font.render(winTxt, 1, self.BLACK)
        else:
            label = self.lost_font.render(lostTxt, 1, self.BLACK)

        wordTxt = self.lost_font.render(self.word.upper(), 1, self.BLACK)
        wordWas = self.lost_font.render('The phrase was: ', 1, self.BLACK)

        self.win.blit(wordTxt, (self.winWidth/2 - wordTxt.get_width()/2, 295))
        self.win.blit(wordWas, (self.winWidth/2 - wordWas.get_width()/2, 245))
        self.win.blit(label, (self.winWidth / 2 - label.get_width() / 2, 140))
        pygame.display.update()
        again = True
        while again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    again = False
        self.reset()


    def reset(self):
        for i in range(len(self.buttons)):
            self.buttons[i][4] = True

        self.limbs = 0
        self.guessed = []
        self.word = self.randomWord()

    #MAINLINE


    # Setup buttons
    def run(self):
        increase = round(self.winWidth / 13)
        for i in range(26):
            if i < 13:
                y = 40
                x = 25 + (increase * i)
            else:
                x = 25 + (increase * (i - 13))
                y = 85
            self.buttons.append([self.LIGHT_BLUE, x, y, 20, True, 65 + i])
            # buttons.append([color, x_pos, y_pos, radius, visible, char])

        self.word = self.randomWord()
        inPlay = True

        while inPlay:
            self.redraw_game_window()
            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    inPlay = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        inPlay = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickPos = pygame.mouse.get_pos()
                    letter = self.buttonHit(clickPos[0], clickPos[1])
                    if letter != None:
                        self.guessed.append(chr(letter))
                        self.buttons[letter - 65][4] = False
                        if self.hang(chr(letter)):
                            if self.limbs != 5:
                                self.limbs += 1
                            else:
                                self.end()
                        else:
                            print(self.spacedOut(self.word, self.guessed))
                            if self.spacedOut(self.word, self.guessed).count('_') == 0:
                                self.end(True)
hangman = Hangman()
hangman.run()
pygame.quit()

# always quit pygame when done!
