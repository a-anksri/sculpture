

class Element:
    
    def __init__(self,text, duplicate, offset, dim, default = 0):
        self. x_offset = offset[0]
        self.y_offset = offset[1]
        self.color1 = [(0,255,0),(255,0,0),(0,255,255),(0,0,0)]
        self.color2 = [(0,0,0),(255,255,255),(0,0,0),(255,255,255)]
        self.dim = dim
        self.text = text
        self.default = default
        self.state = 0
        
        
    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def has(self,x,y, menu_offset):
        if((x > menu_offset[0] + self.x_offset) and (x < menu_offset[0] + self.x_offset + self.dim[0]) and (y > menu_offset[1] + self.y_offset) and (y < menu_offset[1] + self.y_offset + self.dim[1])):
           return (True)
        return (False)
    
    def set_back_color(self,color):
        self.color1.append(color)
        return(len(self.color1) - 1)
        
    def set_font_color(self,color):
        self.color1.append(color)
        return(len(self.color1) - 1)
        

class Gui:
    
    def __init__(self):
        
        self.image = None
        self.msg1 = None
        self.msg2 = None
        self.elements = []
        self.image_controls = []
        self.canvas = None
        self.buttons = []
        
        self.scale = 1.0
        self.x_pan = 0
        self.y_pan = 0
        self.imx1 = 0
        self.imy1 = 0
        self.imx2 = 0
        self.imy2 = 0
        self.dialog_on = False
        
        
        #nth child element is to be highlighted
        self.num = 0
        
        
        self.image_offset = (5,5)
        self.message_offset = (0,630)
        self.menu_offset = (900,0)
        self.message_size = (900,130)
        self.menu_size = (128,760)
        self.image_size = (900,630)
        self.button_offset = (0,0)
        self.button_size = (600,300)
        
        
        self.current_list = [] #??
        
        self.base = np.zeros((760,1028,3), np.uint8)
        
        self.message_pane_base = np.zeros((130,900,3), np.uint8)
        self.message_pane_base[:,:,1] = np.ones((130,900), np.uint8) * 64
        self.message_pane_base[:,:,2] = np.ones((130,900), np.uint8) * 140
        self.button_base = np.ones((300,600), np.uint8)
        self.menu_pane_base = np.zeros((760,128,3), np.uint8)
        self.menu_pane_base[:,:,1] = np.ones((760,128), np.uint8)
        self.menu_pane_base[:,:,2] = np.ones((760,128), np.uint8) * 128
        
        self.image_pane_base = np.zeros((630,900,3), np.uint8)
        
        self.window = self.base.copy()
        self.image_pane = self.image_pane_base.copy()
        self.menu_pane = self.menu_pane_base.copy()
        self.message_pane = self.message_pane_base.copy()
        self.dialog_pane = self.dialog_base.copy()
        
        
    #Adding matter to panes  
    def add_message(self, msg1 = None, msg2 = None, retain = True):
        if(retain):
            if(msg1 is None):
                pass
            else:
                self.msg1 = msg1
            if(msg2 is None):
                pass
            else:
                self.msg2 = msg2
        
        else:
            if(msg1 is None):
                self.msg1 = ''
            else:
                self.msg1 = msg1
            if(msg2 is None):
                self.msg1 = ''
            else:
                self.msg2 = msg2
    
    def add_elements(self, current):
        self.current_link = current
        current_children = self.current_link.children
        gap = int(600/(len(current_children)+1) - 30)
        offset = gap+50
        for i in current_children:
            element = Element(i.get_type(), i.duplicate_possible, (10,offset), (100,30))
            offset += gap + 30
            self.elements.append(element)
        self.elements[0].set_state(1)
    
    def add_dialog():
        pass
    
    def add_image_controls(self):
        self.image_controls.append(Element('+', False, (10,650),(20,20)))
        self.image_controls.append(Element('-', False, (80,650),(20,20)))
        self.image_controls.append(Element('->', False, (80,720),(20,20)))
        self.image_controls.append(Element('<-', False, (10,720),(20,20)))
        self.image_controls.append(Element('up', False, (45,690),(20,20)))
        self.image_controls.append(Element('down', False, (45,690),(20,20)))
    
    def add_image(self, img):
        self.image = img
        
        width = img.shape[1]
        height = img.shape[0]
        
        sc_x = self.image_size[0]/width
        sc_y = self.image_size[1]/height
        self.scale = min(sc_x, sc_y)
        self.canvas = self.image
     
    #setting properties of elements in each pane
     def set_current_element(self, num):
        print(self.num)
        if(num <= self.num):
            return(-1)
        if(num > len(self.elements)):
            return(-1)
        for i in range(num):
            self.elements[i].set_state(2)
        
        self.elements[num].set_state(1)
        self.num = num
        
    def image_position(self, num):
        if(num == 0): #zoom up
            self.scale = self.scale * 1.1
        elif (num == 1): #zoom down
            if(self.image.shape[1] * self.scale < self.image_size[0]) and (self.image.shape[0] * self.scale < self.image_size[1]):
                pass
            else:
                self.scale = self.scale / 1.1
        elif (num == 2): #pan  right
            inc = int(min(50, self.image.shape[1] * self.scale - self.x_pan - self.image_size[0]))
            inc = max(0, inc)
            self.x_pan += inc
        elif (num == 3): #pan left
            inc = min(50, self.x_pan)
            self.x_pan -= inc
        elif (num == 5): #pan  down
            inc = int(min(50, self.image.shape[0] * self.scale - self.y_pan - self.image_size[1]))
            inc = max(0, inc)
            self.y_pan += inc
        elif (num == 4): #pan up
            inc = min(50, self.y_pan)
            self.x_pan -= inc
    
    def check_within(self, x, y):
        #print(x,y)
        for i, element in enumerate(self.elements):
            if (element.has(x,y, self.menu_offset)):
                return(i)
            
        return(-1)
    
    def check_image_controls(self, x, y):
        #print(x,y)
        for i, element in enumerate(self.image_controls):
            if (element.has(x,y, self.menu_offset)):
                return(i)
            
        return(-1)
        
    
    #composing individual panes
    def compose_image(self):
        scale = self.scale
        x_pan = self.x_pan
        y_pan = self.y_pan
        x_pos = 0
        y_pos = 0
        cp = self.canvas.copy()
        width = cp.shape[1]
        height = cp.shape[0]
        
        sc_width = int(scale * width)
        sc_height = int(scale * height)
        self.x_pan = min(self.x_pan, sc_width - self.image_size[0])
        self.y_pan = min(self.y_pan, sc_height - self.image_size[1])
        
        if(sc_width <= self.image_size[0]):
            x_pan = 0
            self.x_pan = 0
            x_pos = int((self.image_size[0] - sc_width)/2)
        
        if(sc_height <= self.image_size[1]):
            y_pan = 0
            self.y_pan = 0
            y_pos = int((self.image_size[1] - sc_height)/2)
        
        
        
        cp = cv.resize(cp, (sc_width, sc_height))
        
        im_width = int(min(sc_width, self.image_size[0]))
        im_height = int(min(sc_height, self.image_size[1]))
        cp = cp[self.y_pan:self.y_pan + im_height, self.x_pan:self.x_pan + im_width,:]
        
        
        self.image_pane[y_pos:y_pos+im_height, x_pos: x_pos + im_width,:] = cp
        
        
        
    
    
    
    def compose_message(self):
        
        pane = cv.putText(self.message_pane, self.msg1, (20,40), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = 1.5, color =  (0,255,255), thickness = 2)
        self.message_pane = cv.putText(pane, self.msg2, (20,100), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = 1, color =  (0,255,255), thickness = 2)
     
    
    def compose_menu(self):
        
        scale = 1.0
        name = self.current_link.get_type()
        l = len(name)
        if(l <= 8):
                scale = 0.75
        else:
                scale = 6.0/l
        self.menu_pane = cv.putText(self.menu_pane, name, (15, 35), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = scale, color = (0,255,255), thickness = 3  )
        
        for i in self.elements:
            
            l = len(i.text)
            if(l <= 12):
                scale = 0.5
            else:
                scale = 6.0/l
                
            color1 = i.color1[i.state]
            color2 = i.color2[i.state]
            init_y = i.y_offset
            init_x = i.x_offset
            self.menu_pane = cv.rectangle(self.menu_pane, (init_x, init_y), (init_x + i.dim[0], init_y + i.dim[1]), color = color1, thickness = -1 )
            self.menu_pane = cv.putText(self.menu_pane, i.text, (init_x+5, init_y + 15), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = scale, color = color2, thickness = 2  )
        
        for i in self.image_controls:
            
            init_y = i.y_offset
            init_x = i.x_offset
            self.menu_pane = cv.rectangle(self.menu_pane, (init_x, init_y), (init_x + i.dim[0], init_y + i.dim[1]), color = color1, thickness = -1 )
            self.menu_pane = cv.putText(self.menu_pane, i.text, (init_x+5, init_y + 15), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = scale, color = color2, thickness = 3  )


        
    def compose(self):
        self.compose_message()
        self.compose_menu()
        self.compose_image()
        self.window[self.message_offset[1]:self.message_offset[1] + self.message_size[1], self.message_offset[0]:self.message_offset[0] + self.message_size[0],:] = self.message_pane
        self.window[self.menu_offset[1]:self.menu_offset[1] + self.menu_size[1], self.menu_offset[0]:self.menu_offset[0] + self.menu_size[0],:] = self.menu_pane
        self.window[self.image_offset[1]:self.image_offset[1] + self.image_size[1], self.image_offset[0]:self.image_offset[0] + self.image_size[0],:] = self.image_pane
        self.menu_pane = self.menu_pane_base.copy()
        self.message_pane = self.message_pane_base.copy()
        self.image_pane = self.image_pane_base.copy()
        return self.window.copy()
        
