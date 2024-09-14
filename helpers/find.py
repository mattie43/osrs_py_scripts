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

    if len(template_img.shape) == 3:  # Check if the image is not grayscale
        template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    return template_img


def find_image(img_name, threshold=0.8):
    """
    Given a template image, returns a tuple of x, y, w, h
    """

    # Take a screenshot
    ss = __take_ss()
    ss_img = numpy.array(ss)  # Convert screenshot to numpy array

    if len(ss_img.shape) == 3:  # Check if the screenshot is not grayscale
        ss_img = cv2.cvtColor(ss_img, cv2.COLOR_RGB2GRAY)

    template_img = __get_template(img_name)

    # Template matching using cv2.matchTemplate
    result = cv2.matchTemplate(ss_img, template_img, cv2.TM_CCOEFF_NORMED)

    locations = numpy.where(result >= threshold)

    # Check if any location found
    if len(locations[0]) > 0:
        # Get the first match location
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        x, y = max_loc  # Top-left corner of matched region
        h, w = template_img.shape[:2]  # Get template image dimensions

        return x, y, w, h  # Return the location and size of the matched region
    else:
        return None  # No match found


def find_color(color):
    """
    Given a BGR color, returns a tuple of x, y, w, h
    """

    # Take a screenshot and convert to HSV
    ss = __take_ss()
    ss_img = numpy.array(ss)
    hsv_img = cv2.cvtColor(ss_img, cv2.COLOR_RGB2HSV)  # Convert to HSV

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
            return (
                x,
                y,
                w,
                h,
            )

    return None
