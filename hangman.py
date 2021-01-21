#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
from random import *
import random

#사운드 출력 필요 모듈
import winsound

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
#힌트텍스트의 폰트 설정
hint_font = pygame.font.SysFont('arial', 30)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

#힌트버튼 사진
hb = pygame.image.load('hint.png')
#이미지크기변경
hintb = pygame.transform.scale(hb, (50,50))

limbs = 0

#특정 범위 내의 좌표 마우스 클릭시 작동하는 클래스
class hintbutton():
    #생성자
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    #마우스 좌표가 범위 내에 있을때 True 반환
    def isover(self,pos):
        if pos[0]>self.x and pos[0]<self.width:
            if pos[1]>self.y and pos[1]<self.height:
                return True

#힌트 버튼 생성
hButton = hintbutton(640,415,690,465)


def redraw_game_window():
    global guessed
    global hangmanPics
    #힌트버튼 변수 선언
    global hintb
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

    #화면에 힌트 버튼 그림 출력
    win.blit(hintb, (640, 415))

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
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        #정답시 사운드
        winsound.PlaySound('./sound/pass.wav',winsound.SND_FILENAME)
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        #정답이 아닐시 사운드
        winsound.PlaySound('./sound/nonpass.wav',winsound.SND_FILENAME)
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

word = randomWord()
#랜덤한 단어의 공백을 제거
hintword = word.replace(' ', '')
#공백제거한 단어의 알파벳 하나를 랜덤으로 추출
w = random.choice(hintword)
#간단하게는
#w = random.choice(word)
#t = w.upper()
#도 가능하지만 이미 추측한 알파벳도 나옴..
#근데 아래 코드도 실행시 똑같이 추측한 알파벳도 나오기 때문에.. 똑같다. 어차피 추측한 알파벳도 나오게 할거라면 위 코드 써도 될 듯.
def Hint():
    global w
    while True:
        #변수w가 이미 추측한 알파벳이라면
        if w in guessed:
            #변수w 다시 지정
            w = random.choice(hintword)
        #아니라면
        else:
            #변수 t에 w를 대문자로 변환한 것 저장
            t = w.upper()
            #반복문 종료
            break
    return t

inPlay = True

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
            #힌트버튼 클릭하면
            if hButton.isover(clickPos):
                #힌트버튼 클릭시 소리 재생
                winsound.PlaySound('./sound/click.wav',winsound.SND_FILENAME)
                #힌트 생성
                t = Hint()
                #텍스트 객체 생성, t=텍스트내용, True = Anti-aliasing 사용, BLACK = 텍스트 컬러 
                text = hint_font.render(t, True, BLACK)
                #화면에 텍스트 객체 출력
                win.blit(text,(660,380))
                #화면업데이트
                pygame.display.update()

            if letter != None:
                #알파벳 버튼 클릭시 소리 재생
                winsound.PlaySound('./sound/click.wav',winsound.SND_FILENAME)
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
