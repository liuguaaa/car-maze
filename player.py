import pygame
import math
class Player(pygame.sprite.Sprite):
    def __init__(self,center_x,center_y,forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50
        self.forward_angle = forward_angle #顺时针角度 第四象限
        self.image_source = pygame.image.load("images/car.png").convert()
        self.image = pygame.transform.scale(self.image_source,(self.width,self.height))
        self.image = pygame.transform.rotate(self.image,-self.forward_angle)
        #self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x,center_y)
        self.last_time = pygame.time.get_ticks() #当前时刻 毫秒
        self.delta_time = 0 #相邻两帧的时间间隔

        self.move_velocity_limit = 220 #移动速度上限
        self.move_velocity = 0
        self.move_acc = 300
        self.rotate_velocity_limit = 140
        self.rotate_velocity = 0
        self.friction = 0.9

    def update_delta_time(self):
        cur_time = pygame.time.get_ticks()
        self.delta_time = (cur_time - self.last_time) / 1000
        self.last_time = cur_time
    def update(self,action_1):
        self.update_delta_time()
        self.input(action_1)
        self.move()

    def rotate(self,direction=1):
        self.forward_angle += self.rotate_velocity * self.delta_time * direction
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        #self.image.set_colorkey("black")
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def move(self,direction=1):
        if direction == 1 and abs(self.move_velocity) > 50:
            self.rotate(direction)
        vx = self.move_velocity * math.cos(math.pi * self.forward_angle / 180) * direction
        vy = self.move_velocity * math.sin(math.pi * self.forward_angle / 180) * direction
        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time
        #self.rect.x += self.move_velocity * self.delta_time
        if direction == -1 and abs(self.move_velocity) > 50:
            self.rotate(direction)
    def input(self,action_1):
        if action_1 == 0:
            self.move_velocity += self.move_acc * self.delta_time
            self.move_velocity = min(self.move_velocity, self.move_velocity_limit)

        # elif action_1 == 1:
        #     self.move_velocity -= self.move_acc * self.delta_time
        #     self.move_velocity = max(self.move_velocity, -self.move_velocity_limit)

        else:
            self.move_velocity = int(self.move_velocity * self.friction)

        sign = 1
        if self.move_velocity < 0:
            sign = -1

        if action_1 == 1:
            self.rotate_velocity = self.rotate_velocity_limit * sign

        elif action_1 == 2:
            self.rotate_velocity = -self.rotate_velocity_limit * sign

        else: self.rotate_velocity = 0

    # def crash(self):
    #     self.crash_sound.play()
    #     self.move(-1)
    #     if self.move_velocity >= 0:
    #         self.move_velocity = min(-self.move_velocity,-100)
    #     else:
    #         self.move_velocity = max(self.move_velocity,100)
    #     self.rotate_velocity *= -1