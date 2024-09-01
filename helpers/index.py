from helpers.runelite import Runelite
from helpers.image_search import ImageSearch
from helpers.mouse import Mouse
from helpers.tabs import Tabs


# Single location for extending helper classes
class HelpersIndex(Runelite, ImageSearch, Mouse, Tabs):
    def __init__(self):
        super().__init__()
