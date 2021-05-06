# Import built-ins
import logging
import os
import math
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
    h = picture_px.shape[0]
    w = picture_px.shape[1]
    px_res = h * w

    if len(msg_to_encode) > 3 * px_res:
        logging.error("Message is too long to be encoded in this image")
        exit(1)

    px_for_chars = np.linspace(1, px_res, math.ceil(len(msg_to_encode)/3), endpoint=False, dtype=int)

    msg_len = []
    n = len(msg_to_encode)
    for _ in range(3):
        n, i = divmod(n, 256)
        msg_len.append(i) 

    picture_px[0, 0] = [msg_len[0], msg_len[1], msg_len[2]]

    msg_tab = []
    for ch in msg_to_encode:
        msg_tab.append(ch)
    if len(msg_to_encode) % 3:
        for i in range(0, 3 - (len(msg_to_encode) % 3) ):
            msg_tab.append(" ")

    for px in px_for_chars:
        #print(msg_tab)
        picture_px[math.floor(px / w), px % w] = [ord(msg_tab[0]) + shift, ord(msg_tab[1]) + shift, ord(msg_tab[2]) + shift]
        msg_tab.pop(2)
        msg_tab.pop(1)
        msg_tab.pop(0)
        
    cv2.imwrite(image_filename, picture_px, [int(cv2.IMWRITE_PNG_COMPRESSION), 4])


def decode(image_filename, shift):
    """
    Decodes message hidden in given image.

    :param image_filename: Filename of image to decode message from as str
    :param shift: Shift value for encrypted pixels as int
    :return: Decoded message from image as str
    """
    picture_px = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)

    h = picture_px.shape[0]
    w = picture_px.shape[1]
    px_res = h * w

    px_len = picture_px[0, 0]
    msg_len = px_len[0] + (px_len[1] << 8) + (px_len[2] << 16)

    px_with_chars = np.linspace(1, px_res, math.ceil(msg_len/3), endpoint=False, dtype=int)

    msg_tab = []
    for px in px_with_chars:
        char = picture_px[math.floor(px / w), px % w]
        msg_tab.append(char[0] - shift)
        msg_tab.append(char[1] - shift)
        msg_tab.append(char[2] - shift)

    return "".join([chr(x) for x in msg_tab])


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

    fr.recognize_face()
    decrypt_access_phrase()
    encode("test.png", 0, "Sex reached suppose our whether. Oh really by an manner sister so. One sportsman tolerably him extensive put she immediate. He abroad of cannot looked in . Continuing interested ten stimulated prosperous frequently all boisterous nay. Of oh really he extent horses wicket.She who arrival end how fertile enabled. Brother she add yet see minuter natural smiling article painted. Themselves at dispatched interested insensible am be prosperous reasonably it. In either so spring wished. Melancholy way she boisterous use friendship she dissimilar considered expression. Sex quick arose mrs lived. Mr things do plenty others an vanity myself waited to. Always parish tastes at as mr father dining at. Name were we at hope. Remainder household direction zealously the unwilling bed sex. Lose and gay ham sake met that. Stood her place one ten spoke yet. Head case knew ever set why over. Marianne returned of peculiar replying in moderate. Roused get enable garret estate old county. Entreaties you devonshire law dissimilar terminated.Passage its ten led hearted removal cordial. Preference any astonished unreserved mrs. Prosperous understood middletons in conviction an uncommonly do. Supposing so be resolving breakfast am or perfectly. Is drew am hill from mr. Valley by oh twenty direct me so. Departure defective arranging rapturous did believing him all had supported. Family months lasted simple set nature vulgar him. Picture for attempt joy excited ten carried manners talking how. Suspicion neglected he resolving agreement perceived at an. Her old collecting she considered discovered. So at parties he warrant oh staying. Square new horses and put better end. Sincerity collected happiness do is contented. Sigh ever way now many. Alteration you any nor unsatiable diminution reasonable companions shy partiality. Leaf by left deal mile oh if easy. Added woman first get led joy not early jokes.To shewing another demands to. Marianne property cheerful informed at striking at. Clothes parlors however by cottage on. In views it or meant drift to. Be concern parlors settled or do shyness address. Remainder northward performed out for moonlight. Yet late add name was rent park from rich. He always do do former he highly.e share of first to worse. Weddings and any opinions suitable smallest nay. My he houses or months settle remove ladies appear. Engrossed suffering supposing he recommend do eagerness. Commanded no of depending extremity recommend attention tolerably. Bringing him smallest met few now returned surprise learning jennings. Objection delivered eagerness he exquisite at do in . Warmly up he nearer mr merely me.Made last it seen went no just when of by. Occasional entreaties comparison me difficulty so themselves. At brother inquiry of offices without do my service. As particular to companions at sentiments. Weather however luckily enquire so certain do. Aware did stood was day under ask. Dearest affixed enquire on explain opinion he. Reached who the mrs joy offices pleased. Towards did colonel article any parties.So delightful up dissimilar by unreserved it connection frequently. Do an high room so in paid. Up on cousin ye dinner should in . Sex stood tried walls manor truth shy and three his. Their to years so child truth. Honoured peculiar families sensible up likewise by on in .It as announcing it me stimulated frequently continuing. Least their she you now above going stand forth. He pretty future afraid should genius spirit on. Set property addition building put likewise get. Of will at sell well at as. Too want but tall nay like old. Removing yourself be in answered he. Consider occasion get improved him she eat. Letter by lively oh denote an.")
    print(decode("test.png", 0))
