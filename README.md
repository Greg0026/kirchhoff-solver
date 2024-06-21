****************
# **Kirchhoff-Solver**
****************

**Spiegazione dettagliata del codice**: *main.py*
=================================================

Il file *main.py* è il motore principale dell'applicazione, all'interno di esso convergono tutti i moduli fondamentali all'esecuzione del programma. 
Oltre a ciò nel file sono presenti le istruzioni alla base di un'interfaccia dinamica, divisa sostanzialmente in tre:
- un menù laterale contenente dei bottoni, utili a selezionare il componente che si deve disegnare;
- uno spazio di lavoro "canvas", ovvero una zona di disegno collegata direttamante agli algoritmi di calcolo dove il circuito prende forma;
- un pannello di controllo, dove l'utente seleziona il verso delle correnti e decide se calcolare il circuito.

Tutta l'interfaccia è costruita sulla base della libreria/modulo tkinter, famosa per essere una delle più usate nello sviluppo software in Python. 
La sua popolarità non è certo dovuta alla sua facilità di utilizzo, ma un progetto open source chiamato customtkinter ha come scopo proprio quella di renderla semplice. 
È per questo motivo che nel codice si vede la scritta "import customtkinter" anzichè "import tkinter".

**Spiegazione dettagliata del codice**: *components.py*
=======================================================

*components.py* è il file che contiene tutte le istruzioni per il corretto disegno del grafico. 
Contiene 4 classi fondamentali:
- class Component(ABC), essa è una classe astratta (eredita il modulo ABC, abstract base class) utile a dare un'impostazione generale degli altri componenti;
- class Wire(Component);
- class Resistor(Component);
- class Generator(Component).
  
Ereditano tutte il comportamento della prima e contengono quindi: un costruttore, un funzione draw (che le disegna nello spazio canvas), una funzione delete per l'eliminazione.
Condividono inoltre l'impostazione delle variabili: self.start, self.end, self.circuit.
