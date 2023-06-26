import numpy as np
import os
import pandas as pd
import pygame as pg
import random 
import time
from difflib import SequenceMatcher

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
HINT_FONT = pg.font.Font(None, 32)
SCORE_FONT = pg.font.Font(None, 32)
pg.display.set_caption("Flag guessing game!")
BACKGROUND = pg.transform.scale(pg.image.load(
    os.path.join('Assets', 'Background', 'cloudy_background.jpg')), (WIDTH, HEIGHT))

# Colours
#WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
#YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Get cleaned data
sheet_path = os.path.join("information", "CleanedDataManuallyFixed.csv") 
df = pd.read_csv(sheet_path, sep=',', keep_default_na=False)
country_names = df['name'].values
country_isos = df['iso'].values
continents = df['region'].values
country_populations = df['population'].values

number_of_countries = len(country_names)
countries_used = number_of_countries # TODO: change this when you can play from certain region 
# countryPropability = ([1] * number_of_countries) / number_of_countries # TODO: use something like this

class Countries:
    def __init__(self):
        self.idx = random.randint(0, number_of_countries-1)
        self.weights = [1/number_of_countries] * number_of_countries

    def getCurrentIndex(self):
        return self.idx

    def update(self, correct):
        factor = 10
        if correct:
            self.weights[self.idx] /= factor
        else:
            self.weights[self.idx] *= factor
        self.randomize()

    def randomize(self):
        sum_of_weights = sum(self.weights)
        multinomial_distribution = [x/sum_of_weights for x in self.weights]
        self.idx = list(np.random.multinomial(1, multinomial_distribution)).index(1)

def loadFlag(iso):
    flag = pg.image.load(os.path.join('Assets', 'Flags', iso + ".png"))
    flag = pg.transform.rotozoom(flag, 0, 0.2)
    if (flag.get_height()> HEIGHT/2):
        flag = pg.transform.rotozoom(flag, 0, (HEIGHT/2.1)/flag.get_height())
    return flag, flag.get_width(), flag.get_height()

def drawFlag(country_index):
    flag, flagWidth, flagHeight = loadFlag(country_isos[country_index])
    SCREEN.blit(flag, ((WIDTH-flagWidth)/2, (HEIGHT/2)-flagHeight))


def getAllCountryNames():
    all_country_names = []
    for country in country_names:
        for alternatives in country.split('/'):
            all_country_names.append(alternatives)
    return all_country_names


def autocompleteCountry(guess):
    all_country_names = getAllCountryNames()
    matching_countries = []
    for country in all_country_names:
        if country.lower().startswith(guess):
            matching_countries.append(country.lower())
    if len(matching_countries) == 0:
        return getBestMatchingCountry(guess)
    elif len(matching_countries) == 1:
        return matching_countries[0]
    else:
        return extendGuess(guess, matching_countries)


def extendGuess(guess, matching_countries):
    len_shortest_country = len(min(matching_countries, key=len))
    len_guess = len(guess)
    if len_shortest_country == len_guess:
        return guess
    extend_guess = guess
    for i in range(len_guess, len_shortest_country):
        i_char = matching_countries[0][i]
        for j in range(1, len(matching_countries)):
            j_char = matching_countries[j][i]
            if not i_char == j_char:
                return extend_guess
        extend_guess += i_char
    return extend_guess


def getBestMatchingCountry(guess):
    all_country_names = getAllCountryNames()
    match_ratio = [SequenceMatcher(None, country.lower(), guess.lower()).ratio() for country in all_country_names]
    index_best_match = match_ratio.index(max(match_ratio))
    best_match = all_country_names[index_best_match]
    return best_match.lower()


def checkAnswer(guess, country_index):
    # correctCountry = country_names[country_index].lower()
    allowed_guesses = country_names[country_index].lower().split('/')
    
    for allowed_guess in allowed_guesses:
        if guess.lower() == allowed_guess.lower():
            return True
    return False

