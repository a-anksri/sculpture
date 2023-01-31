import numpy as np
import pandas as pd
import cv2 as cv
from gui.gui import Element, Gui
from link.link import Link, Chain

landmarks = ["Root", "Forehead", "Left Eye", "Left Ear", "Left Shoulder", "Left Waist", "Right Eye", "Right Ear", "Right Shoulder", "Right Waist", "Nose", "Left Elbow", "Left Knee", "Right Elbow", "Right Knee", "Left Wrist", "Left Foot", "Right Wrist", "Right Foot"]
limbs = {"Root":[1], "Forehead":[10,2,3,6,7,4,5,8,9], "Left Shoulder":[11], "Left Elbow": [15], "Left Waist":[12], "Left Knee": [16], "Right Shoulder":[13], "Right Elbow": [17], "Right Waist":[14], "Right Knee": [18]}
possible_duplicates = [1,11,12,13,14]

def handler(event, x, y, flags, params):
    if(event == cv.EVENT_LBUTTONUP):
        num = gui.check_within(x,y)
        if num > -1:
            gui.set_current_element(num)
        
    
        num = gui.check_image_controls(x,y)
        if (num > -1):
                
            gui.image_position(num)
        
gui = Gui()
chain = Chain(landmarks, limbs, possible_duplicates)
root = chain.get_root()
link = root.children[0]
#link = link.children[5]
gui.add_message("hi", "there")
gui.add_elements(link)
gui.set_current_element(0)
img = cv.imread('noc.png')
gui.add_image(img)
gui.add_image_controls()
cv.namedWindow("View")
cv.setMouseCallback("View", handler)

while(True):
    window = gui.compose()
    cv.imshow("View", window)
    a = cv.waitKey(20)
    
    if (a == ord('q')):
        
        break
cv.destroyAllWindows()
