### Introduzione Concettuale e Crisi del Determinismo
La meccanica quantistica descrive fenomeni microscopici che divergono in modo radicale dall'esperienza della fisica classica. Una delle deviazioni più profonde consiste nell'abbandono del determinismo classico: la meccanica quantistica non è in grado di prevedere con esattezza gli eventi futuri di un sistema, ma unicamente la probabilità con cui essi si verificheranno. Tale peculiarità non deriva da un'incompleta conoscenza dello stato fisico, bensì da una caratteristica intrinseca e fondamentale della natura; è stato infatti sperimentalmente accertato che non esistono "variabili nascoste".

In questo contesto teorico, il concetto classico di "traiettoria" di una particella perde di significato. Questa constatazione trova la sua più celebre espressione matematica nel principio di indeterminazione, formulato originariamente da Werner Heisenberg nel 1927. Secondo tale principio, grandezze fisiche come la coordinata spaziale e l'impulso di un elettrone non possono possedere simultaneamente valori esattamente determinati. Se, in seguito ad una misura, viene assegnata ad una particella una posizione determinata nello spazio, essa non possiederà alcuna velocità determinata, e viceversa. 

È cruciale sottolineare che il principio di indeterminazione esprime un limite intrinseco dei sistemi fisici, totalmente slegato dall'accuratezza strumentale: sebbene ogni singola misurazione possa in linea di principio essere eseguita con accuratezza arbitraria, la determinazione precisa di una grandezza modificherà irrevocabilmente lo stato del sistema in relazione alla sua grandezza coniugata.

### Osservabili, Valori Medi e Dispersione
Per quantificare rigorosamente il principio di indeterminazione, è necessario introdurre la teoria quantistica della misura. In meccanica quantistica, ad ogni grandezza fisica $A$ è associato un operatore lineare hermitiano, $A = A^+$. Se un sistema si trova in un determinato stato iniziale $|\phi\rangle$, il valore medio (o di aspettazione) dei possibili risultati di una misura dell'osservabile $A$ è dato dalla relazione:
$$ \langle A \rangle = \langle \phi | A | \phi \rangle = \sum_i a_i P_i $$
dove $a_i$ sono i possibili risultati della misura (autovalori dell'operatore) e $P_i$ le rispettive probabilità.

Per determinare quanto i risultati di una misura si discostino dal valore medio, si introduce il concetto di dispersione o scarto quadratico medio, definito come:
$$ \langle (\Delta A)^2 \rangle \equiv \langle (A - \langle A \rangle)^2 \rangle $$
dove si è posto per convenzione $\Delta A \equiv A - \langle A \rangle$. 
Se il sistema si trova in uno stato che è autovettore dell'operatore $A$ (indicato con $|a'\rangle$), il valore dell'osservabile è determinato con certezza, e di conseguenza lo scarto quadratico medio si annulla rigorosamente: $\langle (\Delta A)^2 \rangle = 0$.

### Osservabili Incompatibili e la Relazione Generalizzata di Indeterminazione
Per far sì che due osservabili distinte $A$ e $B$ possiedano simultaneamente valori ben determinati (ossia $\langle (\Delta A)^2 \rangle = \langle (\Delta B)^2 \rangle = 0$), lo stato del sistema deve essere un autostato comune di entrambi gli operatori. Ciò è possibile se e solo se i due operatori commutano, ovvero se il loro commutatore è nullo:
$$ [A, B] = 0 $$
In questo caso, le osservabili si dicono *compatibili*. Al contrario, se gli operatori non commutano ($[A, B] \neq 0$), le grandezze fisiche associate prendono il nome di osservabili *incompatibili* e non possono essere determinate simultaneamente.

La limitazione nella misurazione simultanea di osservabili incompatibili è codificata matematicamente dalla **relazione di indeterminazione generalizzata**, che stabilisce la seguente disuguaglianza valida per un qualsiasi stato del sistema:
$$ \langle (\Delta A)^2 \rangle \langle (\Delta B)^2 \rangle \ge \frac{1}{4} \langle i [A, B] \rangle^2 $$
Ciò significa che il prodotto delle dispersioni di due osservabili non commutanti è limitato inferiormente dal valore medio del loro commutatore.

