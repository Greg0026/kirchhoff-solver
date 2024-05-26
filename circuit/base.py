from circuit.components import *
from circuit.utils import *
from collections import defaultdict
import numpy as np
import sympy as sp
from sympy import solve

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
        self.nodes_1d = set()
        self.corrent_in = []
        self.corrent_out = []
        self.connections = defaultdict(set)

        # click event listener
        self.canvas.bind("<Button-1>", lambda event, mode="TRACK": self.select(event, mode)) 

        # build breadboard
        '''for x in range(1, 50):
            self.canvas.create_text(x*30+20, 20, text=x, fill="black", font=('Fantasy 14 bold'))
            for y in range(1, 50):
                if y==1: 
                    self.canvas.create_text(20, x*30+20, text=x, fill="black", font=('Fantasy 14 bold'))
                self.canvas.create_aa_circle(y*30+20, x*30+20, 12, fill="darkgrey")'''
        '''self.elements = [
            Generator(self.canvas, [290, 260], [350, 260], 47),
            Generator(self.canvas, [290, 440], [350, 440], 40),
            Wire (self.canvas,[290, 260], [170, 260]),
            Wire (self.canvas,[170, 260], [170, 170]),
            Wire (self.canvas,[170, 170], [170, 80]),
            Wire (self.canvas, [170, 80], [320, 80]),
            Resistor(self.canvas,[320, 80],  [440, 80], 21),
            Wire (self.canvas, [440, 80], [770, 80]),
            Wire (self.canvas,[770, 80], [770, 170]),
            Wire (self.canvas,[770, 170], [770, 260]),
            Wire (self.canvas,[770, 260], [680, 260]),
            Wire (self.canvas,[680, 260], [680, 200]),
            Resistor (self.canvas,[680, 200], [560, 200], 12),
            Wire (self.canvas,[560, 200], [560, 260]),
            Wire (self.canvas,[560, 260], [560, 320]),
            Resistor (self.canvas,[560, 320], [680, 320], 35),
            Wire (self.canvas,[680, 320], [680, 260]),
            Wire (self.canvas,[560, 260], [350, 260]),
            Wire (self.canvas,[170, 170], [50, 170]),
            Wire (self.canvas,[50, 170], [50, 440]),
            Wire (self.canvas,[50, 440], [290, 440]),
            Wire (self.canvas,[350, 440], [500, 440]),
            Resistor (self.canvas,[500, 440], [620, 440], 57),
            Wire (self.canvas, [620, 440], [860, 440]),
            Wire (self.canvas,[860, 440], [860, 170]),
            Wire (self.canvas,[860, 170], [770, 170])
        ]
        for el in self.elements:
                for comp in self.elements:
                    if el!=comp and (el.start==comp.start or el.end==comp.end or el.end==comp.start or el.start==comp.end):
                        self.connections[el.canvasID].add(comp.canvasID)
        self.nodes_update()'''
        
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
                
    def __deleteUpdate(self):
        delete_box = ctk.CTkComboBox(master=self.root,
                        width=160,
                        font=('Helvetica', 15),
                        dropdown_font=('Helvetica', 15), 
                        values=[f"{el.component}: {el.canvasID}" for el in self.elements],
                        command=self.__delete,
                        variable=ctk.StringVar(value="Elimina")).grid(row=6, column=0, padx=5, pady=1)
    
    '''
    Draw a wire from point a to b
    '''
    def __draw(self, selected):
        if self.tracking:
            self.canvas.unbind("<Motion>")
            self.elements.append(self.prev)
            self.__deleteUpdate()
            self.tracking = False
            for el in self.elements:
                for comp in self.elements:
                    if el!=comp and (el.start==comp.start or el.end==comp.end or el.end==comp.start or el.start==comp.end):
                        self.connections[el.canvasID].add(comp.canvasID)
            
            self.nodes_update()
            
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
                self.prev = Resistor(self.canvas, starting, selected, self.value)
            elif self.component=="generator":
                self.prev = Generator(self.canvas, starting, selected, self.value)
            self.elements.append(self.prev)
        except Exception: 
            # cursor goes out from canvas
            pass

    def nodes_update(self):
        searchNodes(self.connections, self.nodes, self.nodes_1d)
        def corrent_in_callback(choice):
            self.corrent_in.append(int(choice))
        def corrent_out_callback(choice):
            self.corrent_out.append(int(choice))
        ctk.CTkComboBox(master=self.root,
                        width=160,
                        font=('Helvetica', 15),
                        dropdown_font=('Helvetica', 15), 
                        values=[str(el) for el in self.nodes_1d],
                        command=corrent_in_callback,
                        variable=ctk.StringVar(value="Corrente Entrante")).grid(row=2, column=2, padx=8, pady=2)
        
        ctk.CTkComboBox(master=self.root,
                        width=160,
                        font=('Helvetica', 15),
                        dropdown_font=('Helvetica', 15), 
                        values=[str(el) for el in self.nodes_1d],
                        command=corrent_out_callback,
                        variable=ctk.StringVar(value="Corrente Uscente")).grid(row=3, column=2, padx=8, pady=2)
    '''
    Studies electrical connection 
    '''
    def study(self):
        maglie = []
        branches = []
        startLink = defaultdict(list)
        endLink = defaultdict(list)

        searchBranches(self.connections, self.nodes, self.nodes_1d, branches)
        searchCycles(self.connections, self.nodes, self.nodes_1d, branches, maglie, startLink, endLink)

        # ricerca delle equazioni
        '''
        Per un circuito di n rami, le leggi di kirchhoff forniscono un
        sistema di n equazioni lineari tra loro indipendenti che contiene n incognite.
        '''
        sys = []
        for m in maglie:
            if m[0] == maglie[0][0]:
                for i in range(len(m)-1):
                    for j in range(i+1, len(m)-1):
                        if m[i]==m[j]:
                            m.remove(m[i])
                sys.append(m)

        eq_val = list(defaultdict(int))
        
        for eq in sys: 
            eq_val.append(defaultdict(int))
            for branch in eq:
                prev_pin = []
                for el in branch:
                    for comp in self.elements:
                        if el==comp.canvasID:
                            if comp.__class__==Resistor:
                                if branch[0] in self.corrent_out or branch[-1] in self.corrent_in:
                                    eq_val[-1]["i"+str(comp.canvasID)]+=(comp.value*-1)
                                else: eq_val[-1]["i"+str(comp.canvasID)]+=(comp.value)
                                break
                            if comp.__class__==Generator:
                                if comp.start in prev_pin:
                                    eq_val[-1]['generator']+=(comp.value)
                                else: eq_val[-1]['generator']+=(comp.value*-1)
                            prev_pin = [comp.start, comp.end]

            
        eq_ord = []
        for eq in eq_val:
            for el in eq:
                if el not in eq_ord and el!='generator':
                    eq_ord.append(el)
        
        left_matrix = []
        right_matrix = []

        for eq in eq_val:
            left_matrix.append([])
            for comp in eq_ord:
                if eq[comp]==0:
                    left_matrix[-1].append(0)
                else:
                    left_matrix[-1].append(eq[comp])
            right_matrix.append([eq['generator']])

        # corrent eq 
        for node in self.nodes:
            left_matrix.append([0]*len(eq_ord))
            right_matrix.append([0])
            for el in node:
                if el in self.corrent_in or el in self.corrent_out:
                    for branch in branches:
                        if el in branch:
                            for x in branch:
                                if 'i'+str(x) in eq_ord:
                                    if el in self.corrent_in:
                                        left_matrix[-1][eq_ord.index('i'+str(x))] = 1
                                    else: 
                                        left_matrix[-1][eq_ord.index('i'+str(x))] = -1
                else:
                    left_matrix.pop()
                    right_matrix.pop()
                    break
                    
        

        print(self.corrent_in, self.corrent_out)
        print(left_matrix)
        print(right_matrix)

        try:
            sol = np.linalg.solve(left_matrix, right_matrix)
        except:
            print("union")
            right_matrix.pop()
            for i in range(len(left_matrix[-2])):
                    left_matrix[-2][i] += left_matrix[-1][i]
            left_matrix.pop()
            sol = np.linalg.solve(left_matrix, right_matrix)
        finally:
            for i in range(len(sol)):
                ctk.CTkLabel(self.root, text=f"{eq_ord[i]} = {sol[i]}", font=("Helvetica", 18, "bold")).grid(row=5+i, column=2, padx=8, pady=2)
                    
        print('-'*200)
        print(eq_val)
        print('-'*200)
        for eq in sys:
            print(eq)
        print('-'*200)
        print(f"connections: {self.connections}")
        print(f"nodes: {self.nodes}")
        print(f"branches: {branches}")

    '''
    Deletes button function
    Call the delete method of the target 
    Deletes the tkinter button widget
    '''
    def __delete(self, choice):
        target = re.findall(r"\d+", choice)[0]
        for el in self.elements:
            if el.canvasID==int(target):
                self.elements.remove(el)
                el.delete()
                break
          
        self.connections.pop(int(target))
        for conn in self.connections:
            try:
                self.connections[conn].remove(int(target))
            except:
                pass

        self.__deleteUpdate()
