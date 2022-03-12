import random
from kivy.graphics import *


def get_line_x(self, index):
    center_x = int(self.x_p)

    offset = index - 0.5
    spacing = self.spacing * self.width
    line_x = center_x + offset * spacing + self.current_offset_x
    return line_x


def get_line_y(self, index):
    spacing_y = self.h_spacing * self.height
    return index * spacing_y - self.current_offset_y


def get_tile(self, t_x, t_y):
    t_y = t_y - self.loop_index
    x = self.get_line_x(t_x)
    y = self.get_line_y(t_y)
    return x, y


def updateCord(self):
    for i in range(len(self.tile_cord) - 1, -1, -1):
        if self.tile_cord[i][1] < self.loop_index:
            del self.tile_cord[i]
    if len(self.tile_cord) != 0:
        ending_x = self.tile_cord[len(self.tile_cord) - 1][0]
        ending_y = self.tile_cord[len(self.tile_cord) - 1][1] + 1
    else:
        ending_y = 0
        ending_x = 0

    startIndex = -int(self.num / 2) + 1
    endIndex = startIndex + self.num - 1

    for i in range(len(self.tile_cord), self.num_of_tiles):
        r = 0
        if self.min_tiles == 2:
            r = random.randint(-1, 1)
            self.min_tiles = 0
        self.tile_cord.append((ending_x, ending_y))
        self.min_tiles += 1

        if ending_x <= startIndex:
            r = 1
        elif ending_x >= endIndex-1:
            r = -1

        if r == -1:
            ending_x -= 1
            self.tile_cord.append((ending_x, ending_y))
            ending_y += 1
            self.tile_cord.append((ending_x, ending_y))
        elif r == 1:
            ending_x += 1
            self.tile_cord.append((ending_x, ending_y))
            ending_y += 1
            self.tile_cord.append((ending_x, ending_y))

        ending_y += 1


def initialTiles(self):
    for i in range(10):
        self.tile_cord.append((0, i))


def generateTile(self):
    with self.canvas:
        Color(234/255, 242/255, 248/255)
        for i in range(self.num_of_tiles):
            self.tiles.append(Quad())


def updateTile(self):
    for i in range(self.num_of_tiles):
        t_x, t_y = self.tile_cord[i]

        xmin, ymin = self.get_tile(t_x, t_y)
        xmax, ymax = self.get_tile(t_x + 1, t_y + 1)

        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]
