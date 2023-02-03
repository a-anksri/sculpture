#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#trying git

from tool import tool_GUI
from annotation import Final_Annotation
import pandas as pd
import numpy as np
import cv2 as cv
import sys

#returns pandas database with annotations for the 
if(__name__ == "__main__"):
    if(len(sys.argv) <= 1):
        file_name = "noc.png"
    else:
        file_name = sys.argv[1]

   
    All_annotations = Final_Annotation()
    
    #Change image name here
    
    img = cv.imread(file_name)
    
    
    tool_GUI('img_name', All_annotations, img = img)
    a = All_annotations.annotations
    for i in range(len(a['id'])):
        print(a["img_id"][i], a['person'][i], a['id'][i], a['pid'][i], a['type'][i])
    table = pd.DataFrame(a)