#### Dimostrazione della Relazione Generalizzata
La dimostrazione di tale disuguaglianza fondamentale poggia sulle proprietà formali degli spazi vettoriali complessi. Si considerino gli operatori hermitiani $R = \Delta A$ e $S = \Delta B$. Si introduca inoltre una costante reale $\lambda$ e si definisca uno stato ausiliario $|\phi\rangle$ costruito a partire da un generico stato arbitrario $|\alpha\rangle$:
$$ |\phi\rangle = (R + i\lambda S) |\alpha\rangle $$
L'ampiezza di probabilità $\langle \phi | \phi \rangle$ è, per costruzione di uno spazio di Hilbert, una quantità reale positiva o nulla. Sviluppando il prodotto scalare si ottiene:
$$ \langle \phi | \phi \rangle = \langle \alpha | (R - i\lambda S)(R + i\lambda S) | \alpha \rangle = \langle \alpha | R^2 | \alpha \rangle + i\lambda \langle \alpha | RS | \alpha \rangle - i\lambda \langle \alpha | SR | \alpha \rangle + \lambda^2 \langle \alpha | S^2 | \alpha \rangle \ge 0 $$
Semplificando e passando ai valori medi, emerge la condizione:
$$ \langle R^2 \rangle + \lambda \langle i[R, S] \rangle + \lambda^2 \langle S^2 \rangle \ge 0 $$
Il commutatore $[R, S]$ è un operatore antihermitiano, di conseguenza l'operatore $i[R,S]$ è hermitiano e il suo valore di aspettazione $\langle i[R, S] \rangle$ è puramente reale. Poiché la disuguaglianza precedente costituisce un'equazione di secondo grado in $\lambda$ che deve essere sempre positiva o nulla per ogni valore reale del parametro, il suo discriminante $\Delta$ non può essere positivo:
$$ \Delta = \langle i[R, S] \rangle^2 - 4\langle R^2 \rangle \langle S^2 \rangle \le 0 $$
Da cui scaturisce direttamente il risultato:
$$ \langle R^2 \rangle \langle S^2 \rangle \ge \frac{1}{4} \langle i[R, S] \rangle^2 $$
Sostituendo nuovamente $R = \Delta A$ e $S = \Delta B$, si ottiene l'espressione formale della relazione di indeterminazione.

### Il Principio di Indeterminazione tra Posizione e Impulso
L'applicazione più celebre della relazione appena derivata riguarda le variabili coniugate canoniche: la coordinata spaziale e l'impulso. In meccanica quantistica, l'impulso $\vec{p}$ gioca il ruolo di generatore delle traslazioni spaziali. Analizzando l'operatore di traslazione spaziale infinitesima $T(d\vec{x}') = 1 - \frac{i}{\hbar}\vec{p}\cdot d\vec{x}'$ e la sua commutazione con l'operatore di posizione vettoriale $\vec{x}$, si derivano le relazioni di commutazione canoniche di base :
$$ [x_i, p_j] = i\hbar \delta_{ij} $$
$$ [x_i, x_j] = 0 \quad, \quad [p_i, p_j] = 0 $$
La relazione $[x, p_x] = i\hbar$ inserita nella disuguaglianza generalizzata (con $A=x$ e $B=p_x$) produce l'espressione analitica originaria formulata da Heisenberg :
$$ \Delta x \cdot \Delta p_x \ge \frac{\hbar}{2} $$
dove $\Delta x \equiv \sqrt{\langle (\Delta x)^2 \rangle}$ e $\Delta p_x \equiv \sqrt{\langle (\Delta p_x)^2 \rangle}$.

#### Limiti estremi: L'onda Piana e il Pacchetto Gaussiano
Il dualismo introdotto dal principio di indeterminazione emerge in modo cristallino in due contesti fondamentali:
* **Particella Libera (Onda Piana):** Se una particella ha un impulso esattamente determinato pari a $\vec{p'}$, la sua funzione d'onda è un'onda piana del tipo $\psi_{p'}(x') = N e^{\frac{i}{\hbar}p'x'}$. Calcolando la densità di probabilità spaziale si ottiene $P(x, x+dx) = |\psi_{p'}(x)|^2 dx = |N|^2 dx$, ovvero una costante. Fisicamente, l'assenza totale di incertezza sull'impulso ($\Delta p = 0$) conduce a una totale e assoluta indeterminazione della posizione spaziale della particella.
* **Pacchetto d'Onda Gaussiano (Indeterminazione Minima):** È possibile costruire pacchetti d'onda la cui forma massimizza l'informazione simultanea su posizione e impulso, raggiungendo il limite inferiore del principio di indeterminazione. Per un pacchetto d'onda avente distribuzione spaziale gaussiana, le dispersioni assumono i valori $\langle (\Delta x)^2 \rangle = \sigma^2$ e $\langle (\Delta p)^2 \rangle = \frac{\hbar^2}{4\sigma^2}$. Il loro prodotto produce esattamente il limite teorico fondamentale: $\Delta x \cdot \Delta p = \frac{\hbar}{2}$.

### Applicazione Esplicita: L'Indeterminazione sui Sistemi di Spin
Il principio generalizzato manifesta i suoi effetti anche per osservabili che non possiedono analogo classico, come lo spin delle particelle. Il momento angolare intrinseco o spin, descritto dagli operatori $S_x, S_y, S_z$, soddisfa le relazioni di commutazione cicliche tipiche del momento angolare :
$$ [S_i, S_j] = i\hbar \varepsilon_{ijk} S_k $$
Ciò rende manifestamente incompatibili le componenti dello spin lungo assi cartesiani differenti. Scegliendo ad esempio $S_x$ e $S_y$, la relazione di indeterminazione associata impone :
$$ \langle (\Delta S_x)^2 \rangle \langle (\Delta S_y)^2 \rangle \ge \frac{1}{4} \langle i [S_x, S_y] \rangle^2 = \frac{\hbar^2}{4} \langle S_z \rangle^2 $$

Come esempio concreto per una particella di spin 1/2, consideriamo che essa si trovi nell'autostato $|+z\rangle$ (che indica che la misurazione di $S_z$ produrrebbe l'autovalore $+\hbar/2$ con certezza). Tramite le matrici di Pauli, si verifica che il valore medio della componente $x$ e il suo quadrato sono rispettivamente:
$$ \langle S_x \rangle = \langle +z | S_x | +z \rangle = 0 \quad, \quad \langle S_x^2 \rangle = \langle +z | S_x^2 | +z \rangle = \frac{\hbar^2}{4} $$
In modo identico si ottiene per la componente $y$: $\langle S_y \rangle = 0$ e $\langle S_y^2 \rangle = \frac{\hbar^2}{4}$. Le dispersioni assumeranno dunque i valori $\langle (\Delta S_x)^2 \rangle = \hbar^2/4$ e $\langle (\Delta S_y)^2 \rangle = \hbar^2/4$.
Il valore quadratico atteso per il membro destro della disuguaglianza è $\langle S_z \rangle^2 = (\langle +z | S_z | +z \rangle)^2 = \hbar^2/4$. Riunendo i termini si ottiene:
$$ \left( \frac{\hbar^2}{4} \right)^2 \ge \frac{\hbar^2}{4} \left( \frac{\hbar^2}{4} \right) $$
In questo peculiare stato, l'indeterminazione del sistema assume l'esatto valore di uguaglianza, minimizzando perciò la perdita di informazione compatibilmente col vincolo quantistico per osservabili non commutanti.

