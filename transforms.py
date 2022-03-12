def transform(self, x, y):
    # return self.transform2d(x,y)
    return self.transform_perspective(x, y)


def transform2d(self, x, y):
    return int(x), int(y)


def transform_perspective(self, x, y):
    lin_y = y * self.y_p / self.height
    if lin_y > self.y_p:
        lin_y = self.y_p

    diff_x = x - self.x_p
    diff_y = self.y_p - lin_y
    proportion_y = diff_y / self.y_p
    proportion_y = pow(proportion_y, 4)

    new_x = self.x_p + diff_x * proportion_y
    new_y = self.y_p - proportion_y * self.y_p

    return int(new_x), int(new_y)