import random
import sys

import pygame
from pygame.locals import QUIT

from button import Button
from enemy import Enemy
from world import World

world = World()

#import and create an instance of the world class.

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
#creates a display surface
#load images and enemies
medium = pygame.image.load('pngs/mediumtrans.png').convert_alpha()
medium = pygame.transform.scale(
    medium, (int(medium.get_width() * 0.5), int(medium.get_height() * 0.5)))
strong = pygame.image.load('pngs/strongtrans.png').convert_alpha()
strong = pygame.transform.scale(
    strong, (int(strong.get_width() * 0.4), int(strong.get_height() * 0.4)))
elite = pygame.image.load('pngs/elitetrans.png').convert_alpha()
elite = pygame.transform.scale(
    elite, (int(elite.get_width() * 0.7), int(elite.get_height() * 0.7)))
enemy_images = {
    "weak": pygame.image.load('pngs/weaktrans.png').convert_alpha(),
    "medium": medium,
    "strong": strong,
    "elite": elite
}
restart_image = pygame.image.load('pngs/restart.png').convert_alpha() #adding images assigned to variables (buttons)

begin_image = pygame.image.load(
    'pngs/continue.png').convert_alpha() #adding images assigned to variables (buttons)

bg = pygame.image.load("pngs/bg2.png").convert_alpha()
#background
pygame.display.set_caption('COSMIC GUARDIAN: LAST STAND')
shiphealth = 20
cprDecay = 0.95
answer_displayed = False

last_enemy_spawn = pygame.time.get_ticks()

enemy_group = pygame.sprite.Group()

world.process_enemies()
#initializaion


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  DISPLAYSURF.blit(img, (x, y))
#function to draw text

restart_button = Button(650, 550, restart_image, True)
begin_button = Button(500, 750, begin_image, True)  #creating buttons

last_click_time = 0
enemy_click_time = 0
enemy_damage_time = 0
game_over = False
game_outcome = 0  # -1 is loss and 1 is win
health_updated = False
health_updated2 = False
health_updated3 = False
health_updated4 = False
health_updated5 = False

pressed_keys = []
#variables

def get_pressed_keys():
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      # Add pressed key to the list
      pressed_keys.append(pygame.key.name(event.key))
  return pressed_keys
#function to get key presses

