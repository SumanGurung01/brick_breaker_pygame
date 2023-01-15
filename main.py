"""
    Date : Sat Dec 31 2022 19:25:15 GMT+0530 (India Standard Time)
    Author : Suman Gurung
    Description : Brick Breaker using pygame
"""

import pygame
import random

pygame.init()

# CONSTANTS
WIN_HEIGHT,WIN_WIDTH = 700,700

WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

SCORE_FONT = pygame.font.SysFont("comicsans",25)

BRICK_COLORS = [(241,148,138),(195,155,211),(127,179,213),(118,215,196),(247,220,111),(229,152,102),(244,246,247),(255,0,0),(0,255,0),(0,0,255),(33,47,60),(10,255,0)]



# DRAW ON WINDOW WHILE GAME IS ON
def draw(win,paddle,bricks,ball,lives):
    win.fill((0,0,0))
    
    for brick in bricks:
        brick_sprite = pygame.transform.scale(brick.image , (100,20))
        win.blit(brick_sprite , (brick.x , brick.y))

    for life in lives:
        life_sprite = pygame.transform.scale(life.image , (30,30))
        win.blit(life_sprite , (life.x , life.y))

    paddle_sprite = pygame.transform.scale(paddle.image , (150,15))
    win.blit(paddle_sprite , (paddle.x , paddle.y))
    
    
    ball_sprite = pygame.transform.scale(ball.image , (20,20))
    win.blit(ball_sprite, (ball.x,ball.y))

    pygame.display.update()


# BALL MOVEMENTS
def handle_ball_movement(ball,paddle,bricks):
    # left window
    if ball.x + 2*ball.radius > WIN_WIDTH:
        ball.x_vel *= -1  
    # right window
    if ball.x < 0:
        ball.x_vel *= -1
    
    # top window
    if ball.y<= 0:
        ball.y_vel = 3

    # paddle
    if ball.y + 2*ball.radius >= paddle.y:
        if ball.x+ball.radius >= paddle.x and ball.x+ball.radius <= paddle.x+paddle.width: 
            if (ball.x + ball.radius > paddle.x and ball.x+ball.radius < paddle.x+(paddle.width//3)) or ( ball.x + ball.radius > paddle.x+(paddle.width*2//3) and ball.x + ball.radius < paddle.x + paddle.width):
                if ball.x_vel>0:
                    ball.x_vel = 6     
                else:
                    ball.x_vel = -6
            else:
                if ball.x_vel > 0 :
                    ball.x_vel = 3
                else :
                    ball.x_vel = -3
            ball.y_vel = -3

    # brick
    for i , brick in enumerate(bricks , start=0):
        if ball.y + ball.radius >= brick.y and ball.y+ball.radius <= brick.y+brick.height: 
            if ball.x <= brick.x+brick.width:
                ball.x_vel = 3
            if ball.x+ 2*ball.radius >= brick.x:
                ball.x_vel = -3
        
        if ball.y <= brick.y+brick.height:
            if ball.x+ball.radius >= brick.x and ball.x+ball.radius <= brick.x+brick.width:
                ball.y_vel = 3
                bricks.pop(i)       
    
    ball.move()


# PADDLE MOVEMENT
def handle_paddle_movement(keys,paddle):
    if keys[pygame.K_a] and paddle.x >= 0:
        paddle.move(left=True)
    if keys[pygame.K_d] and paddle.x + paddle.width <= WIN_HEIGHT:
        paddle.move(left=False)
    

# BRICK CLASS
class Brick:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 20
        self.image = pygame.image.load(f"sprite/brick{random.randrange(1,9)}.png")

# PADDLE CLASS
class Paddle:
    
    def __init__(self , x,y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 15
        self.image = pygame.image.load("sprite/paddle.png")

    def move(self, left = True):
        if left:
            self.x-=5
        else:
            self.x+=5


# BALL CLASS
class Ball:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x_vel = 3
        self.y_vel = 3
        self.image = pygame.image.load("sprite/ball.png")
        self.radius = 10


    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


# RESET 
def reset(ball , paddle):
    ball.x = WIN_WIDTH//2
    ball.y = WIN_HEIGHT//2


# GAMEOVER
def gameover(win , won):
    win.fill((0,0,0))
    if won:
        text = SCORE_FONT.render("YOU WON", 1 , (255,255,255))
    else:
        text = SCORE_FONT.render("GAMEOVER", 1 , (255,255,255))
    
    win.blit(text,(WIN_WIDTH//2-50, WIN_HEIGHT//2))
    pygame.display.update()


class Lives:    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("sprite/life.png")


# MAIN
def main():

    clock = pygame.time.Clock()
    run = True 
    
    lives = []

    for i in range(3):
        life = Lives(WIN_WIDTH//2 + 30*i - 50, WIN_HEIGHT//2)
        lives.append(life)

    x_loc , y_loc = 0,0
    # BRICKS 
    bricks = []
    for i in range(0,3):
        y_loc = i*20
        for j in range(0,7):
            brick = Brick(x_loc , y_loc)
            bricks.append(brick)
            x_loc+=100
        x_loc = 0
    
    #PADDLE
    paddle = Paddle(WIN_WIDTH//2 - 150//2 ,685)

    # BALL
    ball = Ball(WIN_WIDTH//2 , WIN_HEIGHT//2)

    cancel = 0

    while run:
        clock.tick(60)

        draw(WIN , paddle , bricks , ball , lives)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cancel = 1
                run = False

        keys = pygame.key.get_pressed() 

        handle_paddle_movement(keys,paddle) 
        handle_ball_movement(ball,paddle,bricks)

        if ball.y+ball.radius >= WIN_HEIGHT:
            lives.pop(len(lives)-1)
            reset(ball,paddle)
        
        if len(lives) == 0 or len(bricks) == 0:
            run = False
    
    if cancel == 1:
         pygame.quit()
    else:
        run = True  
        while run:
            if len(lives) == 0:
                gameover(WIN , 0)
            else:
                gameover(WIN , 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
         
        pygame.quit()
   


if __name__=="__main__":
    main()
