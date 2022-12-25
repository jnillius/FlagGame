import pygame as pg
import os
import pandas as pd
import random 
import time

pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 900, 500
FLAG_WIDTH, FLAG_HEIGHT = 200, 120
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pg.transform.scale(pg.image.load(
    os.path.join('Assets', 'Background', 'cloudy_background.jpg')), (WIDTH, HEIGHT))
pg.display.set_caption("Flag guessing game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)
FPS = 30

sheetPath = os.path.join("information", "CleanedData.csv")
df = pd.read_csv(sheetPath, sep=',')


allNames = df['name'].values
allISO = df['iso'].values
numberOfCountries = len(allNames)

### Make in input text box
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

def LoadFlag(name):
    flag = pg.image.load(os.path.join('Assets', 'Flags', name + ".png"))
    # flag = pg.transform.scale_by(flag, 0.2) #(FLAG_WIDTH, FLAG_HEIGHT) 
    flag = pg.transform.rotozoom(flag, 0, 0.2)
    return flag, flag.get_width(), flag.get_height()

class indexation:
    def __init__(self):
        self.idx = random.randint(0, numberOfCountries-1)

    def get(self):
        return self.idx

    def randomize(self):
        self.idx = random.randint(0, numberOfCountries-1)

def draw_flag(newFlag, index):
    if newFlag:
        index.randomize()
    
    idx = index.get() 
    flag, flagWidth, flagHeight = LoadFlag(allISO[idx])

    SCREEN.blit(flag, ((WIDTH-flagWidth)/2, HEIGHT/2-flagHeight))

    randomText = HEALTH_FONT.render("This is the "+allNames[idx]+"-flag!", 1, BLACK)
    SCREEN.blit(randomText, (WIDTH - randomText.get_width() - 10, 10))


def main():
    run = True
    # text box
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box_width, input_box_height = 140, 32
    input_box = pg.Rect((WIDTH/2)-(input_box_width/2)-31, 70+(HEIGHT/2), input_box_width, input_box_height)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    index = indexation()
    newFlag = False
    answer = ''
    text = ''

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
            # Right flag?
            if newFlag:
                if (answer.lower() == allNames[index.get()].lower()):
                    Msg = HEALTH_FONT.render("You are correct! This is the flag of "+allNames[index.get()]+"!", 1, GREEN)
                else:
                    Msg = HEALTH_FONT.render("Unfortunately this is the flag of "+allNames[index.get()]+".", 1, RED)

                SCREEN.blit(Msg, (WIDTH/2 - Msg.get_width()/2 - 10, HEIGHT/2))
                pg.display.update()
                time.sleep(3)
                index.randomize()
                newFlag = False
                break
            # Render flag:
            draw_flag(newFlag, index)
            pg.display.update()
            newFlag = False

        # time.sleep(2)

        # keys_pressed = pg.key.get_pressed()

            

    main()


if __name__ == "__main__":
    main()
    pg.quit()