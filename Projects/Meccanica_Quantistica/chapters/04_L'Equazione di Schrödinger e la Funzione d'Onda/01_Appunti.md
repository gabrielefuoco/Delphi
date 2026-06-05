L'impalcatura matematica della meccanica quantistica si fonda sulla descrizione dello stato di un sistema fisico attraverso vettori in uno spazio vettoriale complesso e sulla loro evoluzione temporale governata da operatori lineari. In questa trattazione, analizzeremo rigorosamente la genesi e la struttura dell'equazione di Schrödinger, partendo dai fondamenti degli operatori a spettro continuo fino a giungere alla formulazione della conservazione locale della probabilità.

### La Rappresentazione delle Coordinate e la Funzione d'Onda

In meccanica quantistica, le osservabili fisiche corrispondono ad operatori hermitiani. Un caso di fondamentale importanza è costituito dalle osservabili dotate di uno spettro continuo di autovalori, come l'operatore posizione. Considerando per semplicità una particella vincolata a muoversi in una dimensione lungo l'asse $x$, l'equazione agli autovalori per l'operatore posizione $x$ si scrive:
$$x |x'\rangle = x' |x'\rangle$$.
In questa formulazione, $x'$ è un numero reale che rappresenta l'autovalore, mentre $x$ è l'operatore. Un generico stato del sistema $|\alpha\rangle$ può essere sviluppato in integrale utilizzando il sistema completo degli autostati della posizione, la cui relazione di completezza è $\int_{-\infty}^{+\infty} dx' |x'\rangle\langle x'| = 1$. Lo sviluppo formale dello stato è il seguente:
$$|\alpha\rangle = \int_{-\infty}^{+\infty} dx' |x'\rangle \langle x'|\alpha\rangle$$.

