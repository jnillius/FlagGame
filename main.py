import pygame as pg
import os
import pandas as pd
import random 
import time

# Game parameters
WIDTH, HEIGHT = 900, 500
FPS = 30

# Game constants
pg.font.init()
pg.mixer.init()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
RESULT_FONT = pg.font.Font(None, 32)
SCORE_FONT = pg.font.Font(None, 32)
pg.display.set_caption("Flag guessing game!")
BACKGROUND = pg.transform.scale(pg.image.load(
    os.path.join('Assets', 'Background', 'cloudy_background.jpg')), (WIDTH, HEIGHT))
# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
# Get cleaned data
sheetPath = os.path.join("information", "CleanedData.csv")
df = pd.read_csv(sheetPath, sep=',')
allNames = df['name'].values
allISO = df['iso'].values
numberOfCountries = len(allNames)

class indexation:
    def __init__(self):
        self.idx = random.randint(0, numberOfCountries-1)

    def get(self):
        return self.idx

    def randomize(self):
        self.idx = random.randint(0, numberOfCountries-1)

def LoadFlag(iso):
    flag = pg.image.load(os.path.join('Assets', 'Flags', iso + ".png"))
    flag = pg.transform.rotozoom(flag, 0, 0.2)
    if (flag.get_height()> HEIGHT/2):
        flag = pg.transform.rotozoom(flag, 0, (HEIGHT/2.1)/flag.get_height())
    return flag, flag.get_width(), flag.get_height()

def draw_flag(index):
    flag, flagWidth, flagHeight = LoadFlag(allISO[index.get()])
    SCREEN.blit(flag, ((WIDTH-flagWidth)/2, (HEIGHT/2)-flagHeight))

def main():
    # Initializations
    run = True
    index = indexation()
    newFlag = False
    answer = ''
    text = ''
    score = 0 
    streak = 0
    # Text box
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box_width, input_box_height = 140, 32
    input_box = pg.Rect((WIDTH/2)-(input_box_width/2)-31, 70+(HEIGHT/2), input_box_width, input_box_height)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            if event.type == pg.KEYDOWN:    
                if event.key == pg.K_RETURN:
                    answer = text
                    text = ''
                    newFlag = True
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            
            # Render: Background
            SCREEN.blit(BACKGROUND, (0, 0))
            # Render: Current input text
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            SCREEN.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pg.draw.rect(SCREEN, color, input_box, 2)
            # Check guess
            if newFlag:
                if (answer.lower() == allNames[index.get()].lower()):
                    Msg = RESULT_FONT.render("You are correct! This is the flag of "+allNames[index.get()]+"!", 1, GREEN)
                    score += 1
                    streak += 1
                else:
                    Msg = RESULT_FONT.render("Unfortunately this is the flag of "+allNames[index.get()]+".", 1, RED)
                    streak = 0

                SCREEN.blit(Msg, ((WIDTH/2) - (Msg.get_width()/2) - 10, (HEIGHT/2)+20))
            # Render flag:
            draw_flag(index)
            # Cheating
            cheatingText = RESULT_FONT.render("This is the flag of "+allNames[index.get()]+"!", 1, BLACK)
            SCREEN.blit(cheatingText, (WIDTH - cheatingText.get_width() - 10, HEIGHT-35))
            # Render score:
            scoreText = SCORE_FONT.render("Score:", 1, BLACK)
            streakText = SCORE_FONT.render("Streak:", 1, BLACK)
            alignWidth = min(scoreText.get_width(), streakText.get_width())
            SCREEN.blit(scoreText, (WIDTH - alignWidth - 50, 10))
            SCREEN.blit(streakText, (WIDTH - alignWidth - 50, 40))
            scoreTextNum = SCORE_FONT.render(str(score), 1, BLACK)
            SCREEN.blit(scoreTextNum, (WIDTH - scoreTextNum.get_width() - 10, 10))
            streakTextNum = SCORE_FONT.render(str(streak), 1, BLACK)
            SCREEN.blit(streakTextNum, (WIDTH - streakTextNum.get_width() - 10, 40))
            # Update display
            pg.display.update()
            # Reset bool
            if newFlag:
                index.randomize()
                time.sleep(3)
            newFlag = False

    main()


if __name__ == "__main__":
    main()
    pg.quit()
