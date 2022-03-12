from kivy.graphics import *
def generateVLines(self):
    with self.canvas:
        Color(240/255, 240/255, 240/255)
        for i in range(self.num):
            self.lines.append(Line())


def generateHLines(self):
    with self.canvas:
        Color(255/255, 255/255, 255/255)
        for i in range(self.h_num):
            self.horizontal_lines.append(Line())


def updateVLines(self):
    startIndex = -int(self.num/2)+1
    endIndex = startIndex+self.num
    for i in range(startIndex,endIndex):
        x_val = self.get_line_x(i)
        x1, y1 = self.transform(x_val, 0)
        x2, y2 = self.transform(x_val, self.height)
        self.lines[i].points = [x1, y1, x2, y2]


def updateHLines(self):
    startIndex = -int(self.num / 2) + 1
    endIndex = startIndex + self.num - 1
    x_min = self.get_line_x(startIndex)
    x_max = self.get_line_x(endIndex)

    for i in range(self.h_num):
        line_y = self.get_line_y(i)
        x1, y1 = self.transform(x_min, line_y)
        x2, y2 = self.transform(x_max, line_y)
        self.horizontal_lines[i].points = [x1, y1, x2, y2]