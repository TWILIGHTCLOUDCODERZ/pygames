import pygame, sys, os
import time
import random

width = 600
height = 800
white = (255,255,255)
black = (0,0,0)
clock = pygame.time.Clock()
g = 1
score = 0
fps = 13
fruits = ['watermelon', 'orange']

pygame.init()
gameDisplay = pygame.display.set_mode((width, height))
gameDisplay.fill(white)
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 32)
score_text = font.render(str(score), True, black, white)
time_font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 24)

def generate_random_fruits(fruit):
    path = os.path.join(os.getcwd(), fruit+'.png')
    data[fruit] = {
        'img' : pygame.image.load(path),
        'x' : random.randint(100, 500),
        'y' : 800,
        'speed_x' : random.randint(-10, 10),
        'speed_y' : random.randint(-80, -60),
        'throw' : False,
        't' : 0,
        'hit' : False,
    }
    if(random.random() >= 0.75):
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

pygame.display.update()

start_time = time.time()
game_duration = 30  # set game duration to 30 seconds

while True:
    gameDisplay.fill(white)
    gameDisplay.blit(score_text, (0,0))
    time_elapsed = int(time.time() - start_time)
    time_left = game_duration - time_elapsed
    if time_left < 0:  # check if time is up
        break  # end the game loop if time is up
    time_text = time_font.render("Time: "+str(time_left), True, black, white)
    gameDisplay.blit(time_text, (500, 0))

    for key,value in data.items():
        if value['throw']:
            value['x'] = value['x'] + value['speed_x']
            value['y'] = value['y'] + value['speed_y']
            value['speed_y'] += (g*value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'],value['y']))
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()
            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                path = os.path.join(os.getcwd(),'half_'+key+'.png')
                value['img'] = pygame.image.load(path)
                value['speed_x'] += 10
                score += 1
                score_text = font.render(str(score), True, black, white)
                value['hit'] = True

        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

# display the final score
if time_elapsed >= game_duration:
    gameDisplay.fill(white)
    score_text_final = font.render("Final Score: "+str(score), True, black, white)
    gameDisplay.blit(score_text_final, (150, 300))
    pygame.display.update()

    # pause for 3 seconds before quitting the game
    time.sleep(3)

    # exit pygame and python
    pygame.quit()
    sys.exit()

    # event loop to check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # update the display and tick the clock
    pygame.display.update()
    clock.tick(fps)