Il prodotto scalare $\langle x'|\alpha\rangle$ assume un significato di primaria importanza e prende la denominazione di **funzione d'onda** $\psi_\alpha(x')$ associata allo stato $|\alpha\rangle$:
$$\psi_\alpha(x') = \langle x'|\alpha\rangle$$.
Dal punto di vista fisico, la grandezza $|\psi_\alpha(x')|^2 dx'$ rappresenta la probabilità che la particella, trovandosi nello stato $|\alpha\rangle$, venga localizzata in un intervallo spaziale infinitesimo di larghezza $dx'$ centrato nel punto $x'$. Pertanto, la distribuzione di probabilità spaziale è rigorosamente definita da:
$$P(x', x' + dx') = |\langle x'|\alpha\rangle|^2 dx' = |\psi_\alpha(x')|^2 dx'$$.
Da ciò discende la condizione di normalizzazione della funzione d'onda affinché la probabilità totale su tutto lo spazio sia pari all'unità:
$$\int_{-\infty}^{+\infty} dx' |\psi_\alpha(x')|^2 = 1$$.

### L'Evoluzione Temporale dei Vettori di Stato

Il determinismo della meccanica quantistica risiede nella stretta consequenzialità temporale del vettore di stato: noto il vettore di stato a un istante iniziale $t_0$, indicato con $|\alpha, t_0\rangle$, il suo comportamento a un qualsiasi istante successivo $t > t_0$ è univocamente definito dal vettore $|\alpha, t\rangle$. Tale evoluzione è descritta da un operatore lineare detto **operatore di evoluzione temporale** $U(t, t_0)$:
$$|\alpha, t\rangle = U(t, t_0)|\alpha, t_0\rangle$$.

La necessità di preservare la conservazione della probabilità totale nel tempo impone che la norma del vettore di stato resti invariata. Tale condizione si traduce nel vincolo di unitarietà per l'operatore $U(t, t_0)$:
$$U^\dagger(t, t_0)U(t, t_0) = 1$$.
L'evoluzione infinitesima del sistema è retta dal generatore delle traslazioni temporali, che la meccanica quantistica identifica con l'operatore Hamiltoniano $H$. L'equazione differenziale che descrive l'evoluzione dell'operatore $U$ è postulata come:
$$i\hbar \frac{\partial}{\partial t} U(t, t_0) = H U(t, t_0)$$.
Applicando ambo i membri di tale equazione differenziale al vettore di stato iniziale $|\alpha, t_0\rangle$, e sfruttando l'indipendenza di quest'ultimo dal tempo, si ottiene l'**equazione di Schrödinger per i vettori di stato**:
$$i\hbar \frac{\partial}{\partial t} |\alpha, t\rangle = H |\alpha, t\rangle$$.

### Derivazione dell'Equazione d'Onda di Schrödinger

L'equazione astratta per i vettori di stato assume la sua celebre forma differenziale quando viene proiettata nella base delle coordinate. Per un sistema descritto in tre dimensioni spaziali, la funzione d'onda dipendente dal tempo è la proiezione:
$$\psi(\vec{x}', t) = \langle \vec{x}'|\alpha, t\rangle$$.

Proiettando l'equazione di Schrödinger (eq. 114) sul bra $\langle \vec{x}'|$, si ottiene:
$$i\hbar \frac{\partial}{\partial t} \langle \vec{x}'|\alpha, t\rangle = \langle \vec{x}'|H|\alpha, t\rangle$$.
L'operatore Hamiltoniano per una particella di massa $m$ immersa in un campo di potenziale esterno $V(\vec{x})$ è l'analogo quantistico dell'Hamiltoniana classica:
$$H = \frac{\vec{p}^2}{2m} + V(\vec{x})$$.

Per valutare l'azione dell'energia cinetica, si ricorda che l'operatore impulso nella rappresentazione delle coordinate è identificato con $\vec{p} = -i\hbar \vec{\nabla}$. Di conseguenza, il termine cinetico diviene proporzionale all'operatore Laplaciano $\nabla'^2$:
$$\langle \vec{x}'| \frac{\vec{p}^2}{2m} |\alpha, t\rangle = \frac{1}{2m} (-i\hbar\nabla') \cdot \langle \vec{x}'|\vec{p}|\alpha, t\rangle = -\frac{\hbar^2}{2m} \nabla'^2 \psi(\vec{x}', t)$$.
Il termine relativo all'energia potenziale è puramente moltiplicativo:
$$\langle \vec{x}'|V(\vec{x})|\alpha, t\rangle = V(\vec{x}')\psi(\vec{x}', t)$$.

Sommando i contributi di energia cinetica e potenziale, perveniamo all'**equazione d'onda di Schrödinger dipendente dal tempo**:
$$i\hbar \frac{\partial \psi}{\partial t} = H\psi = -\frac{\hbar^2}{2m} \nabla'^2\psi + V(\vec{x}')\psi$$.

### Stati Stazionari ed Equazione Indipendente dal Tempo

Nei casi in cui il campo esterno e, di conseguenza, l'operatore Hamiltoniano $H$ non mostrano una dipendenza esplicita dal tempo, il sistema ammette stati con energia rigorosamente determinata. In tali contingenze, l'operatore di evoluzione temporale diviene una semplice fase complessa:
$$U(t, t_0) = e^{-\frac{i}{\hbar}H(t-t_0)}$$.
Gli stati con energia determinata prendono il nome di **stati stazionari** e corrispondono agli autovettori $|n\rangle$ dell'operatore $H$, governati dall'equazione agli autovalori:
$$H |n\rangle = E_n |n\rangle$$.

Per questi stati, l'evoluzione temporale si riduce al prodotto per un fattore di fase oscillante:
$$|n, t\rangle = e^{-\frac{i}{\hbar}E_nt} |n, 0\rangle$$.
Ne consegue che il valore di aspettazione di qualsiasi osservabile su uno stato stazionario rimane immutato nel tempo. Proiettando l'equazione agli autovalori nello spazio delle coordinate e definendo l'autofunzione $\psi_n(\vec{x}') = \langle \vec{x}'|n\rangle$ si deriva l'**equazione d'onda di Schrödinger indipendente dal tempo**:
$$H\psi_n = -\frac{\hbar^2}{2m} \nabla'^2\psi_n + V(\vec{x}')\psi_n = E_n \psi_n$$.

In virtù della linearità dell'equazione e del principio di sovrapposizione, la soluzione più generale dipendente dal tempo per un sistema con potenziale statico è una combinazione lineare di stati stazionari:
$$|\alpha, t=0\rangle = \sum_n c_n(0) |n\rangle$$ che evolve dinamicamente secondo la legge:
$$|\alpha, t\rangle = \sum_n c_n(0) e^{-\frac{i}{\hbar}E_n t} |n\rangle$$. I moduli quadri $|c_n|^2$, che rappresentano la probabilità di misurare l'energia $E_n$, restano costanti nel tempo a riprova della conservazione dell'energia.

### Proprietà Matematiche della Funzione d'Onda e Continuità

La funzione d'onda $\psi$, per ammettere un significato probabilistico rigoroso, deve ottemperare a specifiche richieste matematiche. Essa deve essere *monodroma* (a singolo valore) e *continua in tutto lo spazio*. Inoltre, le sue derivate prime devono preservare la continuità su ogni punto, ivi comprese le superfici ove il potenziale esibisce discontinuità finite; tale continuità della derivata prima decade solo qualora il potenziale diverga all'infinito ($V \to \infty$) su tali superfici. Classicamente ed anche quantisticamente, una particella non può penetrare regioni di potenziale infinito, e perciò la funzione d'onda ivi si annulla in maniera rigorosa ($\psi = 0$).

Esiste un nesso stringente tra la dinamica della funzione d'onda e la conservazione locale della probabilità. Definendo la densità di probabilità come:
$$\rho(\vec{x}, t) = |\psi(\vec{x}, t)|^2$$ è possibile computarne la derivata temporale:
$$\frac{\partial \rho}{\partial t} = \frac{\partial \psi^*}{\partial t} \psi + \psi^* \frac{\partial \psi}{\partial t}$$.

Sostituendo le derivate temporali facendo uso dell'equazione di Schrödinger e della sua complessa coniugata:
$$i\hbar \frac{\partial \psi}{\partial t} = -\frac{\hbar^2}{2m} \nabla^2\psi + V \psi \quad, \quad -i\hbar \frac{\partial \psi^*}{\partial t} = -\frac{\hbar^2}{2m} \nabla^2\psi^* + V \psi^*$$ i termini legati all'energia potenziale $V$ si elidono in maniera esatta, e si giunge a:
$$\frac{\partial \rho}{\partial t} = \frac{i\hbar}{2m} \left( \psi^* \nabla^2\psi - \psi \nabla^2\psi^* \right) = \frac{i\hbar}{2m} \vec{\nabla} \cdot \left( \psi^* \vec{\nabla}\psi - \psi \vec{\nabla}\psi^* \right)$$.

Definendo il vettore densità di corrente (o **densità di corrente di probabilità**):
$$\vec{j} = -\frac{i\hbar}{2m} \left( \psi^* \vec{\nabla}\psi - \psi \vec{\nabla}\psi^* \right) = \frac{\hbar}{m} \text{Im} \left( \psi^* \vec{\nabla}\psi \right)$$ il bilancio temporale della densità di probabilità si riassume nell'**equazione di continuità**:
$$\frac{\partial \rho}{\partial t} + \vec{\nabla} \cdot \vec{j} = 0$$.
Tale formulazione differenziale, del tutto analoga all'equazione classica della fluidodinamica, manifesta la conservazione locale del numero di particelle garantendo l'integrità formale e fisica dell'interpretazione probabilistica introdotta dai postulati della meccanica quantistica.