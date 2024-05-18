from circuit.components import *
from circuit.utils import *
from collections import defaultdict

class BreadBoard:
    '''
    Constructor define attributes and build basic canvas configuration
    '''
    def __init__(self, root: ctk.CTk):
        # attributes
        self.root = root
        self.canvas = ctk.CTkCanvas(root, width=1000, height=800) # canvas object
        self.pin_coordinates = [i*30+20 for i in range(50)] # 1d coordinates
        self.tracking = False # is tracking on?
        self.prev = Wire(self.canvas, [0, 0], [0, 0]) # useful to animation
        self.component = "wire"
        self.value = 0
        self.elements = [0]
        self.nodes = []
        self.connections = defaultdict(set)
        self.row = 0

        # click event listener
        self.canvas.bind("<Button-1>", lambda event, mode="TRACK": self.select(event, mode)) 

        # build breadboard
        '''for x in range(1, 50):
            self.canvas.create_text(x*30+20, 20, text=x, fill="black", font=('Fantasy 14 bold'))
            for y in range(1, 50):
                if y==1: 
                    self.canvas.create_text(20, x*30+20, text=x, fill="black", font=('Fantasy 14 bold'))
                self.canvas.create_aa_circle(y*30+20, x*30+20, 12, fill="darkgrey")'''
        self.elements = [
            Generator(self.canvas, [290, 260], [350, 260]),
            Generator(self.canvas, [290, 440], [350, 440]),
            Wire (self.canvas,[290, 260], [170, 260]),
            Wire (self.canvas,[170, 260], [170, 170]),
            Wire (self.canvas,[170, 170], [170, 80]),
            Wire (self.canvas,[170, 80], [770, 80]),
            Wire (self.canvas,[770, 80], [770, 170]),
            Wire (self.canvas,[770, 170], [770, 260]),
            Wire (self.canvas,[770, 260], [680, 260]),
            Wire (self.canvas,[680, 260], [680, 200]),
            Wire (self.canvas,[680, 200], [560, 200]),
            Wire (self.canvas,[560, 200], [560, 260]),
            Wire (self.canvas,[560, 260], [560, 320]),
            Wire (self.canvas,[560, 320], [680, 320]),
            Wire (self.canvas,[680, 320], [680, 260]),
            Wire (self.canvas,[560, 260], [350, 260]),
            Wire (self.canvas,[170, 170], [50, 170]),
            Wire (self.canvas,[50, 170], [50, 440]),
            Wire (self.canvas,[50, 440], [290, 440]),
            Wire (self.canvas,[350, 440], [860, 440]),
            Wire (self.canvas,[860, 440], [860, 170]),
            Wire (self.canvas,[860, 170], [770, 170])
        ]
        for el in self.elements:
                for comp in self.elements:
                    if el!=comp and (el.start==comp.start or el.end==comp.end or el.end==comp.start or el.start==comp.end):
                        self.connections[el.canvasID].add(comp.canvasID)
        self.study()

    '''
    Pin Managment
    mode="SELECT": return the nearest pin to event
    mode="TRACK": start and stop tracking, create line that follow the cursor
    '''
    def select(self, event, mode="SELECT"):
        # looking for the nearest pin 
        try:
            distance = [event.x, event.y]
        except:
            distance = event

        for p in self.pin_coordinates:
            distance[0] = min(distance[0], abs(event.x-p))
            distance[1] = min(distance[1], abs(event.y-p))
        
        selected = []
        if (event.x-distance[0]-20)%30==0:
            selected.append(event.x-distance[0])
        else:
            selected.append(event.x+distance[0])
        
        if (event.y-distance[1]-20)%30==0:
            selected.append(event.y-distance[1])
        else:
            selected.append(event.y+distance[1])
        
        # output
        if selected[0]>=30 and selected[1]>=30:
            if mode=="SELECT":
                return [selected[0], selected[1]]
            elif mode=="TRACK":
                self.__draw(selected)
                
    '''
    Draw a wire from point a to b
    '''
    def __draw(self, selected):
        if self.tracking:
            self.canvas.unbind("<Motion>")
            self.elements.append(self.prev)
            new = ctk.CTkButton(self.root, 
                                width=10, 
                                text=f"{self.prev.component}: {str(self.prev.canvasID)}", 
                                corner_radius=4, 
                                font=('Helvetica', 10), 
                                fg_color="red", 
                                command=lambda: self.__delete(new, new._text))
            new.grid(row=100+self.row, column=0, padx=5, pady=1)
            self.row+=1
            self.tracking = False
            #[print(x.__class__, x.__getattribute__('start'), x.__getattribute__('end')) for x in self.elements]
            for el in self.elements:
                for comp in self.elements:
                    if el!=comp and (el.start==comp.start or el.end==comp.end or el.end==comp.start or el.start==comp.end):
                        self.connections[el.canvasID].add(comp.canvasID)
            
        else:
            self.canvas.bind("<Motion>", lambda event, starting=selected: self.__follow(event, starting))
            self.prev = Wire(self.canvas, [0, 0], [0, 0])
            self.tracking = True 

    '''
    Follows the cursor during tracking
    # can be wire, generator or resistor
    '''
    def __follow(self, event, starting):
        try: 
            selected = self.select(event=event)
            self.elements.pop()
            self.prev.delete()
            if self.component=="wire":
                self.prev = Wire(self.canvas, starting, selected)
            elif self.component=="resistor":
                self.prev = Resistor(self.canvas, starting, selected)
            elif self.component=="generator":
                self.prev = Generator(self.canvas, starting, selected)
            self.elements.append(self.prev)
        except Exception: 
            # cursor goes out from canvas
            pass

    '''
    Studies electrical connection 
    '''
    def study(self):
        maglie = []
        branches = []
        nodes = []
        nodes_1d = set()
        startLink = defaultdict(list)
        endLink = defaultdict(list)

        searchNodes(self.connections, nodes, nodes_1d)
        searchBranches(self.connections, nodes, nodes_1d, branches)
        searchCycles(self.connections, nodes, nodes_1d, branches, maglie, startLink, endLink)

        # ricerca delle equazioni
        '''
        Per un circuito di n rami, le leggi di kirchhoff forniscono un
        sistema di n equazioni lineari tra loro indipendenti che contiene n incognite.
        '''
        '''sys = []
        for el in startLink:
            sys.append([])
            for branch in startLink[el]:
                for comp in maglie:
                    if branch in comp and comp not in sys:
                        sys[-1].append(comp)
                        break
        
        self.nodes = nodes_1d'''

        sys = []
        for m in maglie:
            if m[0] == maglie[12][0]:
                sys.append(m)

        

        for m in maglie:
            print(m)
        print('-'*200)
        for eq in sys:
            print(eq)
        print('-'*200)
        print(f"connections: {self.connections}")
        print(f"nodes: {nodes}")
        print(f"branches: {branches}")

    '''
    Deletes button function
    Call the delete method of the target 
    Deletes the tkinter button widget
    '''
    def __delete(self, button, target):
        target = re.findall(r"\d+", target)[0]
        button.destroy()
        for el in self.elements:
            if el.canvasID==int(target):
                self.elements.remove(el)
                el.delete()
                break
          
        self.connections.pop(int(target))
        for conn in self.connections:
            print(self.connections[conn])
            try:
                self.connections[conn].remove(int(target))
            except:
                pass
