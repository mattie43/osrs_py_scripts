import pyautogui
import random
from helpers.store import rl


def __get_random(rand_amount):
    rand_x = random.randint(rand_amount * -1, rand_amount)
    rand_y = random.randint(rand_amount * -1, rand_amount)
    return [rand_x, rand_y]


def mouse_move(x, y, rand_amount=0):
    rl_x = rl["window"]["x"]
    rl_y = rl["window"]["y"]
    rand = __get_random(rand_amount)
    pyautogui.moveTo(x + rl_x + rand[0], y + rl_y + rand[1])


def single_click(x=None, y=None, rand_amount=0):
    if x and y:
        mouse_move(x, y, rand_amount)

    pyautogui.click()


def double_click(x=None, y=None, rand_amount=0):
    if x and y:
        mouse_move(x, y, rand_amount)

    pyautogui.click(clicks=2)


def right_click(x, y, text, rand_amount=0):
    # Can we OCR the menu after right click?
    """"""
