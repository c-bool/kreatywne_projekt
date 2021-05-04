# Import built-ins
import logging
import os
# Import additional libraries
from cryptography.fernet import Fernet
import numpy as np
import cv2
# Import project files
import face_recognize as fr


def load_key():
    """
    Loads the previously generated secret key needed to run a program.

    :return: Key from secret file as bytes
    """
    if not os.path.isfile("secret.key"):
        logging.error("Missing file with secret key.")
        exit(1)

    with open("secret.key", "rb") as key_file:
        key = key_file.read()

    return key


def decrypt_access_phrase():
    """
    Decrypts an encrypted message needed to run a program with secret key from file.
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(b'gAAAAABgkYiAKkDlmOx9IlKdMYz9Pw5Wo5Qru7atcCfa0pQxXKGubY8w0iVPBsF'
                                  b'-ZGAVg_sSPp6BcxazmCUQJFU5d0At9ntkjQ==')

    if decrypted_message.decode() != 'klucz_dostepu':
        logging.error("File secret.key found but key is invalid.")
        exit(1)

    logging.info("Key from secret.key is correct!")


def remove_white_pixels(image_filename):
    """
    Removes all white pixels ([255, 255, 255]) in image given by filename.
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


def encode(image_filename, shift, msg_to_encode):
    """
    Calls function for pre-processing input image, then encoding given message in that image.

    :param image_filename: Filename of image to encode message in as str
    :param shift: Shift value for encrypted pixels as int
    :param msg_to_encode: Message to encode in image as str
    """
    picture_px = remove_white_pixels(image_filename)
    rows_for_chars = np.linspace(0, picture_px.shape[0], len(msg_to_encode), endpoint=False, dtype=int)
    for i, char in enumerate(msg_to_encode):
        picture_px[rows_for_chars[i], ord(char)+shift] = [255, 255, 255]
    cv2.imwrite(image_filename, picture_px, [int(cv2.IMWRITE_PNG_COMPRESSION), 4])


def decode(image_filename, shift):
    """
    Decodes message hidden in given image.

    :param image_filename: Filename of image to decode message from as str
    :param shift: Shift value for encrypted pixels as int
    :return: Decoded message from image as str
    """
    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    encoded_chars_found = np.where((picture_px == [255, 255, 255]).all(axis=2))[1] - shift

    return "".join([chr(x) for x in encoded_chars_found])


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

    fr.recognize_face()
    decrypt_access_phrase()
    encode("test.png", 15, "Hello World!!")
    print(decode("test.png", 15))
