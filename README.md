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
  
Ereditano tutte il comportamento della prima e contengono quindi: un costruttore, un metodo draw (che le disegna nello spazio canvas), un metodo delete per l'eliminazione completa del componente.
Condividono inoltre l'impostazione delle variabili: self.start, self.end, self.circuit.

**Spiegazione dettagliata del codice**: *base.py*
=======================================================

Dal nome del file si intuisce che esso sta alla base di tutto. *base.py* si occupa di tutti gli algoritmi matematici che il software necessita. Consiste in una sola classe con 15 membri e 8 metodi molto complessi:
- il costruttore che determina i pin dello spazio di lavoro, ovvero i luoghi di aggancio dei componenti, e inizializza tutti i membri;
- il gruppo di metodi *select*, *draw*, *follow*, che collaborando gestiscono gli eventi del mouse (click e spostamento), sfruttano il modulo *components.py* per disegnare il circuito in base alle preferenze dell'utente, mostrano un'anteprima del componente disegnato prima della conferma dell'utente e modificano le variabili di classe affinchè gli altri metodi possano lavorare;
- il gruppo di metodi *nodes_update*, *study*, si occupano di aggiornare la ricerca dei nodi, dei rami e dei componenti in base alle definizioni date dalle leggi di Kirchhoff, studiano il circuito mediante decine di cicli for e while che impostano e risolvono sistemi matematici. Il lavoro dietro questo gruppo di metodi ha richiesto mesi e la stesura di complicati algoritmi che generalizzino le leggi fisiche alla base del calcolo dei circuiti.
- il gruppo di metodi *delete*, *delete_update*, utile all'eliminazione dei componenti quando richiesto dall'utente e anche alla pulizia di tutti i vettori e strutture dati dai componenti eliminati.

Infine il file *utils.py* contiene qualche funzione che serve a semplificare e ad evitare la ripetizione di pezzi di codice.
