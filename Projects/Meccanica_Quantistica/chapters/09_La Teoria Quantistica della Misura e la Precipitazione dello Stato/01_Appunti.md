### La Crisi del Determinismo e le Ampiezze di Probabilità
La transizione dalla fisica classica alla meccanica quantistica segna il definitivo abbandono del determinismo intrinseco alle equazioni newtoniane. Se nella meccanica classica le leggi del moto permettono di calcolare con esattezza l'evoluzione futura di un sistema note le condizioni iniziali, le leggi quantistiche non possiedono un tale carattere deterministico. Nella meccanica quantistica, infatti, è impossibile prevedere in modo esatto gli eventi futuri; la teoria si limita a fornire le probabilità con cui i diversi eventi potranno occorrere. Questa natura probabilistica non deriva da una conoscenza incompleta del sistema (come postulato dalle teorie a "variabili nascoste", la cui assenza è sperimentalmente accertata), ma è una caratteristica intrinseca del mondo fisico microscopico.

Dal punto di vista del formalismo matematico, la probabilità $P$ di un evento in un esperimento ideale è quantificata dal quadrato del modulo di un numero complesso $\phi$, denominato *ampiezza di probabilità* :
$$P = |\phi|^2$$

Quando un processo quantistico può realizzarsi attraverso diverse alternative indistinguibili (ovvero senza che vi sia un'osservazione diretta del percorso), l'ampiezza di probabilità totale dell'evento è definita dalla sovrapposizione lineare delle singole ampiezze. Pertanto, introducendo due ampiezze $\phi_1$ e $\phi_2$, si manifesta il fenomeno dell'interferenza quantistica :
$$\phi = \phi_1 + \phi_2$$
$$P = |\phi_1 + \phi_2|^2$$

### Il Principio di Sovrapposizione e gli Operatori Lineari
Per formalizzare il concetto di ampiezza, la meccanica quantistica si avvale dell'algebra degli spazi vettoriali complessi, impiegando la notazione di Dirac (bra e ket). Ogni stato quantistico $|\phi\rangle$ può essere analizzato in termini di un insieme completo di stati di base $|i\rangle$. Il sistema è descritto da un'equazione di completezza che sancisce il fondamentale *Principio di Sovrapposizione* :
$$|\phi\rangle = \sum_i |i\rangle \langle i|\phi\rangle \equiv \sum_i c_i |i\rangle$$

La possibilità per un sistema microscopico di esistere in uno stato che è sovrapposizione lineare di più stati di base è un concetto puramente quantistico, privo di alcun analogo nella fisica classica. 

Ad ogni grandezza fisica osservabile $A$, la meccanica quantistica associa un operatore lineare hermitiano $A$ (tale che $A = A^+$). L'aspettazione matematica, o valore medio dei possibili risultati di una misura di $A$ su un sistema preparato nello stato $|\phi\rangle$, è dettato dalla relazione :
$$\langle A \rangle = \langle \phi | A | \phi \rangle$$

Gli autovalori $a_i$ dell'operatore $A$ costituiscono la totalità dei possibili risultati ottenibili in seguito a una misura della grandezza fisica. Se l'osservabile ha spettro discreto, lo stato arbitrario $|\phi\rangle$ può essere espanso in autostati $|a'\rangle$ dell'operatore $A$, i quali soddisfano l'equazione agli autovalori $A|a'\rangle = a'|a'\rangle$. Lo sviluppo si scrive come :
$$|\phi\rangle = \sum_{a'} c_{a'} |a'\rangle$$
dove i coefficienti dello sviluppo sono definiti dal prodotto scalare $c_{a'} = \langle a'|\phi\rangle$.

### L'Atto di Misura: Distruzione dell'Interferenza e Collasso dello Stato
Il nucleo matematico e concettuale di quella che storicamente è nota come Interpretazione di Copenaghen si palesa nel momento in cui l'osservatore compie un atto di misura sul sistema.

Se si esegue un esperimento in grado di determinare quale tra le possibili alternative si è effettivamente realizzata, il principio di sovrapposizione lineare delle ampiezze decade. In questo scenario, la probabilità totale dell'evento non è più il modulo quadro della somma delle ampiezze, ma la somma aritmetica delle probabilità individuali. Non si ha più interferenza :
$$P = P_1 + P_2$$

Questa fenomenologia trova rigorosa formulazione matematica nel postulato della misura. Utilizzando lo sviluppo di uno stato $|\phi\rangle$ normato ad $1$, la probabilità matematica di riscontrare esattamente l'autovalore $a'$ in seguito alla misurazione dell'osservabile $A$ coincide con il modulo quadro dell'ampiezza di transizione $c_{a'}$ :
$$P(a') = |c_{a'}|^2 = |\langle a'|\phi\rangle|^2$$

Ma cosa accade allo stato del sistema *immediatamente dopo* aver registrato il valore $a'$? La meccanica quantistica prescrive che l'atto di misura perturbi irreversibilmente il sistema. Se si ottiene il risultato $a'$, il sistema "precipita" (concetto equivalente al collasso della funzione d'onda) istantaneamente nel corrispondente autostato $|a'\rangle$. 

L'operazione matematica che descrive questo brusco cambiamento, detto anche processo di filtraggio è la proiezione dello stato iniziale. L'operatore responsabile di questa precipitazione dello stato è l'operatore di proiezione (o proiettore) :
$$\Lambda_{a'} = |a'\rangle\langle a'|$$

Facendo agire tale proiettore sul vettore di stato originario $|\phi\rangle$, si ottiene l'abbattimento della sovrapposizione su un singolo autostato :
$$\Lambda_{a'} |\phi\rangle = |a'\rangle\langle a'|\phi\rangle \equiv c_{a'} |a'\rangle$$
L'azione della misura distrugge la memoria quantistica del sistema: gli atomi che emergono da un apparato di misura sono situati nel nuovo autostato e non conservano alcun ricordo della loro storia precedente (matematicamente espresso dal fatto che l'operatore iterato non cambia l'informazione).

### Il Principio di Indeterminazione 
Un'ulteriore estensione concettuale legata indissolubilmente alla teoria quantistica della misurazione è la non-compatibilità di certe grandezze fisiche. Se due operatori $A$ e $B$ non commutano, ovvero se il loro commutatore è non nullo, essi rappresentano grandezze che non possono possedere simultaneamente valori esattamente determinati.
Per due operatori non commutanti, lo scarto quadratico medio (l'indeterminazione) è legato alla disuguaglianza :
$$\langle (\Delta A)^2 \rangle \langle (\Delta B)^2 \rangle \ge \frac{1}{4} \langle i[A,B] \rangle^2$$

L'esempio più celebre è fornito dalle variabili spaziali e coniugate di impulso, le cui regole di commutazione canoniche sono espresse da $[x_i, p_j] = i\hbar \delta_{ij}$. Da tale commutatore scaturisce il Principio di Indeterminazione di Heisenberg :
$$\Delta p \cdot \Delta x \ge \frac{\hbar}{2}$$
Questo principio impone un divieto fondamentale: è intrinsecamente impossibile assegnare contemporaneamente, a seguito di qualsivoglia misura ideale, una coordinata definita e un impulso definito a una particella quantistica. Qualsiasi misura atta a confinare la posizione (es. attraverso una fenditura spaziale di dimensione $a$, ponendo $\Delta x \approx a$) impone una severa perturbazione all'impulso, disperdendo le frange di interferenza e confermando il collasso locale della distribuzione delle probabilità. In termini rigorosi, una particella descritta da un'autofunzione esatta dell'impulso $p'$, la cui forma è $\psi_{p'}(x') = N e^{\frac{i}{\hbar}p' x'}$, ha una densità di probabilità costante in tutto lo spazio: $|\psi_{p'}(x)|^2 = |N|^2$, manifestando un'indeterminazione totale sulla propria posizione.