def getContinent(country_index):
    return continents[country_index]

def getPopulation(country_index):
    population = ''
    for i, j in enumerate(str(country_populations[country_index])[::-1]):
        population += j
        if i > 0 and (i+1)%3 == 0:
            population += '.'
    return population[0:-1][::-1] if population[-1] == '.' else population[::-1]

def main():
    # Hints
    show_population = True
    show_continent = True
    allow_autocomplete = True
    max_letter_clues = 1
    # Initializations
    run = True
    countries = Countries()
    guess_submitted = False
    guess = ''
    text = ''
    score = 0 
    streak = 0
    guess_correct = False
    ctrl_h_press = 0
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
                if event.key == pg.K_TAB and allow_autocomplete:
                    text = autocompleteCountry(text.lower())
                elif event.key == pg.K_DELETE:
                    text = ''
                elif event.key == pg.K_h and pg.key.get_mods() & pg.KMOD_CTRL:
                    ctrl_h_press += 1
                    hint_letter_limit = min(max_letter_clues, ctrl_h_press)
                    text = country_names[countries.getCurrentIndex()][:hint_letter_limit].lower()
                elif event.key == pg.K_RETURN:
                    guess = text
                    text = ''
                    ctrl_h_press = 0
                    guess_submitted = True
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
            if guess_submitted:
                if (checkAnswer(guess, countries.getCurrentIndex())):
                    guess_response_message = RESULT_FONT.render("You are correct! This is the flag of {}.".format(country_names[countries.getCurrentIndex()]), 1, GREEN)
                    score += 1
                    streak += 1
                    guess_correct = True
                else:
                    guess_response_message = RESULT_FONT.render("Unfortunately this is the flag of {}.".format(country_names[countries.getCurrentIndex()]), 1, RED)
                    streak = 0
                    guess_correct = False
                SCREEN.blit(guess_response_message, ((WIDTH/2) - (guess_response_message.get_width()/2) - 10, (HEIGHT/2)+20))
            # Render flag:
            drawFlag(countries.getCurrentIndex())
            # TODO: Region toggels
            
            # Cheating
            cheating_text = RESULT_FONT.render("This is the flag of {}!".format(country_names[countries.getCurrentIndex()]), 1, BLACK)
            SCREEN.blit(cheating_text, (WIDTH - cheating_text.get_width() - 10, HEIGHT-35))
            # Hints
            if show_continent:
                continent_text = HINT_FONT.render("Continent: " + getContinent(countries.getCurrentIndex()), 1, BLACK)
                SCREEN.blit(continent_text, (10, 10))
            if show_population:
                population_text = HINT_FONT.render("Population: " + str(getPopulation(countries.getCurrentIndex())), 1, BLACK)
                SCREEN.blit(population_text, (10 , 20 + HINT_FONT.get_height()))  
            # Render score:
            score_text = SCORE_FONT.render("Score:", 1, BLACK)
            streak_text = SCORE_FONT.render("Streak:", 1, BLACK)
            alignWidth = min(score_text.get_width(), streak_text.get_width())
            SCREEN.blit(score_text, (WIDTH - alignWidth - 50, 10))
            SCREEN.blit(streak_text, (WIDTH - alignWidth - 50, 40))
            scoreTextNum = SCORE_FONT.render(str(score), 1, BLACK)
            SCREEN.blit(scoreTextNum, (WIDTH - scoreTextNum.get_width() - 10, 10))
            streakTextNum = SCORE_FONT.render(str(streak), 1, BLACK)
            SCREEN.blit(streakTextNum, (WIDTH - streakTextNum.get_width() - 10, 40))
            # Update display
            pg.display.update()
            # Reset bool
            if guess_submitted:
                countries.update(guess_correct)
                time.sleep(3)
            guess_submitted = False

    main()


if __name__ == "__main__":
    main()
    pg.quit()
