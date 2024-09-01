tab_list = [
    "combat",
    "stats",
    "quests",
    "backpack",
    "equipment",
    "prayer",
    "magic",
    "logout",
]

spellbooks = [
    "magic_ancient.png",
    "magic_arceuus.png",
    "magic_lunar.png",
    "magic_normal.png",
]


class Tabs:
    def __check_for_spellbook(self):
        for img in spellbooks:
            found = self.find_image_in(img)
            if found:
                return found
        return None

    def select_tab(self, tab_name: str):
        # TODO can we check tab already selected?

        if tab_name not in tab_list:
            print(f"No valid tab name given: {tab_name}")
            return None

        img = f"{tab_name}.png"
        image_coords = None

        # Case to check each mage book
        if tab_name == "magic":
            image_coords = self.__check_for_spellbook()
        else:
            image_coords = self.find_image_in(img)

        if not image_coords:
            return print(f"Failed to find image for tab: {tab_name}")

        self.single_click(image_coords["center_x"], image_coords["center_y"], 10)