### Relazione Tempo-Energia
A corollario dei principi menzionati, vi è un'ulteriore forma della disuguaglianza, fondamentale all'interno della teoria delle perturbazioni dipendente dal tempo. Sebbene il tempo $t$ in meccanica quantistica sia trattato solitamente come un parametro, vige la cosiddetta *relazione di indeterminazione tempo-energia* :
$$ \Delta E \cdot \Delta t \sim \hbar $$
Questa equazione dichiara che per una perturbazione debole agita su un intervallo di tempo limitato $\Delta t$, si può produrre e misurare una variazione apprezzabile dell'energia propria del sistema $\Delta E$ pari all'incirca a $\hbar / \Delta t$. 
È fondativo specificare che questa disuguaglianza non ha lo stesso significato ontologico della relazione posizione-impulso: non si tratta dell'indeterminazione nella conoscenza simultanea di due variabili intrinseche allo stesso istante, bensì esprime il limite in cui la conservazione dell'energia si preserva nell'evoluzione dinamica e durante il processo di misurazione di un sistema su una finestra temporale $\Delta t$.

### L'Esperimento delle due fenditure e la distruzione dell'Interferenza
Il meccanismo con il quale il principio di indeterminazione protegge la logica interna del formalismo quantistico diviene palese in celebri esperimenti ideali, come ampiamente discusso nel dibattito tra Einstein e Bohr al Congresso Solvay nel 1927. Si consideri un apparato a doppia fenditura investito da un fascio di elettroni. Finché non è noto attraverso quale fenditura transiti la particella, le probabilità si sommano tramite il modulo quadro delle ampiezze di probabilità: $P_{12} = |\phi_1 + \phi_2|^2$, ed emerge l'interferenza tipica delle onde. 

Volendo inserire una strumentazione atta a determinare da quale foro passi l'elettrone, la fisica impone di localizzare l'elettrone limitando un'apertura dimensionale o un impulso scambiato con la parete. Misurare l'impulso trasversale ricevuto dallo schermo implica conoscerlo con una precisione maggiore di $\Delta p$. In base all'equazione di Heisenberg, l'indeterminazione sulla posizione dello schermo contenente la fenditura diviene :
$$ \Delta x \approx \frac{\hbar}{\Delta p} \approx \frac{\lambda D}{a} $$
dove $\lambda$ è la lunghezza d'onda di De Broglie dell'elettrone, $a$ è la separazione fra le due fenditure e $D$ la distanza dallo schermo di proiezione. Sorprendentemente, tale imprecisione imposta intrinsecamente dal principio di indeterminazione coincide in maniera esatta con la distanza spaziale fra i massimi d'interferenza: $\Delta x = \lambda D / a$. Tale deviazione statistica assicura matematicamente che l'aver osservato la traiettoria porta le frange a "sbiadirsi" sovrapponendosi in maniera incorrelata, sancendo irrevocabilmente la totale scomparsa della figura di interferenza ($P = P_1 + P_2$) e salvaguardando la coerenza causale della teoria quantistica.