## Introduzione
La Meccanica Quantistica rappresenta una profonda rottura epistemologica e matematica rispetto alla fisica classica pre-novecentesca. Se la meccanica classica, fondata sulle leggi di Newton, possiede un carattere strettamente deterministico in cui la conoscenza delle posizioni e delle velocità iniziali permette di determinare con esattezza l'evoluzione futura del sistema la meccanica quantistica sostituisce tale paradigma con una descrizione intrinsecamente probabilistica. Le leggi quantistiche non prevedono il realizzarsi di eventi certi, ma unicamente le probabilità con cui essi possono occorrere, e tale caratteristica è intrinseca nel mondo fisico, smentendo l'esistenza di "variabili nascoste". Di seguito vengono formalizzati i postulati fondamentali che costituiscono l'impalcatura assiomatica della teoria.

## Postulato della Rappresentazione degli Stati (Spazio di Hilbert e Sovrapposizione)
Il primo postulato definisce la natura cinematica dei sistemi quantistici. In meccanica quantistica, lo stato di un sistema fisico è descritto in modo completo da un vettore in uno spazio vettoriale complesso (Spazio di Hilbert). 

Utilizzando la notazione introdotta da Dirac, lo stato di un sistema è rappresentato da un vettore detto **ket**, indicato con il simbolo $|\phi\rangle$. Ad ogni ket è associato un vettore duale detto **bra**, indicato con $\langle \phi|$, definito nello spazio vettoriale complesso coniugato, secondo la regola di corrispondenza lineare:
$$ c_\alpha|\alpha\rangle + c_\beta|\beta\rangle \longleftrightarrow c_\alpha^* \langle\alpha| + c_\beta^* \langle\beta| $$.

L'interpretazione probabilistica richiede che i vettori di stato corrispondenti a stati fisici reali siano rigorosamente normalizzati a uno:
$$ \langle \phi | \phi \rangle = 1 $$.

Un concetto cardine che discende da questa rappresentazione è il **principio di sovrapposizione degli stati**. Esso afferma che, dato un insieme di stati di base $|i\rangle$, ogni stato $|\phi\rangle$ può essere espresso come combinazione lineare (o sovrapposizione) di tali stati:
$$ |\phi\rangle = \sum_i c_i |i\rangle $$.
Fisicamente, questo indica che se un sistema può trovarsi in diversi stati accessibili, esso può esistere anche in una qualunque loro combinazione lineare complessa, una proprietà che genera fenomeni di interferenza senza alcun analogo classico. La probabilità in meccanica quantistica è infatti data dal modulo quadro di un numero complesso detto *ampiezza di probabilità* ($P = |\phi|^2$). Quando un evento può avvenire secondo alternative indistinguibili, si sommano le ampiezze e non le probabilità, generando l'interferenza: $P = |\phi_1 + \phi_2|^2$.

## Postulato delle Grandezze Fisiche (Osservabili e Operatori)
Il legame tra il formalismo astratto e la realtà empirica è dettato dal secondo postulato. Nella meccanica quantistica si associa ad ogni grandezza fisica (o osservabile) $A$ un operatore lineare $A$ che agisce sullo spazio dei vettori di stato.

Affinché i valori attesi di tali grandezze fisiche siano reali (come richiesto per quantità misurabili in laboratorio), si postula che **gli operatori che rappresentano le osservabili debbano essere operatori hermitiani**, ovvero operatori che coincidono con il proprio aggiunto hermitiano:
$$ A = A^+ $$.
La condizione di hermiticita garantisce che il valore di aspettazione $\langle A \rangle = \langle \phi | A | \phi \rangle$ sia un numero reale.

Gli autovettori di un operatore hermitiano, indicati con $|a'\rangle$, soddisfano l'equazione agli autovalori:
$$ A|a'\rangle = a'|a'\rangle $$.
Si postula che **la totalità degli autovalori $a'$ di un operatore $A$ sia identica alla totalità di tutti i possibili risultati ottenibili da una misura** della grandezza $A$ corrispondente. Autovettori associati ad autovalori distinti risultano inoltre essere rigorosamente ortogonali tra loro ($\langle a' | a'' \rangle = 0$) e formano una base completa per lo spazio degli stati.

## Postulato della Misura e del Collasso del Vettore di Stato
Se si esegue una misura dell'osservabile $A$ su un sistema descritto da uno stato generico $|\phi\rangle$, il risultato ottenuto sarà sempre uno degli autovalori $a'$ dell'operatore $A$. 

Esprimendo lo stato $|\phi\rangle$ come sviluppo nella base degli autostati di $A$, si ha:
$$ |\phi\rangle = \sum_{a'} c_{a'} |a'\rangle $$.
I coefficienti complessi $c_{a'}$ sono determinati dal prodotto scalare $c_{a'} = \langle a' | \phi \rangle$. Il modulo quadro di questa ampiezza di probabilità definisce l'esatta probabilità di misurare l'autovalore $a'$:
$$ P(a') = |c_{a'}|^2 = |\langle a' | \phi \rangle|^2 $$.

