import pygame
import block

# opening the files of the arenas
arena_difficult_file = open("assets/arena_dif.txt", "r")
arena_easy_file = open("assets/arena_easy.txt", "r")

# Reading the arenas
data_hard = arena_difficult_file.read()
data_easy = arena_easy_file.read()

# Converting each line in an element of the lists
arena_difficulties = [data_hard.split('\n'), data_easy.split('\n')]

# Closing the files
arena_difficult_file.close()
arena_easy_file.close()


class arena:
    def __init__(self):
        self.obstacles = []

    def get_obstacles(self):
        return self.obstacles

    def make_arena(self, screen, color, stage):

        lista = []

        if stage == 0:
            for i in range(25):
                for j in range(36):
                    if arena_difficulties[stage][i][j] == '1':
                        x = (j*25)
                        y = (i*22)+100
                        obstacle = block.block(pygame.image.load("assets/city_obstacle.png"),
                                               x, y, screen, color)
                        lista.append(obstacle)

        else:
            for i in range(25):
                for j in range(36):
                    if arena_difficulties[stage][i][j] == '1':
                        x = (j * 25)
                        y = (i * 22) + 100
                        obstacle = block.block(pygame.image.load("assets/vegetation_obstacle1.png"),
                                               x, y, screen, color)
                        lista.append(obstacle)

        self.obstacles = lista
