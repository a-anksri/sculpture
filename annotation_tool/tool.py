#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from link import Link, Chain
from annotation import *
from gui import *
import numpy as np
import cv2 as cv

drag = False
ix = 0
iy = 0
def dummy_handler(event,x,y,flags, params):
    pass

def handler(event, x, y, flags, params):
    global drag, ix, iy
    
    annot = params[0]
    gui = params[1]
    state = annot.get_state()
    
    if(event == cv.EVENT_RBUTTONUP):
        out = gui.check_within_image(x,y)
        if(drag):
            drag = False
            ix = 0
            iy = 0
            gui.reset_pan()
            gui.reset_alert("Pan Mode Off")
            
            return
        
        
        drag = True
        ix = x
        iy = y
        
        
        gui.alert("Pan mode On, Right Click Again to Deactivate", "", old = False)
                
        
        
        
    if(event == cv.EVENT_MOUSEMOVE):
        
        if(drag):
            out = gui.check_within_image(x,y)
            if(out):
                
                gui.pan(ix - x, iy - y)
                
    
    
    
    
    
    if(event == cv.EVENT_LBUTTONUP):
        
        if(drag):
            
            return
        
        if(gui.dialog_on):
            num = gui.check_within_buttons(x,y)
            if(num > -1):
                
                if(num == 0):
                    out = annot.do_confirm(num)
                    
                    
                    if(out == 1):
                        gui.add_message("Select another " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Recorded")
                    else:
                        gui.add_message("Select a " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Recorded")
                    gui.reset_dialog()
                    
                    
                    
                    
                elif(num == 1):
                    out = annot.do_confirm(num)
                    if(out == 1):
                        gui.add_message("Select another " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Recorded")
                    else:
                        gui.add_message("Select a " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Recorded")
                    gui.reset_dialog()
                    
                    
                else:
                    out = annot.dont_confirm()
                    if(out == 1):
                        gui.add_message("Select another " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Cancelled")
                    else:
                        gui.add_message("Select a " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Cancelled")
                    gui.reset_dialog()
                    
                gui.flush_canvas()
                  
                gui.add_elements(annot.parent_link)
                    
            return
        
        
        
        gui.flush_canvas()
        num = gui.check_within(x,y)
        if num > -1:
            
            
            annot.set_child(num)
            
            if(annot.next_link.get_type() == "Root"):
                    gui.add_message("Annotation Complete" "ANN")
                    
                    return
            
    
            gui.add_message("Select a " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "")
            gui.add_elements(annot.parent_link)
            
        
        
        num = gui.check_image_controls(x,y)
        if (num > -1):
            gui.image_position(num)
            
        out = gui.check_within_image(x,y)
        x1,y1 = gui.rescale_coords(x,y)
        
        if(out):
            gui.current_selx, gui.current_sely = x1, y1
            
            gui.add_dialog(x,y)
            annot.do_select(x1,y1)
            
            
        
            
        
        