Un aspetto rivoluzionario della quantistica emerge immediatamente dopo la misurazione. Se la misura fornisce il valore $a'$, il processo di misura influisce irreversibilmente sul sistema: **il sistema precipita (o collassa) istantaneamente nell'autostato $|a'\rangle$** corrispondente all'autovalore misurato. Formalmente, questo processo di filtraggio è descritto dall'operatore di proiezione $\Lambda_{a'}$:
$$ \Lambda_{a'} = |a'\rangle\langle a'| $$.
Il valore medio (o valore di aspettazione) teorico di un gran numero di misurazioni identiche su sistemi preparati nello stato $|\phi\rangle$ è dato dalla somma pesata dei possibili risultati:
$$ \langle A \rangle = \sum_{a'} |c_{a'}|^2 a' $$.

## Postulato di Commutazione e Principio di Indeterminazione
Due grandezze fisiche $A$ e $B$ possono avere simultaneamente valori ben determinati se e solo se gli operatori ad esse associati commutano tra loro, ovvero se il loro commutatore è nullo:
$$ [A, B] = AB - BA = 0 $$.

Quando due operatori non commutano, essi corrispondono a grandezze incompatibili e obbediscono alla relazione di indeterminazione generalizzata:
$$ \langle(\Delta A)^2\rangle \langle(\Delta B)^2\rangle \ge \frac{1}{4} |\langle i [A, B] \rangle|^2 $$.
Questo teorema mostra che le dispersioni (scarti quadratici medi) di due osservabili non commutanti non possono essere simultaneamente nulle.

Questo concetto trova la sua forma più celebre nella formulazione del momento angolare e delle coordinate canoniche. Dirac postulò che la quantizzazione avviene sostituendo le parentesi di Poisson della meccanica classica con i commutatori della meccanica quantistica, secondo la regola:
$$ \{f, g\}_{classica} \rightarrow \frac{i}{\hbar} [f, g] $$.
Applicando tale regola alle variabili coniugate di posizione $x_i$ e impulso $p_j$, si ottengono le **relazioni di commutazione canoniche**:
$$ [x_i, p_j] = i\hbar \delta_{ij} \quad, \quad [x_i, x_j] = 0 \quad, \quad [p_i, p_j] = 0 $$.
Da ciò deriva rigorosamente il Principio di Indeterminazione di Heisenberg, il quale sancisce che posizione e impulso non possono avere traiettorie simultaneamente determinate:
$$ \Delta x \cdot \Delta p \ge \frac{\hbar}{2} $$.

## Postulato dell'Evoluzione Temporale (Equazione di Schrödinger)
A differenza del processo di misura che è discontinuo e probabilistico, l'evoluzione di uno stato quantistico isolato nel tempo è continua e strettamente deterministica. Lo stato al tempo $t$, indicato con $|\alpha, t\rangle$, è ricavato a partire dallo stato iniziale $|\alpha, t_0\rangle$ tramite un **operatore di evoluzione temporale unitario** $U(t, t_0)$:
$$ |\alpha, t\rangle = U(t, t_0)|\alpha, t_0\rangle \quad \text{con} \quad U^+(t, t_0)U(t, t_0) = 1 $$.

Poiché l'energia totale (l'Hamiltoniano $H$) è il generatore delle traslazioni temporali la dinamica del sistema è dettata dall'**Equazione di Schrödinger**:
$$ i\hbar \frac{\partial}{\partial t} |\alpha, t\rangle = H |\alpha, t\rangle $$.
Se il sistema è sottoposto ad un campo esterno definito da un potenziale spaziale $V(\vec{x})$, l'Hamiltoniano assume la forma $H = \frac{\vec{p}^2}{2m} + V(\vec{x})$. Proiettando l'equazione di Schrödinger nella rappresentazione delle coordinate, dove la funzione d'onda è $\psi(\vec{x}', t) = \langle\vec{x}'|\alpha, t\rangle$ e l'impulso è l'operatore differenziale $\vec{p} = -i\hbar\vec{\nabla}$ si ottiene l'equazione d'onda differenziale di Schrödinger:
$$ i\hbar \frac{\partial \psi}{\partial t} = -\frac{\hbar^2}{2m} \nabla'^2\psi + V(\vec{x}')\psi $$.

## Postulato di Symmetria per Particelle Identiche
Nella meccanica quantistica vige il principio di indistinguibilità assoluta delle particelle identiche. A causa di ciò, il vettore di stato complessivo di un sistema a molti corpi deve mostrare una simmetria definita sotto l'azione dell'operatore di scambio $P_{ij}$ (che inverte le coordinate e gli spin della particella $i$ con la particella $j$).
Applicando l'operatore di scambio, le uniche trasformazioni ammissibili sono un cambiamento di segno globale (autovalore -1) o la totale immutabilità (autovalore +1):
$$ P_{12}|\psi\rangle = \pm |\psi\rangle $$.

Tale principio genera la divisione di tutta la materia in due categorie :
1. **I Bosoni** (particelle a spin intero) le cui funzioni d'onda sono totalmente **simmetriche**: $P_{ij} |\psi_S\rangle = + |\psi_S\rangle$.
2. **I Fermioni** (particelle a spin semintero) le cui funzioni d'onda sono totalmente **antisimmetriche**: $P_{ij} |\psi_A\rangle = - |\psi_A\rangle$.

Questa antisimmetria per i fermioni comporta il **Principio di Pauli**: il vettore di stato antisimmetrico, rappresentabile tramite un determinante di Slater, si annulla identicamente qualora due o più fermioni tentino di occupare il medesimo stato quantistico simultaneamente. Questa proprietà cinematica, che si conserva invariantemente nel tempo essendo $[H, P_{ij}]=0$ non ha paritetiche espressioni nella fisica classica e definisce il comportamento dell'intera materia stabile dell'universo.