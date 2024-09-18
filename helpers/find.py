import numpy
import pyautogui
import cv2
from helpers.store import rl
from pathlib import Path


def __take_ss():
    region = [
        rl["window"]["x"],
        rl["window"]["y"],
        rl["window"]["w"],
        rl["window"]["h"],
    ]
    ss = pyautogui.screenshot(region=region)
    return ss


def __get_limits(color):
    c = numpy.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = numpy.array([hue - 10, 100, 100], dtype=numpy.uint8)
        upperLimit = numpy.array([180, 255, 255], dtype=numpy.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = numpy.array([0, 100, 100], dtype=numpy.uint8)
        upperLimit = numpy.array([hue + 10, 255, 255], dtype=numpy.uint8)
    else:
        lowerLimit = numpy.array([hue - 10, 100, 100], dtype=numpy.uint8)
        upperLimit = numpy.array([hue + 10, 255, 255], dtype=numpy.uint8)

    return lowerLimit, upperLimit


def __get_template(img):
    __PATH = Path(__file__).parent.parent
    imgs_dir = __PATH.joinpath("imgs")
    img_path = list(imgs_dir.rglob(img))

    if not img_path:
        print("No image found in path.")
        return None

    template_img = cv2.imread(img_path[0], cv2.IMREAD_UNCHANGED)

    return template_img


def find_image(template_img, region=None, confidence=0.8):
    """
    Given a template image, returns an array of the center x and y if found, else None.
    """

    # Take screenshot
    ss_img = __take_ss()
    ss_img = cv2.cvtColor(numpy.array(ss_img), cv2.COLOR_RGB2GRAY)

    if not template_img.endswith(".png"):
        template_img = f"{template_img}.png"

    template_img = __get_template(template_img)

    if not template_img.any():
        print("No template image found.")
        return None

    if region:
        # [x1, y1, x2, y2]
        # y1:y2, x1:x2
        a = region[1]
        b = region[3]
        c = region[0]
        d = region[2]
        template_img = template_img[a:b, c:d]

    template_img = cv2.cvtColor(numpy.array(template_img), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(ss_img, template_img, cv2.TM_CCOEFF_NORMED)

    locations = numpy.where(result >= confidence)

    if len(locations[0]) > 0:
        _, _, _, max_loc = cv2.minMaxLoc(result)
        tl_x, tl_y = max_loc
        h, w = template_img.shape[:2]
        br_x, br_y = (tl_x + w, tl_y + h)
        center_x = (tl_x + br_x) // 2
        center_y = (tl_y + br_y) // 2

        return [center_x, center_y]
    else:
        return None  # No match found


def find_color(color):
    """
    Given a BGR color, returns an array of the center x and y if found, else None.
    """

    # Take a screenshot and convert to HSV
    ss_img = __take_ss()
    hsv_img = cv2.cvtColor(numpy.array(ss_img), cv2.COLOR_RGB2HSV)  # Convert to HSV

    # Get HSV limits for the color
    lower, upper = __get_limits(color)

    # Create mask for the color range
    mask = cv2.inRange(hsv_img, lower, upper)

    # Find contours from the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter valid contours to an array
    for contour in contours:
        if cv2.contourArea(contour) > 50:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            return [center_x, center_y]

    return None
