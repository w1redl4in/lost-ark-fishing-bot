import threading
import cv2 as cv
import numpy as np
import keyboard
from PIL import ImageGrab
import time
import random
from tkinter import *

should_cast = True
is_fishing = False
fishing_running_count = 0

screen = Tk()
screen.title('Lost Ark Fishing Bot')
screen.geometry('500x300')

def delay_to_start_fishing (): 
    time.sleep(3)


def destroy_all_labels ():
    for label in screen.winfo_children():
        if isinstance(label, Label):
            label.destroy()

def background(func):
    t = threading.Thread(target=func)
    t.start()

def handle_log_thresholds (min, max, accepted):
    global fishing_running_count
    fishing_running_count = fishing_running_count + 1
    max_log_count = 10
    
    text = f"Min Threshold: {round(min, 1)} - Max Threshold: {round(max, 2)} - Accepted Threshold: {round(accepted, 2)}"

    global threshold_label

    threshold_label = Label(screen, text = text)
    threshold_label.pack()

    if(fishing_running_count == max_log_count):
        print("fechar")
        destroy_all_labels()
        fishing_running_count = 0

def handle_stop_fishing ():
    global is_fishing
    global fishing_running_count
    global should_cast
    should_cast = True
    is_fishing = False
    fishing_running_count = 0
    print("Parando de pescar...")
    destroy_all_labels()

def handle_start_fishing ():
    template = cv.imread('lure.png', 0)

    global is_fishing
    global should_cast
    is_fishing = True

    # delay_to_start_fishing()

    while is_fishing:
        
        if (should_cast):
            print("Jogando a isca")

            keyboard.press_and_release('e')

            should_cast = False

            continue

        img_pixels = ImageGrab.grab(bbox=(0, 0, 1920, 1080))

        img_rgb = np.array(img_pixels)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        match_template_response = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

        accepted_threshold = 0.81
        min_threshold = np.min(match_template_response)
        max_threshold = np.max(match_template_response)

        handle_log_thresholds(min_threshold, max_threshold, accepted_threshold)
        
        loc = np.where(match_template_response >= accepted_threshold)

        for pt in zip(*loc[::-1]):
            if pt != None:
                print("Peixe detectado! Puxando isca")
                keyboard.press_and_release('e')
                should_cast = True
                time.sleep(random.uniform(6, 7.5))
                break

        time.sleep(0.100)

start_fishing_button = Button(screen, text = "Pescar!", command=lambda: background(handle_start_fishing))
stop_fishing_button = Button(screen, text = "Parar de pescar", command=lambda: background(handle_stop_fishing))

start_fishing_button.pack()
stop_fishing_button.pack()
     
screen.mainloop()