from kivy.config import Config
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'height', 400)
Config.set('graphics', 'width', 900)
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.properties import Clock
from kivy.graphics import *
from kivy.lang import Builder

Builder.load_file("menu.kv")


def readScore():
    with open('score.txt') as f:
        score = f.readline()
    return score


def writeScore(score):
    with open('score.txt', 'w') as f:
        f.write(score)

class MainWidget(RelativeLayout):
    from Controls import on_touch_up, on_touch_down
    from transforms import transform, transform2d, transform_perspective
    from Lines import generateHLines, generateVLines, updateVLines, updateHLines
    from Tiles import updateTile, updateCord, generateTile, initialTiles, get_line_x, get_line_y, get_tile
    menu_widget = ObjectProperty()
    bg = ObjectProperty()
    x_p = NumericProperty(0)
    y_p = NumericProperty(0)

    num = 10
    h_num = 12
    lines = []
    horizontal_lines = []
    spacing = 0.55
    h_spacing = 0.15

    current_offset_y = 0
    SPEED_Y = 0
    SPEED = 130

    current_offset_x = 0
    SPEED_X = 0

    tiles = []
    tile_cord = []
    num_of_tiles = 25

    loop_index = 1
    last_loop_index = 1
    increment_diff = 50
    min_tiles = 2

    ship = None
    base_y = 0.04
    ship_width = 0.13
    ship_height = 0.08
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    GAME_OVER = False
    GAME_START = False

    labelText = StringProperty("I  N  F  I  N  I  T  Y")
    buttonText = StringProperty("S T A R T")
    score = StringProperty("")
    highScore = StringProperty(readScore())

    backgrounds = ["backgrounds/bg1.jpg",
                   "backgrounds/bg2.jpg",
                   "backgrounds/bg3.jpg",
                   "backgrounds/bg4.jpg",
                   "backgrounds/bg5.jpg",
                   "backgrounds/bg6.jpg",
                  ]
    default_bg = 2


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # vertical lines
        with self.canvas.before:
            self.background = Rectangle()
        self.generateVLines()
        # horizontal lines
        self.generateHLines()

        # tile
        self.generateTile()
        self.restartGame()

        # ship
        self.initShip()

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def changeBackgroundLeft(self):

        if self.default_bg == 0:
            return
        self.default_bg -= 1

    def changeBackgroundRight(self):

        if self.default_bg == len(self.backgrounds)-1:
            return
        self.default_bg += 1

    def restartGame(self):
        self.loop_index = 1
        self.min_tiles = 2
        self.current_offset_y = 0
        self.SPEED = 130

        self.current_offset_x = 0
        self.SPEED_X = 0
        self.tile_cord = []
        self.initialTiles()
        self.updateCord()
        # self.generateTile()
        self.GAME_OVER = False

    def initShip(self):
        with self.canvas:

            Color(0, 0, 0)
            self.ship = Triangle()


    def updateShip(self):
        self.background.size = self.size
        self.background.source = self.backgrounds[self.default_bg]
        center_x = self.width / 2
        base_y = self.base_y * self.height
        ship_half_width = self.ship_width * self.width / 2

        self.ship_coordinates[0] = center_x - ship_half_width, base_y
        self.ship_coordinates[1] = center_x, base_y + (self.height * self.ship_height)
        self.ship_coordinates[2] = center_x + ship_half_width, base_y

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def checkShipCollision(self):
        for i in range(3):
            t_x, t_y = self.tile_cord[i]
            # if t_y > self.loop_index + 1:
            #     return False
            if self.checkTileCollision(t_x, t_y):
                return True
        return False

    def checkTileCollision(self, t_x, t_y):
        xmin, ymin = self.get_tile(t_x, t_y)
        xmax, ymax = self.get_tile(t_x + 1, t_y + 1)
        for i in range(len(self.ship_coordinates)):
            x, y = self.ship_coordinates[i]
            # print(x)
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return True
        return False

    def update(self, dt):
        self.updateVLines()
        self.updateHLines()
        self.updateTile()
        self.updateShip()
        if not self.GAME_OVER and self.GAME_START:
            self.SPEED_Y = self.height / self.SPEED
            current_x_speed = self.SPEED_X * self.width / 100
            time_factor = dt * 60

            self.current_offset_y += self.SPEED_Y * time_factor
            self.current_offset_x += current_x_speed * time_factor

            spacing_y = self.height * self.h_spacing
            self.score = str(self.loop_index)

            while self.current_offset_y > spacing_y:
                self.current_offset_y -= spacing_y
                self.loop_index += 1
                self.updateCord()
            if self.loop_index % self.increment_diff == 0 and self.loop_index != self.last_loop_index:
                self.SPEED -= 5
                self.last_loop_index = self.loop_index

        if not self.checkShipCollision() and not self.GAME_OVER and self.GAME_START:
            self.GAME_OVER = True
            self.menu_widget.opacity = 1
            print("Game over")
            currHighscore = int(readScore())
            if currHighscore < self.loop_index:
                self.highScore = self.score
                writeScore(self.highScore)

    def on_x_p(self, widget, value):
        pass

    def on_y_p(self, widget, value):
        pass

    def startGame(self):
        self.GAME_START = True
        self.menu_widget.opacity = 0
        self.restartGame()
        self.labelText = "G A M E   O V E R"
        self.buttonText = "R E S T A R T"


class GameApp(App):
    pass


GameApp().run()
