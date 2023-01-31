
class Link:

  def __init__(self, landmark, possible = False):
    self.landmark_type = landmark
    self.parent = self
    self.children = []
    self.next_child = 0
    self.duplicate_possible = possible
  
  def add_parent(self, parent):
    self.parent = parent

  def add_child(self, child):
    self.children.append(child)

  def get_type(self):
    return self.landmark_type

  def get_parent(self):
    return self.parent

  def check_over(self):
    if(self.next_child == len(self.children)):
      
      return(True)
    else:
      return(False)
  
  

class Chain:

  def __init__(self, landmarks, limbs, possible_duplicates):
    self.landmarks = landmarks
    self.limbs = limbs
    self.possible_duplicates = possible_duplicates
    self.links = {}
    for i, landmark in enumerate(self.landmarks):
      if(i in self.possible_duplicates):
        link = Link(landmark, True)
      else:
        link = Link(landmark, False)
      self.links[landmark] = link

    self.links["Root"].add_parent(None)

    for limb in limbs:
      parent = self.links[limb]
      for i in limbs[limb]:
        self.links[self.landmarks[i]].add_parent(parent)
        self.links[parent.get_type()].add_child(self.links[self.landmarks[i]])

  def get_root(self):
    return self.links["Root"]
  
  


  def traverse(self):
      next = self.links["Root"]
      while(next is not None):
        print(next.get_type())
        next, _ = next.successor()
        
