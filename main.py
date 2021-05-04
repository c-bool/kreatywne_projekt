import numpy as np
import cv2


def remove_zero_pixels(image_filename):
    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    picture_px[np.where((picture_px == [255, 255, 255]).all(axis=2))] = [254, 254, 254]

    return picture_px


def encode(image_filename, msg_to_encode):
    picture_px = remove_zero_pixels(image_filename)
    rows_for_chars = np.linspace(0, picture_px.shape[0], len(msg_to_encode), endpoint=False, dtype=int)
    for i, char in enumerate(msg_to_encode):
        picture_px[rows_for_chars[i], ord(char)] = [255, 255, 255]
    cv2.imwrite(image_filename, picture_px, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])


def decode(image_filename):
    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    encoded_chars_found = np.where((picture_px == [255, 255, 255]).all(axis=2))[1]

    return "".join([chr(x) for x in encoded_chars_found])


encode("test.png", "Hello World!!")
print(decode("test.png"))
