#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random
import sqlite3
from datetime import datetime
import winsound #사운드 출력 필요 모듈
import time #타임 모듈
import threading #쓰레드 모듈

pygame.init()

cnt = 1 #id
conn=sqlite3.connect("database.db") #DB 연결
c=conn.cursor() #커서 연결
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMERY KEY,score_time INTEGER)") #DB 테이블 생성

winHeight = 480 #창 세로 픽셀 길이
winWidth = 700 #창 가로 픽셀 길이
win=pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("hangman game") #화면 타이틀 설정

##########colors##########
BLACK = (0,0, 0)
WHITE = (255,255,255)
ORANGE = (255,127,39)
YELLOW =(255,242,0)

##########fonts##########
btn_font = pygame.font.SysFont('arial', 20) 
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 40)
#힌트 폰트 설정
hint_font = pygame.font.SysFont('arial', 30)

word = ''
buttons = []
guessed = [] 
hangmanPics = [pygame.image.load('hang_picture/hangman0.png'), pygame.image.load('hang_picture/hangman1.png'),pygame.image.load('hang_picture/hangman2.png'), pygame.image.load('hang_picture/hangman3.png'),pygame.image.load('hang_picture/hangman4.png'), pygame.image.load('hang_picture/hangman5.png'), pygame.image.load('hang_picture/hangman6.png')]
background_1 = pygame.image.load("background/background_1.png")
background_2 = pygame.image.load("background/background_2.png")
level_button = []
limbs = 0
time_out=[] # 시간 들어갈 리스트
#힌트버튼사진
hb = pygame.image.load('hint.png')
#이미지크기변경
hintb = pygame.transform.scale(hb, (50,50))



#특정 범위 내의 좌표 마우스 클릭시 작동하는 클래스
class hintbutton():
    #생성자
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    #마우스 좌표가 범위 내에 있을 때 True 반환
    def isin(self,pos):
        if pos[0]>self.x and pos[0]<self.width:
            if pos[1]>self.y and pos[1]<self.height:
                return True

#힌트버튼 생성
hButton = hintbutton(640,415,690,465)

def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    global start
    #힌트버튼 변수 선언
    global hintb
    win.fill(WHITE)
    # 시간 함수
    global delta_time

    now_time = datetime.now()
    delta_time = (now_time-start).total_seconds()
    
    timer = btn_font.render("time : {}".format(str(int(delta_time))),True,BLACK)
    win.blit(timer,(10,450))

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

    #화면에 힌트 버튼 그림 출력
    win.blit(hintb, (640,415))


    pic = hangmanPics[limbs] #행맨그림
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()


    
def level():#바뀜
    win.fill(WHITE)
    font = pygame.font.SysFont("monospace", 24)  #폰트 설정
    text = font.render("LEVEL 1 - animal(easy ver.)",True, BLACK)  #텍스트가 표시된 Surface를 만듦
    win.blit(text,(160,100))
    text = font.render("LEVEL 2 - animal(hard ver.)",True,BLACK)  #텍스트가 표시된 Surface를 만듦
    win.blit(text,(160,150))
    text = font.render("LEVEL 3 - location(easy ver.)",True,BLACK)  #텍스트가 표시된 Surface를 만듦
    win.blit(text,(160,200))
    text = font.render("LEVEL 4 - location(hard ver.)",True,BLACK)  #텍스트가 표시된 Surface를 만듦
    win.blit(text,(160,250))
    text = font.render("LEVEL 5 - food(easy ver.)",True,BLACK)  #텍스트가 표시된 Surface 를 만듦
    win.blit(text,(160,300))
    text = font.render("LEVEL 6 - food(hard ver.)",True,BLACK)  #텍스트가 표시된 Surface를 만듦
    win.blit(text,(160,350))
    pygame.display.update()
    
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_ticks = pygame.time.get_ticks()
                clickPos = pygame.mouse.get_pos()
                x, y = clickPos
                if y >= 80 and y <= 120:
                    if x >= 150 and x <= 500:
                        return 'stage/animal_easy.txt'
                if y >= 130 and y <= 170:
                    if x >= 150 and x <= 500:
                        return 'stage/animal_hard.txt'
                if y >= 180 and y <= 220:
                    if x >= 150 and x <= 500:
                        return 'stage/location_easy.txt'
                if y >= 230 and y <= 270:
                    if x >= 150 and x <= 500:
                        return 'stage/location_hard.txt'
                if y >= 280 and y <= 320:
                    if x >= 150 and x <= 500:
                        return 'stage/food_easy.txt'
                if y >= 330 and y <= 380:
                    if x >= 150 and x <= 500:
                        return 'stage/food_hard.txt'
    
def randomWord(w):#바뀜
    global start
    file = open(w)#바뀜
    f = file.readlines()
    i = random.randrange(0, len(f)-1)
    start = 0
    start = datetime.now() #스타트

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

    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'

    redraw_game_window()
    pygame.time.delay(1000)

    if winner == True:
        win.blit(background_1,(0, 0))
        winsound.PlaySound('./sound/pass.wav',winsound.SND_FILENAME)
        label = lost_font.render(winTxt, 1, BLACK)
         #DB insert
        c.execute("INSERT INTO users (id, score_time) VALUES(?,?)", (cnt,int(delta_time)))
        conn.commit()
        cnt+=1
    else:
        win.blit(background_2, (0, 0))
        winsound.PlaySound('./sound/nonpass.wav',winsound.SND_FILENAME)
        label = lost_font.render(lostTxt, 1, BLACK)

    c.execute("SELECT * FROM users")

    cf=c.fetchone()
    most_score=cf[1]

    for row in c.fetchall():
        if row[1] <= most_score: # 가장 초가 작은 사람
            most_score=row[1]
    
    topscore_user=most_score

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The word was :', 1, BLACK)
    topscore = lost_font.render("1st user : {}sec.".format(topscore_user), 1, ORANGE) #1등 score

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
    word = randomWord(w)

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
    buttons.append([YELLOW, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

w = level()#바뀜
word = randomWord(w)#바뀜
#랜덤한 단어의 공백을 제거
hintword = word.replace(' ', '')
#공백제거한 단어의 알파벳 하나를 랜덤으로 추출
a = random.choice(hintword)

#힌트
def Hint():
    global a
    while True:
        #변수 a가 이미 추측한 알파벳이라면
        if a in guessed:
            #변수 a 다시 지정
            a = random.choice(hintword)
        #아니라면
        else:
            #변수 t에 a를 대문자로 변환한 것 저장
            t = a.upper()
            #반복문 종료
            break
    return t


inPlay = True#바뀜


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
            #힌트버튼 클릭하면
            if hButton.isin(clickPos):
                #힌트버튼 클릭시 소리재생
                winsound.PlaySound('./sound/click.wav',winsound.SND_FILENAME)
                #힌트생성
                t = Hint()
                #텍스트 객체 생성, t = 텍스트내용, True = Anti-aliasing 사용, BLACK = 텍스트컬러
                text = hint_font.render(t, True, BLACK)
                #화면에 텍스트객체 출력
                win.blit(text, (660,380))
                #화면 업데이트
                pygame.display.update()

            if letter != None:
                winsound.PlaySound('./sound/click.wav',winsound.SND_FILENAME) #버튼 클릭시 소리 재생
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        time_out.append(delta_time) #리스트 시간 추가
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        time_out.append(delta_time) # 끝날때 리스트에 흐른 시간 추가
                        end(True)


c.close()
pygame.quit()