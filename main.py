import customtkinter as ctk
from circuit import base
import os
import sys

def main():
    sys.setrecursionlimit(10000)
    print(f"pid: {os.getpid()}")

    root = ctk.CTk()
    root.title("Kirchhoff")

    circuit = base.BreadBoard(root)

    def newComponent(component: str, value: int = 5):
        circuit.component = component
        circuit.value = value

    def combobox_callback(choice):
        print("combobox dropdown clicked:", choice)

    genval = ctk.CTkEntry(root, placeholder_text='Corrente erogata')
    resval = ctk.CTkEntry(root, placeholder_text='Resistenza opposta')

    sideMenu = [
        ctk.CTkLabel(root, text="Aggiungi un nuovo componente", font=('Helvetica', 20)),
        ctk.CTkButton(root, text="Conduttore", corner_radius=4, font=('Helvetica', 16), command=lambda: newComponent('wire')),
        ctk.CTkButton(root, text="Generatore", corner_radius=4, font=('Helvetica', 16), command=lambda: newComponent('generator', genval.get())),
        genval,
        ctk.CTkButton(root, text="Resistore", corner_radius=4, font=('Helvetica', 16), command=lambda: newComponent('resistor', resval.get())),
        resval,
        
    ]

    ctrlPanel = [
        ctk.CTkLabel(root, text="Pannello di controllo", font=('Helvetica', 20)),
        ctk.CTkComboBox(master=root,
                        width=160,
                        font=('Helvetica', 15),
                        dropdown_font=('Helvetica', 15), 
                        values=[str(el) for el in circuit.nodes],
                        command=combobox_callback,
                        variable=ctk.StringVar(value="Corrente Entrante")),
        ctk.CTkComboBox(master=root,
                        width=160,
                        font=('Helvetica', 15),
                        dropdown_font=('Helvetica', 15), 
                        values=[str(el) for el in circuit.nodes],
                        command=combobox_callback,
                        variable=ctk.StringVar(value="Corrente Uscente")),
        ctk.CTkButton(root, width=175, text="Calcola", corner_radius=4, font=('Helvetica', 16), fg_color="green", command=circuit.study),
    ]

    # render side menu
    i=0
    for el in sideMenu:
        i+=1
        el.grid(row=i, column=0, padx=5, pady=1)

    # render canvas    
    circuit.canvas.grid(row=0, column=1, rowspan=200)

    # render control panel
    i = 0
    for el in ctrlPanel:
        i+=1
        el.grid(row=i, column=2, padx=8, pady=2)
    root.mainloop()

if __name__=="__main__":
    main()
