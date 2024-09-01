import pyautogui as pag
import random


class Mouse:
    def __get_random(self, rand_amount):
        rand_x = random.randint(rand_amount * -1, rand_amount)
        rand_y = random.randint(rand_amount * -1, rand_amount)
        return [rand_x, rand_y]

    def single_click(self, x=None, y=None, rand_amount=0):
        if x and y:
            self.mouse_move(x, y, rand_amount)

        pag.click()

    def double_click(self, x=None, y=None, rand_amount=0):
        if x and y:
            self.mouse_move(x, y, rand_amount)

        pag.click(clicks=2)

    def mouse_move(self, x, y, rand_amount=0):
        rl_x = self.rl_window["x"]
        rl_y = self.rl_window["y"]
        rand = self.__get_random(rand_amount)
        pag.moveTo(x + rl_x + rand[0], y + rl_y + rand[1])

    def right_click(self, x, y, text):
        # Can we OCR the menu after right click?
        """"""
