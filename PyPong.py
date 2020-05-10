'''
Created on Aug 30, 2012

@author: bearpaw7
'''
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
 
# Import a library of functions called 'pygame'

import math
import pygame
from random import randrange
import os

# Define the colors we will use in RGB format
black = (  0,  0,  0)
white = (255,255,255)
blue =  (  0,  0,255)
red =   (255,  0,  0)

pi = math.pi

class Ball:
    base_velocity = 5.5
    def __init__(self,x,y,degrees, height, width):
        self.position=[x,y]
        self.direction=degrees
        self.radius=9
        self.velocity=self.base_velocity
        pygame.mixer.init()
        self.redsound=None
        self.bluesound=None
        self.tink=None
        self.height = height
        self.width = width

    def top(self):
        return self.position[1]-self.radius
    def bottom(self):
        return self.position[1]+self.radius
    def left(self):
        return self.position[0]-self.radius
    def right(self):
        return self.position[0]+self.radius

    def collide(self, paddle):
        if paddle.color == red:
            if self.left()>=paddle.left() and self.left()<=paddle.right():
                if self.position[1]>=paddle.top() and self.position[1]<=paddle.bottom():
                    self.velocity=min((self.velocity+self.velocity*0.20),paddle.thick)
                    self.position[0]=paddle.right()+self.radius
                    self.direction=randrange(0,120)+300
        if paddle.color == blue:
            if self.right()<=paddle.right() and self.right()>=paddle.left():
                if self.position[1]>=paddle.top() and self.position[1]<=paddle.bottom():
                    self.velocity=min((self.velocity+self.velocity*0.20),paddle.thick)
                    self.position[0]=paddle.left()-self.radius
                    self.direction=randrange(120,240)

    def bounceHorizontal(self):
        self.direction=(int)(self.direction)%360
        self.velocity=self.velocity-self.velocity*0.25
        if self.direction<90:
            self.direction=360-self.direction
        elif self.direction<180:
            self.direction=270-(self.direction-90)
        elif self.direction<270:
            self.direction=180-(self.direction-180)
        else:
            self.direction=360-self.direction

    def update(self,paddle1,paddle2):
        self.position[0]+=self.velocity*math.cos(self.direction*pi/180)
        self.position[1]-=self.velocity*math.sin(self.direction*pi/180)
        if self.top()<=0:
            self.bounceHorizontal()
            self.position[1]=self.radius
            self.velocity=min((self.velocity+self.velocity*0.20),paddle1.thick)
        elif self.bottom()>=self.height:
            self.bounceHorizontal()
            self.position[1]=self.height-self.radius
            self.velocity=min((self.velocity+self.velocity*0.20),paddle1.thick)
        if self.right()<0:
            self.position=[self.width/2,self.height/2]
            self.direction=0
            self.velocity=self.base_velocity
            paddle2.points+=1
        elif self.left()>self.width:
            self.position=[self.width/2,self.height/2]
            self.direction=180
            self.velocity=self.base_velocity
            paddle1.points+=1
        self.collide(paddle1)
        self.collide(paddle2)

        return self.position, self.velocity, self.direction

    def draw(self,screen):
        pygame.draw.circle(screen,black,[(int)(self.position[0]),(int)(self.position[1])],self.radius,0)

class Paddle:
    def __init__(self,_top,_column,_length,_color, height, width):
        # [x,y] is top left coordinate of paddle
        self.head=_top
        self.column=_column
        self.length=_length
        self.thick=14
        self.activity=0
        self.color=_color
        self.points=0
        self.height = height
        self.width = width

    def top(self):
        return self.head
    def bottom(self):
        return self.top()+self.length
    def left(self):
        return self.column-self.thick/2
    def right(self):
        return self.column+self.thick/2

    def score(self):
        return self.points.__str__()

    def setActivity(self,event, ai_decision=None):
        if self.color == red:
            self.activity=ai_decision
        elif self.color == blue:
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.activity=0
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.activity=0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.activity=1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.activity=-1

    def update(self):
        # move player bars
        if self.activity>0 and self.top() > 5:
            self.head-=5
        elif self.activity<0 and self.bottom() < self.height - 5:
            self.head+=5

        return self.head

    def draw(self,screen):
        pygame.draw.line(screen,self.color,[self.column,self.top()],[self.column,self.bottom()],self.thick)

class PyPong:
    def __init__(self, screen, ball, player1, player2, width, height):
        print('Initiated PyPong')
        self.screen = screen
        self.ball = ball
        self.player1 = player1
        self.player2 = player2
        self.width = width
        self.height = height

    def step(self, action):

        for event in pygame.event.get():  # User did something
            # If user clicked close
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True  # Flag that we are done so we exit this loop
            self.player2.setActivity(event)

        if action == 0:
            action = -1

        self.player1.setActivity(None, action)

        player1_pos = self.player1.update()
        player2_pos = self.player2.update()

        ball_pos, ball_velocity, ball_direction = self.ball.update(self.player1, self.player2)
        #    print ball.position
        self.screen.fill(white)

        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen)

        font = pygame.font.Font(None, 25)

        # Render the text. "True" means anti-aliased text.
        # Black is the color. This creates an image of the
        # letters, but does not put it on the screen
        text = font.render("Reinforcement Learning Pong by Aswin Visva, original game built by Beef", True, black)
        score1text = font.render(self.player1.score(), True, red)
        score2text = font.render(self.player2.score(), True, blue)

        # Put the image of the text on the screen at 250x250
        self.screen.blit(text, [50, 300])
        self.screen.blit(score1text, [50, 0])
        self.screen.blit(score2text, [650, 0])

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

        return player1_pos, ball_pos[0], ball_pos[1], ball_velocity, ball_direction, int(self.player1.score()), int(self.player2.score())
