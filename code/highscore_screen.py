import pygame
import sys

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
            if keys[pygame.K_a]:
                str_list.append("A")
                pressing = True
            elif keys[pygame.K_b]:
                str_list.append("B")
                pressing = True
            elif keys[pygame.K_c]:
                str_list.append("C")
                pressing = True
            elif keys[pygame.K_d]:
                str_list.append("D")
                pressing = True
            elif keys[pygame.K_e]:
                str_list.append("E")
                pressing = True
            elif keys[pygame.K_f]:
                str_list.append("F")
                pressing = True
            elif keys[pygame.K_g]:
                str_list.append("G")
                pressing = True
            elif keys[pygame.K_h]:
                str_list.append("H")
                pressing = True
            elif keys[pygame.K_i]:
                str_list.append("I")
                pressing = True
            elif keys[pygame.K_j]:
                str_list.append("J")
                pressing = True
            elif keys[pygame.K_k]:
                str_list.append("K")
                pressing = True
            elif keys[pygame.K_l]:
                str_list.append("L")
                pressing = True
            elif keys[pygame.K_m]:
                str_list.append("M")
                pressing = True
            elif keys[pygame.K_n]:
                str_list.append("N")
                pressing = True
            elif keys[pygame.K_o]:
                str_list.append("O")
                pressing = True
            elif keys[pygame.K_p]:
                str_list.append("P")
                pressing = True
            elif keys[pygame.K_q]:
                str_list.append("Q")
                pressing = True
            elif keys[pygame.K_r]:
                str_list.append("R")
                pressing = True
            elif keys[pygame.K_s]:
                str_list.append("S")
                pressing = True
            elif keys[pygame.K_t]:
                str_list.append("T")
                pressing = True
            elif keys[pygame.K_u]:
                str_list.append("U")
                pressing = True
            elif keys[pygame.K_v]:
                str_list.append("V")
                pressing = True
            elif keys[pygame.K_w]:
                str_list.append("W")
                pressing = True
            elif keys[pygame.K_x]:
                str_list.append("X")
                pressing = True
            elif keys[pygame.K_y]:
                str_list.append("Y")
                pressing = True
            elif keys[pygame.K_z]:
                str_list.append("Z")
                pressing = True
            elif keys[pygame.K_SPACE]:
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
