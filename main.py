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

    genval = ctk.CTkEntry(root, placeholder_text='Corrente erogata')
    resval = ctk.CTkEntry(root, placeholder_text='Resistenza opposta')

    sideMenu = [
        ctk.CTkLabel(root, text="Aggiungi un nuovo componente", font=('Helvetica', 18)),
        ctk.CTkButton(root, text="Conduttore", corner_radius=4, font=('Helvetica', 16), command=lambda: newComponent('wire')),
        ctk.CTkButton(root, text="Generatore", corner_radius=4, font=('Helvetica', 16), command=lambda: newComponent('generator', genval.get())),
        genval,
        ctk.CTkButton(root, text="Resistore", corner_radius=4, font=('Helvetica', 16), command=lambda: newComponent('resistor', resval.get())),
        resval,
        ctk.CTkButton(root, text="Calcola", corner_radius=4, font=('Helvetica', 16), fg_color="green", command=circuit.study)
    ]

    i=0
    for el in sideMenu:
        i+=1
        el.grid(row=i, column=0, padx=5, pady=1)
    circuit.canvas.grid(row=0, column=1, rowspan=200)
    root.mainloop()

if __name__=="__main__":
    main()