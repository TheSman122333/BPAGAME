import pygame as pg
import random
from enemy_data import ENEMY_SPAWN_DATA

class World():
  def __init__(self):
    self.level = 1
    self.enemy_list = []
    self.spawned_enemies = 0
    self.killed_enemies = 0
    #init
  def process_enemies(self):
    enemies = ENEMY_SPAWN_DATA[self.level - 1]
    for enemy_type in enemies:
      enemies_to_spawn = enemies[enemy_type]
      for enemy in range(enemies_to_spawn):
        self.enemy_list.append(enemy_type)
      #checking and appending enemies to spawn. main.py will read it and spawn them
    random.shuffle(self.enemy_list)
    #CHANCE/LUCK, it shuffles the order so that the enemies don't come out in the same order every time

  def check_level_complete(self):
    if (self.killed_enemies) == len(self.enemy_list):
      return True
      #if killed enemies is equal to the amount of enemies in the list, then the level is complete.
  def reset_level(self):
    #reset enemy variables
    self.enemy_list = []
    self.spawned_enemies = 0
    self.killed_enemies = 0
    #reset level variables
