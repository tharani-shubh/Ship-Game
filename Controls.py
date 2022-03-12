from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):
    if not self.GAME_OVER and self.GAME_START:
        if touch.x < self.width / 2:
            self.SPEED_X = +2
        else:
            self.SPEED_X = -2
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    self.SPEED_X = 0