import cv2
import numpy as np
import pathlib
import time
import mss
from PIL import Image


def find_and_sort_templates(main_image, templates):
    """
    Find and sort the positions of template images found in the main image.

    Args:
        main_image_path (str): Path to the main image.
        templates (list): List of tuples with (template_image, template_path).

    Returns:
        List of sorted positions with (x, y, width, height).
    """
    # Load the main image and convert it to grayscale
    # main_image = cv2.imread(main_image_path, cv2.IMREAD_GRAYSCALE)

    # Initialize a list to store found template positions
    found_positions = []

    # Search for each template in the main image
    for template, template_path in templates:
        if template is None:
            continue

        # Perform template matching
        result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)

        # Get the coordinates of the matches
        threshold = 0.9  # Adjust the threshold as needed
        locations = np.where(result >= threshold)

        # Add the template size and positions to the list
        template_height, template_width = template.shape
        for y, x in zip(*locations):
            found_positions.append(
                (x, y, template_width, template_height, template_path)
            )

    # Sort positions from left to right based on x-coordinate
    sorted_positions = sorted(found_positions, key=lambda pos: (pos[1], pos[0]))

    return sorted_positions


def take_screenshot(region=None):
    """
    Take a screenshot of a specific region.

    Args:
        region (tuple): A tuple of (left, top, width, height) specifying the region to capture.

    Returns:
        The screenshot image as a numpy array.
    """
    with mss.mss() as sct:
        # Define the monitor or region to capture
        monitor = (
            sct.monitors[1]
            if region is None
            else {
                "top": region[1],
                "left": region[0],
                "width": region[2],
                "height": region[3],
            }
        )

        # Take the screenshot
        screenshot = sct.grab(monitor)

        # Convert to a format compatible with OpenCV
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        return img


def draw_results(image_path, sorted_positions):
    # Load the main image
    image = cv2.imread(image_path)

    for x, y, w, h, template_path in sorted_positions:
        # Draw a rectangle around each found template
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save or display the result
    cv2.imshow("Detected Templates", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def load_images_from_folder(folder_path):
    """
    Load all image files from a specified folder and return them as a list of images.

    Args:
        folder_path (str): Path to the folder containing images.

    Returns:
        List of images.
    """
    images = []
    folder = pathlib.Path(folder_path)

    # List all image files in the folder
    for image_file in folder.glob("*.*"):
        # Load the image
        image = cv2.imread(str(image_file), cv2.IMREAD_GRAYSCALE)
        if image is not None:
            images.append((image, str(image_file)))  # Store image and file path
        else:
            print(f"Warning: Unable to load image {image_file}")

    return images


def get_template_names(templates):
    """
    Get the names of the template images.

    Args:
        templates (list): List of tuples with (template_image, template_path).

    Returns:
        Concatenated string of template names.
    """
    names = [
        pathlib.Path(template_path).stem
        for _, _, _, _, template_path in sorted_positions
    ]
    return "".join(names)


def assume_coords(names_str):
    if names_str and len(names_str) > 8:
        return {
            "x": names_str[0:4],
            "y": names_str[4:8],
            "z": names_str[8],
        }


# Example usage
main_image_path = "./imgs/region.png"
template_paths = load_images_from_folder("./fonts/Numbers")
region = (773, 527, 124, 55)

while True:
    ss = take_screenshot(region)
    sorted_positions = find_and_sort_templates(ss, template_paths)
    names = get_template_names(sorted_positions)
    # print("names: ", names)
    print("coords: ", assume_coords(names))
    # draw_results(main_image_path, sorted_positions)
    time.sleep(2)
