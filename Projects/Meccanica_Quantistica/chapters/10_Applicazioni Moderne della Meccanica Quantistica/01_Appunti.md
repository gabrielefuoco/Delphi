Sebbene il testo fornito non tratti esplicitamente lo sviluppo storico o l'ingegneria del computer quantistico e del laser, esso delinea in modo rigoroso ed esaustivo l'intera impalcatura matematica, i postulati e le equazioni differenziali che costituiscono le fondamenta teoriche di queste tecnologie moderne. Di seguito è redatto un capitolo accademico formale e dettagliato che estrae ed elabora i principi fisici e matematici alla base di tali applicazioni.

***



#### Il Qubit e il Formalismo dello Spin 1/2
Alla base dell'informazione quantistica (e della realizzazione del *quantum computer*) vi è il concetto di sistema a due livelli, o qubit. Nel formalismo della meccanica quantistica, il sistema fisico prototipico per descrivere un qubit è una **particella di spin $1/2$**, le cui proprietà si manifestano in esperimenti ideali di tipo Stern-Gerlach.

Gli autovalori del quadrato dello spin, $S^2$, per tali particelle sono pari a $\hbar^2 s(s+1)$, e la proiezione lungo l'asse $z$ dello spin, $S_z$, può assumere unicamente due valori quantizzati: $\pm \hbar/2$. Questi due autostati, che nell'informatica quantistica vengono tipicamente denotati come $|0\rangle$ e $|1\rangle$, sono qui rigorosamente definiti dai vettori di stato:
$|+\rangle \longleftrightarrow S_z = +\hbar/2 \quad, \quad |-\rangle \longleftrightarrow S_z = -\hbar/2$.

Questi vettori costituiscono una base ortonormale, obbedendo alla relazione:
$\langle + | + \rangle = \langle - | - \rangle = 1, \quad \langle + | - \rangle = \langle - | + \rangle = 0$.
In virtù del **principio di sovrapposizione**, uno dei pilastri fondamentali della meccanica quantistica il vettore di stato generico $|\phi\rangle$ di questo sistema a due livelli si esprime come una combinazione lineare complessa:
$|\phi\rangle = c_+ |+\rangle + c_- |-\rangle$.
La condizione di normalizzazione per tale stato (analoga alla conservazione della probabilità per un qubit) è espressa rigorosamente da:
$|c_+|^2 + |c_-|^2 = 1$.

L'azione su questi stati è mediata da **operatori hermitiani**, essenziali per descrivere le trasformazioni e le porte logiche quantistiche. La rappresentazione matriciale delle componenti dello spin fa uso delle **matrici di Pauli**, definite come:
$S_x = \frac{\hbar}{2} \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad S_y = \frac{\hbar}{2} \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad S_z = \frac{\hbar}{2} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$.
Tali operatori soddisfano le regole di commutazione fondamentali dell'algebra di Lie associate alle rotazioni:
$[S_i, S_j] = i\hbar \epsilon_{ijk} S_k$.

#### Evoluzione Temporale e Porte Logiche Quantistiche
In un computer quantistico, le computazioni avvengono tramite l'evoluzione temporale controllata degli stati dei qubit. Tale dinamica è governata dall'**equazione di Schrödinger dipendente dal tempo**:
$i\hbar \frac{\partial}{\partial t} |\alpha, t\rangle = H |\alpha, t\rangle$.
Se l'Hamiltoniano $H$ del sistema non dipende esplicitamente dal tempo, l'evoluzione dello stato da un istante $t_0$ a un istante $t$ è determinata dall'applicazione di un **operatore unitario di evoluzione temporale** $U(t, t_0)$:
$|\alpha, t\rangle = e^{-\frac{i}{\hbar}H(t-t_0)} |\alpha, t_0\rangle$.
In tale operatore, le trasformazioni unitarie preservano la norma del vettore di stato e sono matematicamente equivalenti all'azione continua delle porte logiche (*quantum gates*) sui registri di qubit.

#### Il Problema della Misura nel Calcolo Quantistico
Il collasso della funzione d'onda e l'estrazione di informazione da un computer quantistico sono modellizzati dalla teoria quantistica della misura. Ad ogni grandezza fisica osservabile è associato un **operatore hermitiano** $A = A^+$. 

