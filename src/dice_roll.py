# src/dice_roll.py
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
        # Le premier chiffre affiché immédiatement pour ne pas avoir de case vide
        self.current_display = random.randint(1,6) 

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

    def draw(self, screen, font):
        # Cette méthode n'est plus utilisée directement dans la nouvelle UI de main.py
        # Le dé est affiché dans draw_sidebar
        pass