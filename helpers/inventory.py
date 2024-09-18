from helpers.find import find_image
from helpers.mouse import single_click, mouse_move
from helpers.store import rl

# Inv slot size is w30, h26


def __get_all_slots(fromZero=False):
    backpack_coords = find_image("backpack")
    starting_x = 0 if fromZero else backpack_coords[0] - 77
    starting_y = 0 if fromZero else backpack_coords[1] + 31

    col_x = [starting_x + i * 42 for i in range(4)]
    col_y = [starting_y + i * 36 for i in range(7)]

    return [col_x, col_y]


def __get_inv_slot(slot_num, fromZero=False):
    row_x, col_y = __get_all_slots(fromZero)

    # Determine the row and column from the slot number
    col = (slot_num - 1) % 4
    row = (slot_num - 1) // 4

    # Get the x and y coordinates
    slot_x = row_x[col]
    slot_y = col_y[row]

    return [slot_x, slot_y]


def ss_inv_slot(slot_num):
    return __get_inv_slot(slot_num)
    """"""


def is_inv_slot_empty(slot_num):
    slot = __get_inv_slot(slot_num, fromZero=True)
    # Use inv slot size as w and h
    region = [slot[0], slot[1], slot[0] + 30, slot[1] + 26]
    found = find_image("empty_inv", region)
    return True if found else False


def click_inv_slot(slot_num):
    slot = __get_inv_slot(slot_num)
    # Use half of inv slot size to get center.
    single_click(slot[0] + 15, slot[1] + 13, 8)
