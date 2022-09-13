import pygame
import sys
import string

name = ""
str_list = []

pressing = True


def highscore_screen(screen, clock, font):
    global name, pressing

    str_list.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill("white")

        keys = pygame.key.get_pressed()
        if not pressing:
            for letter in string.ascii_lowercase:
                if eval(f"keys[pygame.K_{letter}]"):
                    str_list.append(letter.upper())
                    pressing = True

            if keys[pygame.K_SPACE]:
                str_list.append(" ")
                pressing = True
            elif keys[pygame.K_BACKSPACE]:
                str_list.pop()
                pressing = True
            elif keys[pygame.K_RETURN]:
                break

        elif not keys.__contains__(True):
            pressing = False

        name = "".join(letter for letter in str_list)

        text1 = "WELL DONE!"
        text2 = "YOU MADE A HIGH SCORE!"
        text3 = "Please enter your name:"
        text4 = f"{name}"
        texts = [text1, text2, text3, text4]

        (x, y) = (400, 50)
        for text in texts:
            surface = font.render(text, False, "black")
            rect = surface.get_rect(center=(x, y))
            screen.blit(surface, rect)
            y += 100

        pygame.display.update()
        clock.tick(60)
