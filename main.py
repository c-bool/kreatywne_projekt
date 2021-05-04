# Import built-ins
import logging
# Import additional libraries
import numpy as np
import cv2


def remove_white_pixels(image_filename):
    """
    Removing all white pixels ([255, 255, 255]) in image given by filename.
    This pre-processing is needed because encoded message will be hidden in white pixels.

    :param image_filename: Filename of image to remove all white pixels in as str
    :return: Image's pixels as numpy array
    """
    if not image_filename.lower().endswith('.png'):
        logging.error("Image should be in png format.")
        exit(1)

    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)

    try:
        _ = picture_px.shape  # will throw exception for corrupted/non-image files
    except Exception as e:
        print(e)
        logging.error("Image is not available or corrupted.")
        exit(1)

    picture_px[np.where((picture_px == [255, 255, 255]).all(axis=2))] = [254, 254, 254]

    return picture_px


def encode(image_filename, msg_to_encode):
    """
    Calling function for pre-processing input image, then encoding given message in that image.

    :param image_filename: Filename of image to encode message in as str
    :param msg_to_encode: Message to encode in image as str
    """
    picture_px = remove_white_pixels(image_filename)
    rows_for_chars = np.linspace(0, picture_px.shape[0], len(msg_to_encode), endpoint=False, dtype=int)
    for i, char in enumerate(msg_to_encode):
        picture_px[rows_for_chars[i], ord(char)] = [255, 255, 255]
    cv2.imwrite(image_filename, picture_px, [int(cv2.IMWRITE_PNG_COMPRESSION), 4])


def decode(image_filename):
    """
    Decoding message hidden in given image.

    :param image_filename: Filename of image to decode message from as str
    :return: Decoded message from image as str
    """
    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    encoded_chars_found = np.where((picture_px == [255, 255, 255]).all(axis=2))[1]

    return "".join([chr(x) for x in encoded_chars_found])


logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
encode("test.png", "Hello World!!")
print(decode("test.png"))
