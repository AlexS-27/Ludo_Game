import random
import pygame
import time

class Dice:
    def __init__(self):
        self.result = None
        self.animating = False
        self.animating_start = 0
        self.animating_duration = 0.6
        self.current_display = 1

    def dice_roll(self):
        return random.randint(1,6)

    def start_animation(self):
        self.animating = True
        self.animating_start = time.time()
        self.result = None

    def update(self):
        if self.animating:
            elapsed = time.time() - self.animating_start

            if elapsed < self.animating_duration:
                #during the animation --> draw a random number
                self.current_display = random.randint(1,6)
            else:
                # End of the animation
                self.result = self.dice_roll()
                self.current_display = self.result
                self.animating = False

    def draw(self, screen, font, x=0, y=0):
        text = font.render(str(self.current_display), True, (255,255,255))
        screen.blit(text, (x,y))


