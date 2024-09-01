import cv2
import pyautogui
import numpy
from pathlib import Path


class ImageSearch:
    def __init__(self):
        __PATH = Path(__file__).parent.parent
        self.imgs_dir = __PATH.joinpath("imgs")

    def __take_ss(self):
        # x, y, w, h
        screenshot = pyautogui.screenshot(
            region=(
                self.rl_window["x"],
                self.rl_window["y"],
                self.rl_window["w"],
                self.rl_window["h"],
            )
        )
        screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot  # Keep it in BGR format

    def __imagesearcharea(self, template, confidence: float):
        # If image doesn't have an alpha channel, convert it from BGR to BGRA
        im = self.__take_ss()
        if len(template.shape) < 3 or template.shape[2] != 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2BGRA)
        # Get template dimensions
        hh, ww = template.shape[:2]
        # Extract base image and alpha channel
        base = template[:, :, 0:3]
        alpha = template[:, :, 3]
        alpha = cv2.merge([alpha, alpha, alpha])

        correlation = cv2.matchTemplate(im, base, cv2.TM_SQDIFF_NORMED, mask=alpha)
        min_val, _, min_loc, _ = cv2.minMaxLoc(correlation)

        if not min_val < confidence:
            return None

        top_left = min_loc
        bottom_right = (top_left[0] + ww, top_left[1] + hh)
        cv2.rectangle(
            im, top_left, bottom_right, (0, 255, 0), 2
        )  # Draw rectangle around match
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2
        cv2.rectangle(im, top_left, bottom_right, (0, 255, 0), 2)

        return {
            "center_x": center_x,
            "center_y": center_y,
            "tl_x": top_left[0],
            "tl_y": top_left[1],
            "br_x": bottom_right[0],
            "br_y": bottom_right[1],
        }

    def find_image_in(
        self,
        img,
        confidence=0.15,
    ):
        image_path = list(self.imgs_dir.rglob(img))
        if not image_path:
            print("No image found in path.")
            return None

        image = cv2.imread(image_path[0], cv2.IMREAD_UNCHANGED)

        return self.__imagesearcharea(image, confidence)