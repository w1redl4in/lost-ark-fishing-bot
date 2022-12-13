import cv2 as cv
import numpy as np
import keyboard
from PIL import ImageGrab
import time
import random

cast = True
template = cv.imread('lure.png', 0)
w, h = template.shape[::-1]

while True:
    if (cast):
        print("Jogando a isca")
        keyboard.press_and_release('e')
        cast = False
        continue

    img_pixels = ImageGrab.grab(bbox=(0, 0, 1920, 1080))

    img_rgb = np.array(img_pixels)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    match_template_response = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

    accepted_threshold = 0.81
    min_threshold = np.min(match_template_response)
    max_threshold = np.max(match_template_response)

    print(accepted_threshold, max_threshold, min_threshold)
    
    loc = np.where(match_template_response >= accepted_threshold)

    for pt in zip(*loc[::-1]):
        if pt != None:
            print("Peixe detectado! Puxando isca")
            keyboard.press_and_release('e')
            cast = True
            time.sleep(random.uniform(6, 7.5))
            break

    time.sleep(0.100)









