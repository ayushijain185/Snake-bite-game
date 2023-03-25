import pygame
import random
import os

pygame.mixer.init()

pygame.init()



screen_width =700
screen_height =600

gamewindow=pygame.display.set_mode((screen_width,screen_height))


bgimg=pygame.image.load("snake.png")
bgimg=pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

welimg=pygame.image.load("greencolor.png")
welimg=pygame.transform.scale(welimg, (screen_width, screen_height)).convert_alpha()

overimg=pygame.image.load("greencolor.png")
overimg=pygame.transform.scale(overimg, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snake Game")
pygame.display.update()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (56, 147, 56)

font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()


def plot_snake(gamewindow,color,snk_list, snake_size):
    for x ,y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])

def scorescreen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gamewindow.blit(screen_text, [x, y])

def welcome():
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play()
    gameexit=False
    while not gameexit:
        gamewindow.fill(black)
        gamewindow.blit(welimg, (0, 0))
        scorescreen("Welcome To The Snake Bit",white,100,200)
        scorescreen("Press Enter........", white, 160, 250)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameexit=True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

def gameloop():
    gameexit = False
    gameover = False
    snake_x = 40
    snake_y = 40
    snake_size = 10
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_len = 1
    fps = 30
    init_velocity = 5
    score = 0
    food_x = random.randint(2, screen_width - 2)
    food_y = random.randint(2, screen_height - 2)


    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore=f.read()
        f.close()

    while not gameexit:
        if gameover:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
                f.close()
            gamewindow.fill(black)
            gamewindow.blit(overimg, (0, 0))
            scorescreen("Game Over!!!", white, 105, 150)
            scorescreen(f"Your Score : {score}", white, 100, 200)
            scorescreen(f"Highest Score : {highscore}", white, 100, 250)
            scorescreen("Press Enter to Continue", white, 100, 500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameexit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameexit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                pygame.mixer.music.load('turn.mp3')
                pygame.mixer.music.play()
                food_x = random.randint(2, screen_width - 5)
                food_y = random.randint(2, screen_height - 40)
                snk_len += 5
                if score > int(highscore):
                    highscore = score


            gamewindow.fill(white)
            gamewindow.blit(bgimg,(0,0))
            scorescreen("score : " + str(score), red, 5, 5)
            scorescreen(" highscore : " + str(highscore), red, 205, 5)
            pygame.draw.rect(gamewindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_len:
                del snk_list[0]

            if head in snk_list[:-1]:
                gameover=True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                gameover = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()
            plot_snake(gamewindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()