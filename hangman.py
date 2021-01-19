#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random
import sqlite3
import datetime

score=0 #점수
cnt = 1 #id
now=datetime.datetime.now() #현재 시점의 날짜
nowDatetime=now.strftime("%Y-%m-%d %H:%M:%S")
conn=sqlite3.connect("database.db")
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMERY KEY,score INTEGER,regdate text)")

pygame.init()
winHeight = 480
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("hangman game") #화면 타이틀 설정
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
LIGHT_BLUE = (102,255,255)

btn_font = pygame.font.SysFont('arial', 20) 
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 40)
word = ''
buttons = []
guessed = [] 
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]
background_1 = pygame.image.load("background/background.png") 
limbs = 0


def redraw_game_window():
    global guessed #사용자가 입력하는 단어
    global hangmanPics
    global limbs # 행맨그림 index
    win.fill(WHITE) #배경color
    
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3]) #첫번째줄 버튼
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)  #두번째줄 버튼
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK) #버튼 글씨
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK) # _ _ _ _ _ <- 이 부분
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs] #행맨그림
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
    spacedWord = '' #화면에 표시되는 word
    guessedLetters = guessed #사용자가 입력한 단어
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ ' #정답 word 길이 만큼 '_'추가하기
            for i in range(len(guessedLetters)): #사용자 입력 단어 알파벳 길이
                if word[x].upper() == guessedLetters[i]: # 정답이랑 비교해서 같다면
                    spacedWord = spacedWord[:-2] # '_'지우고
                    spacedWord += word[x].upper() + ' ' # 알파벳 추가
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y): #버튼 눌렀을 때 그 위치에 해당하는 알파벳문자 return
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    global cnt
    global background_1

    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'

    #DB insert
    c.execute("INSERT INTO users (id, score, regdate) VALUES(?,?,?)", (cnt, score,nowDatetime))
    conn.commit()
    cnt+=1

    redraw_game_window()
    pygame.time.delay(1000)

    TOPSCORE_TRUE=False
    most_score=0

    for row in c.execute("SELECT * FROM users"):
        if row[1] > most_score: #가장 높은 점수 찾기
            most_score=row[1]
            most_score_date=row[2]
            TOPSCORE_TRUE=True
        topscore_user=most_score

    if TOPSCORE_TRUE == True:
        win.fill(GREEN)
    else :
        win.blit(background_1, (0, 0)) #end 배경 color

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The word was :', 1, BLACK)
    topscore = lost_font.render("1st user : {}".format(topscore_user), 1, RED) #1등 score

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    win.blit(topscore, (winWidth / 2 - topscore.get_width() / 2, 80))

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
    buttons.append([GREEN, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생
            conn.execute("DELETE FROM users") #DB 데이터 삭제
            conn.commit()
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1]) #마우스가 클릭한거
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

c.close()
pygame.quit()
# always quit pygame when done!
