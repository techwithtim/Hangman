#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random

pygame.init()
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth, winHeight))


# Add the following function for the game-over screen

def game_over_screen(winner=False):
    global limbs
    global guessed
    global buttons
    global word

    win.fill(GREEN)
    pygame.time.delay(1000)

    if winner:
        message = 'WINNER!'
    else:
        message = 'You Lost'

    label = lost_font.render(message, 1, BLACK)
    word_txt = lost_font.render(f'The phrase was: {word.upper()}', 1, BLACK)
    play_again_btn = btn_font.render('Play Again', 1, BLACK)

    win.blit(word_txt, (winWidth / 2 - word_txt.get_width() / 2, 295))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    win.blit(play_again_btn, (winWidth / 2 - play_again_btn.get_width() / 2, 350))
    pygame.display.update()

    # Wait for user input to play again
    waiting_for_input = True
    play_again_btn_rect = play_again_btn.get_rect(topleft=(winWidth / 2 - play_again_btn.get_width() / 2, 350))
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and play_again_btn_rect.collidepoint(event.pos)):
                waiting_for_input = False
    reset()



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
            click_pos = pygame.mouse.get_pos()
            letter = buttonHit(click_pos[0], click_pos[1])
            if letter is not None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        game_over_screen()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        game_over_screen(True)

pygame.quit()


# always quit pygame when done!
