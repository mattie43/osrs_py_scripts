class Inventory:
    def __init__(self):
        super().__init__()
        self.inv_loc = None

    def __find_inventory(self):
        self.inv_loc = self.find_image(img="inventory.png")

    def __get_slot_coords(self, slot):
        # tl of img + gap between img and slot one + half of inv slot size
        starting_x = self.inv_loc["tl_x"] + 42 + 15
        starting_y = self.inv_loc["tl_y"] + 11 + 13

        col_x = [starting_x + i * 42 for i in range(4)]
        col_y = [starting_y + i * 36 for i in range(7)]

        # Determine the row and column from the slot number
        col = (slot - 1) % 4
        row = (slot - 1) // 4

        # Get the x and y coordinates
        slot_x = col_x[col]
        slot_y = col_y[row]

        return [slot_x, slot_y]

    def click_inventory_slot(self, slot: int = 1):
        if not self.inv_loc:
            self.__find_inventory()

        coords = self.__get_slot_coords(slot)
        self.single_click(coords[0], coords[1], 8)

    def is_inventory_slot_empty(self, slot: int = 1):
        if not self.inv_loc:
            self.__find_inventory()

        rl_x = self.rl_window["x"]
        rl_y = self.rl_window["y"]
        coords = self.__get_slot_coords(slot)
        region = (
            coords[0] - 15 + rl_x,
            coords[1] - 13 + rl_y,
            30,
            26,
        )
        return self.find_image(img="empty_inv_slot.png", region=region)
