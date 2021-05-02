from PIL import Image
from tqdm import tqdm

def prepareIMG(): #remove empty pixels if exist
    with Image.open("test.jpg") as im:
        width, height = im.size
        im = im.convert("RGB") #convert to (R, G, B) format
    count = 0
    px = im.load()
    for row in tqdm(range(height)):
        for col in range(width - 1):
            if px[col, row] == (255, 255, 255):
                count += 1
                px[col, row] == (254, 254, 254)
    return im #return picture w/o empty pixsels


def encode(picture, msg): #encode msg in picture
    msg_tab = [] 
    for char in msg:
        msg_tab.append(ord(char)) #create tab with ascii values of msg
    row = 0
    col = 0
    width, height = picture.size
    px = picture.load()
    for x in tqdm(msg_tab):
        if col + x <= width: #select col if in range
            col += x
        else: #go to next row if not in range
            row += 1
            col = 1 + x
        px[col, row] = (255, 255, 255) #set empty pixel
    return picture #return encoded msg in picture

def decode(picture):
    width, height = picture.size
    count = 0 #ascci value counter
    px = picture.load()
    msg_tab = []
    for row in tqdm(range(height)): #iterate through all pixels
        for col in range(width - 1):
            if px[col, row] == (255, 255, 255): #if empty pixel, save current counter and reset it
                msg_tab.append(count)
                count = 0
            count += 1
        count = 0 #reset counter when in next row
    s = ""
    for x in msg_tab: #decode ascii values and add to string
        s += chr(x)
    return s #return msg

print(decode(encode(prepareIMG(), "Hello World!!")))
