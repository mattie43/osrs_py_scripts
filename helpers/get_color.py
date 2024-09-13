import numpy
import pyautogui
import cv2
from helpers.store import store


def __take_ss():
    region = [
        store["rl"]["window"]["x"],
        store["rl"]["window"]["y"],
        store["rl"]["window"]["w"],
        store["rl"]["window"]["h"],
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


def get_color(color):
    """
    Given a BGR color, returns the coords of the center of the found color and highlights
    connected regions of that color.
    """

    # Take a screenshot and convert to HSV
    ss = __take_ss()
    img = numpy.array(ss)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)  # Convert to HSV

    # Get HSV limits for the color
    lower, upper = __get_limits(color)

    # Create mask for the color range
    mask = cv2.inRange(hsv_img, lower, upper)

    # Find contours from the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    for contour in contours:
        if cv2.contourArea(contour) > 50:  # Filter out small areas (adjust as needed)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(
                img, (x, y), (x + w, y + h), (0, 255, 0), 2
            )  # Draw a rectangle around the connected area

    # Display the image with contours
    cv2.imshow("Detected Colors", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
