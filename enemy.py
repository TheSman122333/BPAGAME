import pygame as pg
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA
from world import World
#imports
world = World()
#defining world class
class Enemy(pg.sprite.Sprite):
  def __init__(self, enemy_type, waypoints, images):
    pg.sprite.Sprite.__init__(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoint = 1
    self.health = ENEMY_DATA.get(enemy_type)["health"]
    self.speed = ENEMY_DATA.get(enemy_type)["speed"]
    self.angle = 0
    self.original_image = images.get(enemy_type)
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos
    self.mask = pg.mask.from_surface(self.image)
    self.atend = False
    #init variables
    
  def update(self):
    if self.atend == False:
      self.move()
      self.rotate()
      #move/rotate (if they are not at end)

    
  def move(self):
    #define a target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
      self.atend = False
      #how much do I need to move more?
    else:
      #enemy has reached the end of the path
      self.atend = True
      self.kill()
    # calc dist
    dist = self.movement.length()
    #print(dist)
    # check if dist is greater than speed
    if dist >= self.speed:
      self.pos += self.movement.normalize() * self.speed
    else:
      if dist != 0:
        #set speed to distance
        self.pos += self.movement.normalize() * dist
        self.target_waypoint += 1
    

  def rotate(self):
    # calc dist to next wayp
    dist = self.target-self.pos
    # use dist for angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    # rotate
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

    #Calculates angle of the waypoints, and rotates the image accordingly