Il valore di aspettazione dei risultati di una misura di $A$ su uno stato $|\phi\rangle$ è dato da:
$\langle A \rangle = \sum_i a_i P_i = \langle \phi | A | \phi \rangle$.
Un processo di misura che forza il sistema ad assumere un unico stato base ben definito (ad esempio, a seguito della lettura del qubit) è descritto da un **operatore di proiezione** (o misura selettiva) della forma:
$\Lambda_{a'} = |a'\rangle\langle a'|$.
L'azione di tale operatore distrugge irreversibilmente le sovrapposizioni precedenti, causando la perdita di informazione relativa alla storia passata del sistema, come illustrato dalle catene di filtraggio negli apparati ideali di Stern-Gerlach. Le osservabili fisiche misurabili simultaneamente senza distruggere i reciproci stati devono commutare, ossia $[A, B] = 0$; in caso contrario, obbediscono alla relazione di indeterminazione generalizzata $\langle(\Delta A)^2\rangle\langle(\Delta B)^2\rangle \geq \frac{1}{4} \langle i[A,B] \rangle^2$.

#### Interazione Radiazione-Materia e l'Emissione Stimolata (Basi del Laser)
Mentre il computer quantistico si basa sugli stati di spin e sull'entanglement, il **Laser** (Light Amplification by Stimulated Emission of Radiation) trae il suo fondamento teorico dalle transizioni energetiche degli atomi e dall'**emissione stimolata**, studiata tramite la **teoria delle perturbazioni dipendenti dal tempo**.

L'evoluzione dei coefficienti $c_k(t)$ di uno stato atomico sottoposto ad un campo perturbativo esterno $V(t)$ (come un'onda elettromagnetica incidente) è definita dal sistema esatto:
$i\hbar \frac{dc_k}{dt} e^{-\frac{i}{\hbar}E_k^{(0)}t} = \sum_m V_{km} c_m e^{-\frac{i}{\hbar}E_m^{(0)}t}$.
Affinando il calcolo mediante la regola d'oro di Fermi, la probabilità di transizione per unità di tempo tra uno stato iniziale $i$ e uno stato finale $n$ nello spettro continuo è:
$W_{i\to n} = \frac{2\pi}{\hbar} |V_{ni}|^2 \delta(E_n^{(0)} - E_i^{(0)})$.

Il nucleo matematico dell'effetto Laser risiede nell'analisi del termine di interazione che modula le frequenze di oscillazione. Quando l'atomo perturbato decade a un livello energetico inferiore ($E_n^{(0)} < E_i^{(0)}$) cedendo al campo elettromagnetico esterno un "quanto" di energia pari a $\hbar\omega$, avviene quello che la teoria quantistica definisce in modo esplicito come **processo di emissione stimolata**. Il campo perturbativo agisce come un "pozzo inesauribile di energia" (o sorgente), forzando coerentemente le transizioni necessarie all'amplificazione della luce.

#### Coerenza e Indistinguibilità: I Bosoni
Affinché i fotoni emessi nel processo descritto sopra creino un fascio Laser coerente, subentra un altro principio puramente quantistico non avente alcun analogo classico: l'**indistinguibilità totale delle particelle identiche**. 

In presenza di più particelle della stessa specie, la degenerazione di scambio impone l'utilizzo dell'**operatore di scambio** $P_{ij}$, il cui effetto sul vettore di stato è:
$P_{ij} |\psi\rangle = \pm |\psi\rangle$.
Nel caso specifico della radiazione elettromagnetica (fotoni), le particelle possiedono spin intero e sono identificate come **bosoni**. Essi sono descritti da vettori di stato rigorosamente **simmetrici** :
$P_{ij} |N_{\text{bosoni identici}}\rangle = + |N_{\text{bosoni identici}}\rangle$.
Questa simmetria, nota anche come obbedienza alla statistica di Bose-Einstein consente a un numero macroscopico di fotoni di condensare nel medesimo stato quantistico, generando il fascio di radiazione altamente collimato, monocromatico e coerente che caratterizza intrinsecamente un Laser. Qualora si trattasse di fermioni (particelle a spin semintero descritte da stati antisimmetrici), l'accumulo nello stesso stato sarebbe proibito dal principio di esclusione.