right_ans = False
level_started = False
current_time = pygame.time.get_ticks()
pick = random.randint(0, 3)
#more init
while True:
  roundNumber = world.level
  sheal = 20  #default shiphealth round 1
  sheal += sheal * (0.1 * (roundNumber * cprDecay))     #the cpr decay
  #applying shiphealth per round decay

  cpr = sheal - 20  #calculating cpr
  maxshiphealth = sheal
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
      #check for user quit
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if current_time - last_click_time >= 250:
        pos = pygame.mouse.get_pos()
        if spaceship.get_rect(
            topleft=(0, 0)).collidepoint(pos) and shiphealth < maxshiphealth:
          shiphealth += 1
          last_click_time = current_time
          #if the mouse is down, and is colliding with the spaceship, it will heal it by 4 health points a second.
    if event.type == pygame.MOUSEBUTTONDOWN and current_time - enemy_click_time >= 100:
      pos = pygame.mouse.get_pos()
      for enemy in enemy_group:
        if enemy.rect.collidepoint(pos):
          enemy.health -= 1
          if enemy.health <= 0:
            world.killed_enemies += 1
            enemy.kill()
            #KILL WRINKLER
          enemy_click_time = current_time
          print(enemy.health)
          #if mouse is down, and colliding with a enemy, it will do 10 damage a second (assuming you can click that fast)

  if game_over is False:
    if shiphealth == 0:
      game_over = True
      game_outcome = -1
    elif shiphealth < 0:
      shiphealth = 0
      game_outcome = -1
    #checking if game over and changes game_outcome accordingly.

  rany = random.randint(100, 350)
  waypoints = [(random.randint(900, 1800), rany),
               (450, 220)]  # CHANGE THESE TO CHANGE THE PATH
  #random waypoints for the enemies to go to (CHANCE/LUCK)

  DISPLAYSURF.blit(bg, (0, 0))
  spaceship = pygame.image.load('pngs/spaceship.png')
  #cursor = pygame.image.load('pngs/cursors.png')
  spaceship = pygame.transform.scale(
      spaceship,
      (int(spaceship.get_width() * 1.25), int(spaceship.get_height() * 1.25)))
  seperator = pygame.image.load('pngs/block.webp')
  seperator = pygame.transform.scale(
      seperator,
      (int(seperator.get_width() * 1.65), int(seperator.get_height() * 2.37)))
  #cursor = pygame.transform.scale(cursor, (int(
  #cursor.get_width() * 0.25), int(cursor.get_height() * 0.25)))
  seperator = pygame.transform.scale(
      seperator, (int(seperator.get_width()), int(seperator.get_height()) * 4))
  seperator = pygame.transform.rotate(seperator, 90)
  #pygame.draw.lines(DISPLAYSURF, "grey0", False, waypoints)
  enemy_group.draw(DISPLAYSURF)
  font = pygame.font.Font(None, 36)
  text = font.render(f'Ship Health: {shiphealth}', True, (255, 255, 255))
  level_text = font.render(f'Level: {world.level - 1}', True, (255, 255, 255))
  enemiestokill = font.render(
      f'Killed enemies: {world.killed_enemies}, Enemies to kill: {len(world.enemy_list)}',
      True, (255, 255, 255))
  DISPLAYSURF.blit(level_text, (0, 460))
  #DISPLAYSURF.blit(cursor, (200, 250))
  DISPLAYSURF.blit(enemiestokill, (0, 490))
  DISPLAYSURF.blit(seperator, (0, 400))
  DISPLAYSURF.blit(spaceship, (0, 0))
  #rendering images 

  if game_over is False:
    if level_started is True:
      if pygame.time.get_ticks(
      ) - last_enemy_spawn >= 1000 and world.spawned_enemies < len(
          world.enemy_list):
        enemy_type = world.enemy_list[world.spawned_enemies]
        enemy = Enemy(enemy_type, waypoints, enemy_images)
        enemy_group.add(enemy)
        world.spawned_enemies += 1
        last_enemy_spawn = pygame.time.get_ticks()

      current_time = pygame.time.get_ticks()

      for enemy in enemy_group:
        enemy.update()
        if enemy.atend is True:
          if enemy.speed == 14:
            shiphealth -= 1
            world.killed_enemies += 1
            enemy_damage_time = current_time
          if enemy.speed == 11:
            shiphealth -= 3
            world.killed_enemies += 1
            enemy_damage_time = current_time
          if enemy.speed == 8:
            shiphealth -= 6
            world.killed_enemies += 1
            enemy_damage_time = current_time
          if enemy.speed == 20:
            shiphealth -= 10
            world.killed_enemies += 1
            enemy_damage_time = current_time
            #if game is running, and last spawn was over a second ago, spawn it. it will iterate through the for loop, check if it is at the end, and if it is, it will subtract the according amount of health.
  elif game_over is True:

    if game_outcome == -1:
      #ADD AN ENDING STATEMENT " THE HUMAN RACE IS EXTINCT. TRY AGAIN? "
      font = pygame.font.Font(None, 175)
      pygame.draw.rect(DISPLAYSURF,
                       "dodgerblue", (400, 200, 1200, 800),
                       border_radius=30)
      draw_text("You Lost", font, "black", 735, 500)
      if restart_button.draw(DISPLAYSURF):
        for enemy in enemy_group:
          enemy.kill()
        #game_over = False
        last_enemy_spawn = pygame.time.get_ticks()    
        world.reset_level()
        world.process_enemies()
        pressed_keys = []
        level_started = False
        shiphealth = 20
        game_outcome = 0
        world.level = 1
        #YOU LOST (resetting variables)
        
    elif game_outcome == 1:
      #ADD AN ENDING STATEMENT " NOW YOU HAVE DEFENDED EARTH, YOU ARE ABLE TO REPOPULATE THE WORLD "
      font = pygame.font.Font(None, 175)
      font1 = pygame.font.Font(None, 50)
      pygame.draw.rect(DISPLAYSURF,
                       "dodgerblue", (400, 200, 1200, 800),
                       border_radius=30)
      draw_text("You Won, Congrats!", font, "black", 415, 500)
      if restart_button.draw(DISPLAYSURF):
        for enemy in enemy_group:
          enemy.kill()
        #game_over = False
        last_enemy_spawn = pygame.time.get_ticks()    
        world.reset_level()
        world.process_enemies()
        pressed_keys = []
        level_started = False
        shiphealth = 20
        game_outcome = 0
        world.level = 1
        #YOU WON (resetting variables))


  if world.level != 1:
    if world.check_level_complete() is True:
      if shiphealth != 0:
        if world.level == 6:
          game_outcome = 1
          game_over = True
          #if game should be over, make it over, and change game_outcome accordingly.
        else:
          
          level_started = False
  
          presskey = get_pressed_keys()
          pygame.draw.rect(DISPLAYSURF,"dodgerblue", (400, 200, 1200, 800),border_radius=30)
          font = pygame.font.Font(None, 50)
  
          
          if pick == 0:
            font = pygame.font.Font(None, 50)
            font1 = pygame.font.Font(None, 40)
            draw_text("How many planets are in the solar system", font, "black",
                      700, 500)
            draw_text("A. 6, B. 7, C. 8, D. 9", font1, "black", 860, 600)
            if any(presskey):
              if "c" in presskey:
                draw_text("Right Answer!", font, "green", 795, 300)
                if health_updated is False:
                  shiphealth += 5
                  #pressed_keys = []
                  #pick = random.randint(0,4)
                  health_updated = True
              elif "c" not in presskey:
                draw_text("Wrong Answer!", font, "red", 795, 300)
                if health_updated is False:
                  shiphealth -= 5
                  #pressed_keys = []
                  #pick = random.randint(0,4)
                  health_updated = True
          if pick == 1:
            font = pygame.font.Font(None, 50)
            font1 = pygame.font.Font(None, 40)
            draw_text("What is the largest planet in the solar system?", font,
                      "black", 700, 500)
            draw_text("A. Saturn, B. Jupiter, C. Mars, D. Pluto", font1, "black",
                      860, 600)
            if any(presskey):
              if "b" in presskey:
                draw_text("Right Answer!", font, "green", 795, 300)
                if health_updated2 is False:
                  shiphealth += 5
                  #pressed_keys = []
                  #pick = random.randint(0,4)
                  health_updated2 = True
              elif "b" not in presskey:
                draw_text("Wrong Answer!", font, "red", 795, 300)
                if health_updated2 is False:
                  shiphealth -= 5
                  #pressed_keys = []
                  # pick = random.randint(0,4)
                  health_updated2 = True
          if pick == 2:
            font = pygame.font.Font(None, 50)
            font1 = pygame.font.Font(None, 40)
            draw_text("Why are black holes black?", font, "black", 700, 500)
            draw_text(
                "A. There is no light in space, B. It is too deep to see anything",
                font1, "black", 600, 600)
            draw_text(
                "C. None of the above, D. It absorbs all of the incoming light.",
                font1, "black", 600, 700)
            if any(presskey):
              if "d" in presskey:
                draw_text("Right Answer!", font, "green", 795, 300)
                if health_updated3 is False:
                  shiphealth += 5
                  #pressed_keys = []
                  # pick = random.randint(0,4)
                  health_updated3 = True
              elif "d" not in presskey:
                draw_text("Wrong Answer!", font, "red", 795, 300)
                if health_updated3 is False:
                  shiphealth -= 5
                  #pressed_keys = []
                  #pick = random.randint(0,4)
                  health_updated3 = True
  
          if pick == 3:
            font = pygame.font.Font(None, 50)
            font1 = pygame.font.Font(None, 40)
            draw_text("How many moons does Jupiter have?", font, "black", 470,
                      500)
            draw_text("A. 95, B. 29, C. 97, D. 56", font1, "black", 860, 600)
            if any(presskey):
              if "a" in presskey:
                draw_text("Right Answer!", font, "green", 795, 300)
                if health_updated4 is False:
                  shiphealth += 5
                  #pressed_keys = []
                  # pick = random.randint(0,4)
                  health_updated4 = True
              elif "d" not in presskey:
                draw_text("Wrong Answer!", font, "red", 795, 300)
                if health_updated4 is False:
                  shiphealth -= 5
                  #pressed_keys = []
                  #pick = random.randint(0,4)
                  health_updated4 = True
  
          if begin_button.draw(DISPLAYSURF):
            world.level += 1
            last_enemy_spawn = pygame.time.get_ticks()
            world.reset_level()
            world.process_enemies()
            pressed_keys = []
            level_started = True
            game_over = False
            if health_updated is True or health_updated2 is True or health_updated3 is True or health_updated4 is True:
              #pick = random.randint(0, 3)
              health_updated = False
              health_updated2 = False
              health_updated3 = False
              health_updated4 = False
            if pick == 0:
              pick = random.randint(1, 3)
            if pick == 1:
              pick = random.randint(2, 3)
            if pick == 2:
              pick = random.randint(3, 3)
            if pick == 3:
              pick = random.randint(0, 2)

           # ^ This chunk deals with, picking a question, rendering it, and checking if the player got it right or wrong. The way to answer questions is by typing them in the game window (EDUCATIONAL ASPECT)

    
  if world.level == 1 and level_started == False:
    pygame.draw.rect(DISPLAYSURF,
                     "dodgerblue", (400, 200, 1200, 800),
                     border_radius=30)
    font = pygame.font.Font(None, 50)
    draw_text("COSMIC GUARDIAN: LAST STAND.", font, "black", 740, 200)
    draw_text(
        "Welcome to Cosmic Guardian: Last Stand. is an intergalactic adventure",
        font, "black", 405, 300)
    draw_text(
        "where you; the last survivor on Earth, must defend against an extra-",
        font, "black", 405, 330)
    draw_text(
        "terrestrial invasion.As the only line of defense, pilot a futuristic yet",
        font, "black", 420, 360)
    draw_text("makeshift spaceship constructed from salvaged scrap parts.",
              font, "black", 420, 390)
    draw_text("As the spaceship is makeshift, you may need to click buttons",
              font, "black", 420, 420)
    draw_text(
        "or type answers multiple times.  Face increasingly challenging enemy",
        font, "black", 405, 450)
    draw_text("U.F.O's across five rounds. Between rounds,engage in cosmic",
              font, "black", 420, 480)
    draw_text(
        "knowledge challenges, to swiftly save earth. Good Luck Commander.",
        font, "black", 420, 510)
    draw_text("[radio signal fades]", font, "black", 810, 540)
    if begin_button.draw(DISPLAYSURF):
      world.level += 1
      last_enemy_spawn = pygame.time.get_ticks()
      world.reset_level()
      world.process_enemies()
      pressed_keys = []
      game_over = False
      level_started = True

  #first time start screen

  DISPLAYSURF.blit(text, (0, 430))
  pygame.display.update()
  #update the screen.
