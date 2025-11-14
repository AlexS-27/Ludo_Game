import pygame

pygame.init()

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE) #,pygame.display.set_caption('Ludo Game')
screen_width, screen_height = screen.get_size()

#setup window's title
pygame.display.set_caption("Ludo Game")

# define game variable
#laod image

run = True

#main loop
while run:

    events = pygame.event.get()
    for event in events:
        #quit pygame
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
