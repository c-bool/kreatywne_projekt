# Import built-ins
import logging
import os
import math
from pathlib import Path
# Import additional libraries
from cryptography.fernet import Fernet
import numpy as np
import cv2
import easygui
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


def read_input_image(image_filename):
    """
    Reads pixels of input image given by filename.

    :param image_filename: Filename of input image to encode message in as str
    :return: Image's pixels as numpy array
    """
    if not image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        logging.error("Image should be in png / jpg / jpeg format.")
        exit(1)

    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)

    try:
        _ = picture_px.shape  # will throw exception for corrupted/non-image files
    except Exception as e:
        print(e)
        logging.error("Image is not available or corrupted.")
        exit(1)

    return picture_px


def encode(input_image_filename, shift, msg_to_encode, output_image_filename):
    """
    Calls function for reading input image, then encoding given message in that image.

    :param input_image_filename: Filename of input image to encode message in as str
    :param shift: Shift value for encrypted pixels as int
    :param msg_to_encode: Message to encode in image as str
    :param output_image_filename: Filename of encoded image to save as str
    """
    logging.info("Encoding...")
    picture_px = read_input_image(input_image_filename)
    height, width, _ = picture_px.shape
    px_res = height * width
    msg_length = len(msg_to_encode)

    if msg_length > 3 * (px_res - 1):
        logging.error("Message is too long to be encoded in this image")
        exit(1)

    # Encode message length in the very first pixel
    picture_px[0, 0] = [byte for byte in msg_length.to_bytes(3, byteorder='little')]

    # Encode message across the whole image's pixels
    msg_tab = [*[char for char in msg_to_encode], *[' ' for _ in range(3 - (msg_length % 3))]]
    px_for_chars = np.linspace(1, px_res, math.ceil(msg_length / 3), endpoint=False, dtype=int)
    for px in px_for_chars:
        picture_px[math.floor(px / width), px % width] = [ord(char) + shift for char in msg_tab[:3]]
        del msg_tab[:3]
    picture_px[-1, -1] = [123, 123, 123]

    logging.info(f"Saving new image with encoded message to {output_image_filename}...")
    cv2.imwrite(output_image_filename, picture_px, [int(cv2.IMWRITE_PNG_COMPRESSION), 4])
    logging.info(f"Image with encoded message was saved to file {output_image_filename} in current working folder!")


def read_png_image(image_filename):
    """
    Reads pixels of png image given by filename.

    :param image_filename: Filename of image to decode message from as str
    :return: Image's pixels as numpy array
    """
    if not image_filename.lower().endswith('.png'):
        logging.error("Image must be in png format.")
        exit(1)

    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)

    try:
        _ = picture_px.shape  # will throw exception for corrupted/non-image files
    except Exception as e:
        print(e)
        logging.error("Image is not available or corrupted.")
        exit(1)

    if (picture_px[-1, -1] != [123, 123, 123]).all():
        logging.error("Image was not encoded using this tool.")
        exit(1)

    return picture_px


def decode(image_filename, shift):
    """
    Decodes message hidden in given image.

    :param image_filename: Filename of image to decode message from as str
    :param shift: Shift value for encrypted pixels as int
    :return: Decoded message from image as str
    """
    logging.info("Decoding...")
    picture_px = read_png_image(image_filename)
    height, width, _ = picture_px.shape
    px_res = height * width

    msg_len = int.from_bytes(picture_px[0, 0], byteorder='little')

    px_with_chars = np.linspace(1, px_res, math.ceil(msg_len / 3), endpoint=False, dtype=int)
    msg_tab = []
    for px in px_with_chars:
        msg_tab = [*msg_tab, *[x - shift for x in picture_px[math.floor(px / width), px % width]]]

    return "".join([chr(x) for x in msg_tab])


def main():
    while True:
        choice = easygui.indexbox(msg='What do you want to do?', title='Color Code',
                                  choices=['Encode', 'Decode', 'Exit'], image="icon.jpeg", cancel_choice='No')
        if choice == 0:
            default_text = 'Enter message to encode here...'
            msg = easygui.textbox(msg='Enter message to encode', title='Color Code', text=default_text)
            if msg is None:
                logging.warning("Cancelled or entered empty string.")
                continue

            shift = easygui.integerbox(msg='Enter shift value for encode', title='Color Code', default=0,
                                       lowerbound=0, upperbound=30)
            if shift is None:
                continue

            filename = easygui.fileopenbox(msg="Select image to encode", title='Color Code', default="*.png",
                                           filetypes=["*.png", "*.jpg", "*.jpeg", "Image files"], multiple=False)
            if filename is None:
                continue

            while True:
                save_filename = easygui.enterbox(msg="Save encoded image as..", title='Color Code',
                                                 default=f"encoded_{Path(filename).stem}.png")
                if not save_filename or save_filename.endswith('.png'):
                    break
                else:
                    logging.warning("Output image to save must be in png format!")
            if save_filename is None:
                continue

            encode(filename, shift, msg, save_filename)
        elif choice == 1:
            filename = easygui.fileopenbox(msg="Select image to decode", title='Color Code',
                                           default="encoded_*.png", filetypes="*.png", multiple=False)
            if filename is None:
                continue

            shift = easygui.integerbox(msg='Enter shift value for decode', title='Color Code', default=0)
            if shift is None:
                continue

            easygui.msgbox(msg=f"Message encoded in image is:\n\n{decode(filename, shift)}", title='Color Code',
                           ok_button='Continue')
        else:
            exit(0)


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

    fr.recognize_face()
    decrypt_access_phrase()
    main()
