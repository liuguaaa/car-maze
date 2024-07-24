import math
import pygame
import gym
from gym import spaces
import numpy as np
from wall import Wall
from star import Star
from target import Target
from player import Player
import time
from collided import collided_rect,collided_circle

class CarMazeEnv(gym.Env):


    def __init__(self):
        super(CarMazeEnv,self).__init__()
        self.env_width = 1000
        self.env_height = 600
        self.time = 0

        self.walls_cnt = 0
        self.walls_pos = [] #

        self.stars_cnt = 0
        self.stars_pos = [] #

        self.target_cnt = 0
        self.targets_pos = [] #

        self.direction = 1

        self.delta_time = 10 #?
        self.time_limit = 20000

        self.seed(2)

        self.done = False
        self.player = None

        self.stars = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.episode_reward = 0
        self.rewards = list()


        low = np.array([
            #position
            50,
            25,
            #angle
            0,
            #agent_velocity
            -140,
            #rotate_velocity
            -220,
        ])


        high = np.array([
            #position
            975,
            575,
            #angle
            math.pi,
            #agent_velocity
            140,
            #rotate_velocity
            220,
        ])
        self.action_space = spaces.Box(0,180,shape=(1, ))
        self.observation_space = spaces.Box(low,high)

#        self.seed()
        self.state = None

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 600))
        self.load()
        self.screen.fill("black")

        pygame.display.flip()
        self.clock.tick(20)


    def load(self):

        with open('level1.txt','r') as fin:
            self.walls_cnt = int(fin.readline())
            for i in range(self.walls_cnt):
                x, y, width, height = map(int,fin.readline().split())
                self.walls_pos.append((x,y,width,height))
            self.load_walls(self.walls_pos)

            self.stars_cnt = int(fin.readline())
            for i in range(self.stars_cnt):
                x, y = map(int,fin.readline().split())
                self.stars_pos.append((x,y))
            self.load_stars(self.stars_pos)

            self.targets_cnt = int(fin.readline())
            for i in range(self.targets_cnt):
                x , y = map(int,fin.readline().split())
                self.targets_pos.append((x,y))
            self.load_targets(self.targets_pos)

            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)

    def step(self,action):
        action_1 = action[0]
        action_1 = int(action_1 / 45)

        self.player.update(action_1)

        print("angle",self.player.forward_angle)

        print("cos",math.cos(math.pi * self.player.forward_angle / 180))

        reward = 0

        self.time += self.delta_time


        if (pygame.sprite.spritecollide(self.player,self.walls,False)):
                self.done = True
                reward -= 100
        if self.time >= self.time_limit:
            self.done = True

        if pygame.sprite.spritecollide(self.player,self.stars,True):
            self.stars_cnt -= 1
            reward += 50

        if pygame.sprite.spritecollide(self.player,self.targets,True) and self.stars_cnt == 0:
            self.rewards += 200
            self.done = True

        self.episode_reward += reward

        if self.done:
                print('episode_reward ={}'.format(self.episode_reward))
                print('agent_pos={}, forward_angle={}, agent_velocity={} ,agent_rotate_velocity={}'.format(self.player.rect.center,
                                                                                                                   self.player.forward_angle,
                                                                                                                   self.player.move_velocity,
                                                                                                                   self.player.rotate_velocity
                                                                                                            ))

                self.rewards.append(self.episode_reward)

        self.state = np.array(
            [
                self.player.rect.center[0],
                self.player.rect.center[1],
                self.player.forward_angle,
                self.player.move_velocity,
                self.player.rotate_velocity
             ])

        self.render()

        return self.state, reward, self.done, \
               {
                   "agent_pos": self.player.rect.center,
                   "angle": self.player.forward_angle,
                   "agent_velocity": self.player.move_velocity,
                   "rotate_velocity": self.player.rotate_velocity,
               }

    def reset(self):

        self.done = False
        self.state = np.array(
            [
             150,
             420,
             0,
             0,
             0
             ])

        self.time = 0
        self.episode_reward = 0
        self.rewards = list()


        self.walls_pos.clear()
        self.stars_pos.clear()
        self.targets_pos.clear()
        with open('level1.txt', 'r') as fin:
            self.walls_cnt = int(fin.readline())
            for i in range(self.walls_cnt):
                x, y, width, height = map(int, fin.readline().split())
                self.walls_pos.append((x, y, width, height))

            self.stars_cnt = int(fin.readline())
            for i in range(self.stars_cnt):
                x, y = map(int, fin.readline().split())
                self.stars_pos.append((x, y))

            self.targets_cnt = int(fin.readline())
            for i in range(self.targets_cnt):
                x, y = map(int, fin.readline().split())
                self.targets_pos.append((x, y))


            self.load_stars(self.stars_pos)
            self.load_targets(self.targets_pos)

        #self.seed(20)
        self.load_player(150,420,0)

        return np.array(self.state,dtype=np.float32)

    def render(self):
        self.screen.fill("black")
        self.stars.update()
        self.stars.draw(self.screen)

        self.targets.update()
        self.targets.draw(self.screen)

        self.walls.update()
        self.walls.draw(self.screen)


        self.player.image.set_colorkey("black")
        self.screen.blit(self.player.image,self.player.rect)
        self.clock.tick(20)


        pygame.display.flip()


    def load_walls(self,walls):
        self.walls.empty()
        for x,y,width,height in walls:
            wall = Wall(x,y,width,height)
            wall.add(self.walls)

    def load_stars(self,stars):
        self.stars.empty()
        for x,y in stars:
            star = Star(x,y)
            star.add(self.stars)

    def load_targets(self,targets):
        self.targets.empty()
        for x,y in targets:
            target = Target(x,y)
            target.add(self.targets)

    def load_player(self,center_x,center_y,forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x,center_y,forward_angle)







