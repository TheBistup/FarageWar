import pygame
from random import randint
from math import sqrt
import pyautogui as auto

class Game():
    def __init__(self):
          # Initialise values, pygame stuff

          self.display_settings = [480, 480]
          self.game_caption = "Shoot Farage - 0.2"
          self.game_display = pygame.display.set_mode(self.display_settings)

          pygame.init()
          pygame.display.set_caption(self.game_caption)
          self.clock = pygame.time.Clock()

          print ("[!] Loading Images... Expect some sRGB errors coz I cba to crush them!")
          self.images = {
          "x": pygame.image.load("./Assets/x.png"),
          "y": pygame.image.load("./Assets/y.png"),
          "-x": pygame.image.load("./Assets/-x.png"),
          "-y": pygame.image.load("./Assets/-y.png"),
          "bird": pygame.image.load("./Assets/bird.png"),
          "explosion": pygame.image.load("./Assets/explosion.jpg"),
          "health0": pygame.image.load("./Assets/health0.png"),
          "health1": pygame.image.load("./Assets/health1.png"),
          "health2": pygame.image.load("./Assets/health2.png"),
          "health3": pygame.image.load("./Assets/health3.png"),
          "farage": pygame.image.load("./Assets/farage.png"),
          "union jack": pygame.image.load("./Assets/union_jack.jpg"),
          "EU": pygame.image.load("./Assets/EU.png")
          }

          self.keys = {"w": 0, "a": 0, "s": 0, "d": 0, "f": 0}

          self.map_pos = {"x": -480, "y": -480}
          self.proj = []
          self.farages = []

          self.facing = "-y"
          self.check = 0
          self.health = 3
          self.kills = 0
          self.font = pygame.font.SysFont("Comic Sans MS", 30)

          self.game_loop()

    def game_loop(self):
        tick = 0
        while True:
            tick += 1
            self.get_events()

            self.blit_map()
            self.blit_char()
            self.deal_farages()
            self.destroy_farages()
            self.fire()
            text = self.font.render("Farages Killed: %s" % (str(self.kills)), False, (0,0,0))
            self.game_display.blit(text, (0,0))

            if self.kills >= 50:
                while True:
                    self.game_display.blit(self.images["EU"], (0, 0))
                    text2 = self.font.render("You Saved The UK!!! Well done!", False, (0,0,0))
                    self.game_display.blit(text2, (self.display_settings[0]/2-50,self.display_settings[1]/2))
                    self.game_display.blit(text, (0,0))
                    pygame.display.update()
                    self.clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

            pygame.display.update()
            self.clock.tick(60)

            if tick == 120:
                self.create_farage()
                tick = 0

            if tick % 30 == 0:
                self.deal_damage()

    def deal_farages(self):
        for i in range(0, len(self.farages)):
            if self.farages[i][0] < self.display_settings[0] / 2:
                self.farages[i][0] += 2
            if self.farages[i][0] > self.display_settings[0] / 2:
                self.farages[i][0] -= 2
            if self.farages[i][1] < self.display_settings[1] / 2:
                self.farages[i][1] += 2
            if self.farages[i][1] > self.display_settings[1] / 2:
                self.farages[i][1] -= 2

            if self.keys["w"] == 1:
                self.farages[i][1] += 4
            if self.keys["a"] == 1:
                self.farages[i][0] += 4
            if self.keys["s"] == 1:
                self.farages[i][1] -= 4
            if self.keys["d"] == 1:
                self.farages[i][0] -= 4

            self.game_display.blit(
            self.images["farage"],
            (self.farages[i][0], self.farages[i][1])
            )

    def destroy_farages(self):
        for i in range(0, len(self.proj)):
            px = self.proj[i][0] + 20
            py = self.proj[i][1] + 20
            for j in range(0, len(self.farages)):
                try:
                    fx = self.farages[i][0] + 20
                    fy = self.farages[i][1] + 20
                    dx = abs(px-fx)
                    dy = abs(py-fy)
                    if dx**2 + dy**2 <= 40**2:
                        self.farages.pop(j)
                        j -= 1
                        self.kills += 1
                except:
                    pass

    def deal_damage(self):
        for i in range(0, len(self.farages)):
            fx = self.farages[i][0] + 20
            fy = self.farages[i][1] + 20

            cx = self.display_settings[0] / 2
            cy = self.display_settings[1] / 2

            dx = abs(cx-fx)
            dy = abs(cy-fy)

            if dx**2 + dy**2 <= 40**2:
                self.health -= 1
            if self.health == -1:
                auto.alert("""The farages have taken over the world.
With your last breath you say goodbye to England as she is submitted once more into the dark ages.""")
                while True:
                    self.game_display.fill([0,0,0])
                    half1 = self.display_settings[0]/2 - 155
                    half2 = self.display_settings[1]/2 - 120
                    self.game_display.blit(self.images["explosion"], (0, 0))
                    pygame.display.update()
                    self.clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()


    def create_farage(self):
        randx = randint(0, self.display_settings[0])
        randy = randint(0, self.display_settings[1])
        self.farages.append([randx, randy])

    def fire(self):
        if self.keys["f"] == 1:
            self.proj.append([
             240, 240,
             self.map_pos["x"], self.map_pos["y"],
             self.facing
             ])
        temp = self.proj
        for i in range(0, len(self.proj)):
            if len(self.proj) > 0:
                if self.proj[i][4] == "x":
                    self.proj[i][0] += 6
                elif self.proj[i][4] == "y":
                    self.proj[i][1] += 6
                elif self.proj[i][4] == "-x":
                    self.proj[i][0] -= 6
                elif self.proj[i][4] == "-y":
                    self.proj[i][1] -= 6

                if self.keys["w"] == 1:
                    self.proj[i][1] += 4
                if self.keys["a"] == 1:
                    self.proj[i][0] += 4
                if self.keys["s"] == 1:
                    self.proj[i][1] -= 4
                if self.keys["d"] == 1:
                    self.proj[i][0] -= 4

                self.game_display.blit(
                self.images["bird"],
                (self.proj[i][0], self.proj[i][1])
                )

        for i in range(0, len(self.proj)):
            try:
                if self.proj[i][0] + 20 < 0 or self.proj[i][0] + 20 > self.display_settings[0]:
                    self.proj.pop(i)
                    i -= 1
                elif self.proj[i][1] + 20 < 0 or self.proj[i][1] + 20 > self.display_settings[1]:
                    self.proj.pop(i)
                    i -= 1
            except:
                pass


    def blit_char(self):
        half1 = int(self.display_settings[0] / 2)
        half2 = int(self.display_settings[1] / 2)
        check = 0
        blitted = 0

        if self.keys["w"] == 1:
            if blitted == 0:
                self.game_display.blit(self.images["-y"], (half1, half2))
                self.facing = "-y"
                blitted = 1
            check = 1
            self.map_pos["y"] += 4
        if self.keys["a"] == 1:
            if blitted == 0:
                self.game_display.blit(self.images["-x"], (half1, half2))
                self.facing = "-x"
                blitted = 1
            check = 1
            self.map_pos["x"] += 4
        if self.keys["s"] == 1:
            if blitted == 0:
                self.game_display.blit(self.images["y"], (half1, half2))
                self.facing = "y"
                blitted = 1
            check = 1
            self.map_pos["y"] -= 4
        if self.keys["d"] == 1:
            if blitted == 0:
                self.game_display.blit(self.images["x"], (half1, half2))
                self.facing = "x"
                blitted = 1
            self.map_pos["x"] -= 4
            check = 1
        if check == 0:
            self.game_display.blit(self.images[self.facing], (half1, half2))
        healthy = str("health%s" % (self.health))
        self.game_display.blit(self.images[healthy], (half1, half2+30))

    def blit_map(self):
        if self.map_pos["x"] > 0:
            self.map_pos["x"] = 0
        if self.map_pos["y"] > 0:
            self.map_pos["y"] = 0
        if self.map_pos["x"] < -2276:
             self.map_pos["x"] = -2276
        if self.map_pos["y"] < -1076:
            self.map_pos["y"] = -1076

        self.game_display.blit(
        self.images["union jack"],
        (self.map_pos["x"], self.map_pos["y"])
        )



    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.keys["w"] = 1
                if event.key == pygame.K_a:
                    self.keys["a"] = 1
                if event.key == pygame.K_s:
                    self.keys["s"] = 1
                if event.key == pygame.K_d:
                    self.keys["d"] = 1
                if event.key == pygame.K_f:
                    self.keys["f"] = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keys["w"] = 0
                if event.key == pygame.K_a:
                    self.keys["a"] = 0
                if event.key == pygame.K_s:
                    self.keys["s"] = 0
                if event.key == pygame.K_d:
                    self.keys["d"] = 0
                if event.key == pygame.K_f:
                    self.keys["f"] = 0


run = Game()
