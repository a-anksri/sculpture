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
            
            
        
def tool_GUI(img_name, All_annotations, img = None):
  
  gui = Gui()
  person_id = 0
  
  
  
  gui.add_image(img)
  gui.add_image_controls()
  
  
  
  
  while(True):
    
    annot = Annotation_noGUI(landmarks, limbs, possible_duplicates, person_id = person_id, img_id = img_name)
    annot.start_annotation()
    cv.namedWindow("View")
    cv.setMouseCallback("View", handler, (annot,gui) )
    
    gui.add_elements(annot.parent_link)
    gui.set_current_element(0)
    gui.add_message("Select a Forehead", "Starting New person")

    annot.set_state('select')
    gui.flush_canvas()
    more = False
    complete = False
    to_save = True
    alert = False

    
    
    while(True):

        
        
        num = annot.get_child()
        
        
        gui.set_current_element(num)
        if(annot.next_link.get_type() == 'Root'):
            gui.add_message("Annotation Complete","Press 'a' to save and add person, Press 's' to save and quit, 'q' to quit without saving")
            annot.set_state('main')
            cv.setMouseCallback("View", dummy_handler, (annot,gui) )
            complete = True
        
        gui.cx, gui.cy, gui.cz = annot.traverse(annot.current_parent)
        window = gui.compose()
            
        
        cv.imshow("View", window)
        
            
        a = cv.waitKey(20)
        
        if(annot.get_state() == 'confirm' and a == ord(' ')):
            out = annot.do_confirm(0)
                    
                    
            if(out == 1):
                    gui.add_message("Select another " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Recorded")
            else:
                    gui.add_message("Select a " + annot.next_link.get_type() + " connected to highlighted " + annot.parent_link.get_type(), "Selection Recorded")
            gui.reset_dialog()
            
            gui.flush_canvas()
                  
            gui.add_elements(annot.parent_link)
            
        if (a == ord('q') and complete):
            to_save = False
            break
        
        if (a == ord('q') and not complete):
            gui.add_message("Annotation is incomplete", "'a': Save and add person, 's': Save and Quit, 'x' Quit without saving, 'n': add person withou saving")
            alert = True
            
        elif(a == ord('a')):
            to_save = True
            more = True
            break
        
        elif(a == ord('s')):
            to_save = True
            more = False
            break
        
        elif(a == ord('x') and alert):
            to_save = False
            more = False
            break
            
        elif(a == ord('n') and alert):
            to_save = False
            more = True
            break
            
        
            
        
      
        
    
    if(to_save):
      next_id = All_annotations.append(annot)
      
    cv.destroyAllWindows()
    
    

    if(not more):
      break
    if(to_save):
        person_id += 1
          
        
        
