### La Crisi della Fisica Classica e le Origini del Concetto di Quanto
La genesi della formulazione del dualismo onda-particella affonda le sue radici nell'incapacità della meccanica e dell'elettrodinamica classica di descrivere i fenomeni microscopici. L'elettrodinamica di Maxwell, descrivendo la luce come un'onda elettromagnetica, falliva nel giustificare la distribuzione spettrale dell'energia emessa da un corpo nero. La formula classica di Rayleigh-Jeans, $u(\omega, T) = \frac{\omega^2}{\pi^2c^3} KT$, prevedeva un'energia totale irraggiata infinita, nota come "catastrofe ultravioletta". 

La risoluzione di tale discrepanza fu ottenuta nel 1900 da Max Planck, il quale postulò che l'energia dei modi normali di oscillazione del campo elettromagnetico non variasse con continuità, ma fosse un multiplo intero di un "quanto" elementare di energia. L'energia di un singolo quanto, o fotone, è proporzionale alla frequenza $\omega$ della radiazione secondo la relazione fondamentale:
$$ \varepsilon = \hbar\omega $$
dove $\hbar = 1.054 \cdot 10^{-27} \text{ erg} \cdot \text{s}$ è la costante di Planck ridotta. I livelli energetici consentiti assumono dunque la forma discreta $E_n = n\hbar\omega$, con $n = 0, 1, 2...$. Questo segnò la prima introduzione di una natura corpuscolare (quantizzata) per la radiazione elettromagnetica.

### Evidenze della Natura Corpuscolare della Luce: Effetto Fotoelettrico e Compton
La duplice natura della radiazione fu formalizzata analizzando l'interazione luce-materia. Einstein (1905) spiegò l'effetto fotoelettrico ipotizzando che la luce fosse composta da particelle (fotoni), la cui energia obbedisce al principio di conservazione durante l'urto con un elettrone metallico:
$$ E_{el} = \frac{1}{2}mv^2 = \hbar\omega - W $$
dove $W$ è la funzione lavoro necessaria per estrarre l'elettrone. 

La conferma definitiva della natura corpuscolare giunse con l'Effetto Compton (1922). Considerando la radiazione come un gas di fotoni, a ciascun fotone si associa un quadrivettore energia-impulso $q = \left( \frac{\hbar\omega}{c}, \hbar\vec{k} \right)$ con norma quadra nulla ($q^2 = 0$). Nell'urto elastico tra un fotone incidente e un elettrone bersaglio a riposo, avente quadrimpulso $p = (mc, \vec{0})$, la conservazione del quadrimpulso $p + q = p' + q'$ conduce, dal punto di vista cinematico, alla relazione:
$$ p'^2 = m^2c^2 = (p + q - q')^2 = m^2c^2 + 2m\hbar\omega - 2m\hbar\omega' - \frac{2\hbar^2\omega\omega'}{c^2} + 2\hbar^2 \vec{k}\cdot\vec{k}' \cos\theta $$
Semplificando e introducendo la lunghezza d'onda $\lambda = \frac{2\pi c}{\omega}$, si ottiene la formula dello spostamento Compton:
$$ \lambda' - \lambda = \frac{h}{mc}(1 - \cos\theta) $$
dove la quantità $\lambda_C \equiv \frac{h}{mc} \simeq 2.4 \cdot 10^{-10} \text{ cm}$ è la lunghezza d'onda Compton dell'elettrone. La luce dimostra di possedere un impulso ben definito, comportamento tipico della materia corpuscolare.

### L'Ipotesi di De Broglie: Le Onde di Materia
Se la radiazione elettromagnetica presenta proprietà corpuscolari pur essendo descritta classicamente da un'equazione d'onda, Louis De Broglie, nel 1923, postulò un'audace simmetria insita in natura: la natura duale deve applicarsi anche alla materia. 
Dalla cinematica del fotone si ricava la relazione tra il suo impulso $p$ e il modulo del suo vettore d'onda $k$:
$$ p = \hbar k = \frac{2\pi\hbar}{\lambda} = \frac{h}{\lambda} $$
De Broglie ipotizzò che questa medesima equazione descrivesse le particelle massive. Una particella materiale di massa $m$ in moto con velocità $v$ e impulso $p = mv$ si comporta, in specifiche condizioni, come un'onda materiale caratterizzata da una lunghezza d'onda:
$$ \lambda = \frac{h}{p} $$
Questa è la celebre relazione di De Broglie. La natura ondulatoria degli elettroni venne sperimentalmente confermata nel 1927 da Davisson e Germer tramite la diffrazione elettronica su un reticolo cristallino, dove i massimi di interferenza rispondevano all'equazione di Bragg $2a \sin\theta = n\lambda$.

L'ipotesi di De Broglie fornì inoltre la giustificazione teorica del modello atomico di Bohr (1913). Bohr aveva postulato *ad hoc* che il momento angolare dell'elettrone fosse quantizzato secondo la regola $L = mvr = n\hbar$. Introducendo la relazione di De Broglie $\lambda = h/p$, la condizione di Bohr si riscrive in modo illuminante:
$$ L = pr = \frac{h}{\lambda}r = n\frac{h}{2\pi} \implies 2\pi r = n\lambda $$
Questa equazione dimostra che le orbite consentite per l'elettrone sono unicamente quelle in cui la circonferenza orbitale ospita un numero intero di lunghezze d'onda associate alla particella, configurando di fatto la costituzione di un'onda stazionaria.

### La Struttura Formale del Dualismo: L'Esperimento delle Due Fenditure
La necessità di un formalismo in grado di gestire simultaneamente particelle (che arrivano in pacchetti discreti e indivisibili) e onde (che interferiscono) si rivela in modo paradigmatico nell'esperimento delle due fenditure.
Nella meccanica classica, per i corpuscoli (es. proiettili), le probabilità di passaggio attraverso le fenditure si sommano linearmente:
$$ P_{12} = P_1 + P_2 $$
Al contrario, per le onde, si sommano le ampiezze del campo, generando l'intensità (interferenza):
$$ I_{12} = |h_1 + h_2|^2 = I_1 + I_2 + 2\sqrt{I_1 I_2}\cos\delta $$
dove l'ultimo addendo rappresenta il termine di interferenza e $\delta$ la differenza di fase.

Per le particelle microscopiche, quali gli elettroni, i rivelatori misurano l'arrivo di entità discrete (particelle), ma la distribuzione spaziale della probabilità di arrivo manifesta frange d'interferenza (onde), invalidando l'additività classica: $P_{12} \neq P_1 + P_2$. 
Per descrivere questo fenomeno, la meccanica quantistica postula l'esistenza di un'ampiezza di probabilità intrinsecamente complessa, denotata con $\phi$. La probabilità osservabile $P$ è il modulo quadro di tale ampiezza:
$$ P = |\phi|^2 $$
Quando un evento quantistico può realizzarsi secondo percorsi alternativi indistinguibili, si applica il principio di sovrapposizione alle ampiezze, non alle probabilità :
$$ \phi = \phi_1 + \phi_2 \implies P_{12} = |\phi_1 + \phi_2|^2 $$
Tuttavia, se viene inserito un apparato per determinare la traiettoria precisa dell'elettrone (ad esempio, illuminandolo con una sorgente di luce), lo stato viene perturbato, forzando la particella in uno stato definito. In questo caso, le alternative diventano distinguibili e il termine di interferenza scompare, recuperando l'additività classica delle probabilità: $P'_{12} = P'_1 + P'_2$.

### Il Principio di Indeterminazione come Fondamento del Dualismo
Il concetto classico di traiettoria cessa di avere validità nella meccanica quantistica. La natura ondulatoria impone un limite fondamentale alla simultanea determinazione di grandezze coniugate, formalizzato da Heisenberg nel 1927 come il Principio di Indeterminazione:
$$ \Delta p \cdot \Delta x \ge \frac{\hbar}{2} $$
Questa disuguaglianza intrinseca spiega il collasso dell'interferenza nell'esperimento delle fenditure qualora si effettui una misurazione. Se la distanza tra le fenditure è $a$ e la distanza dello schermo è $D$, l'impulso trasmesso dalla luce all'elettrone per localizzarlo deve essere almeno dell'ordine di $\Delta p \simeq 2p \sin\theta \simeq \frac{pa}{D}$. 
Ne consegue che l'incertezza sulla posizione dell'elettrone diventa:
$$ \Delta x \approx \frac{\hbar}{\Delta p} \approx \frac{h D}{p a} \approx \frac{\lambda D}{a} $$
Poiché la distanza tra due massimi di interferenza consecutivi sullo schermo è esattamente pari a $\Delta x = \frac{\lambda D}{a}$, lo spostamento casuale $\Delta x$ indotto dalla misurazione di posizione distrugge completamente la visibilità delle frange d'interferenza. O si osserva la natura particellare (traiettoria misurata), o si osserva la natura ondulatoria (interferenza), ma mai entrambe simultaneamente.

### Rappresentazione Matematica: Onde Piane e Pacchetti d'Onda
Nel formalismo astratto che ne scaturisce, l'impulso di una particella diviene un operatore differenziale agente nello spazio delle coordinate:
$$ \vec{p} = -i\hbar\vec{\nabla} $$
L'equazione agli autovalori per l'operatore impulso, $\vec{p}|\vec{p}'\rangle = \vec{p}'|\vec{p}'\rangle$, espressa nella rappresentazione delle coordinate, si risolve tramite la funzione :
$$ \psi_{\vec{p}'}(\vec{x}') \equiv \langle\vec{x}'|\vec{p}'\rangle = \frac{1}{(2\pi\hbar)^{3/2}} e^{\frac{i}{\hbar}\vec{p}'\cdot\vec{x}'} $$
Questa soluzione descrive un'onda piana, idealizzazione matematica di un autostato dell'impulso. In accordo con il principio di Heisenberg, poiché l'impulso è perfettamente noto ($\Delta p = 0$), la distribuzione spaziale della probabilità risulta omogenea ed infinitamente estesa: $P(x, x+dx) = |N|^2 dx$.

Affinché l'onda di materia possa descrivere una particella localizzata in una determinata regione spaziale, si deve abbandonare l'onda piana singola in favore di una sovrapposizione continua di stati ad impulso definito, generando un "pacchetto d'onda". L'esempio più significativo è il pacchetto d'onda gaussiano, la cui funzione d'onda unidimensionale è:
$$ \psi_\alpha(x') = \frac{1}{(2\pi\sigma^2)^{1/4}} e^{i\frac{p_0 x'}{\hbar} - \frac{x'^2}{4\sigma^2}} $$
La densità di probabilità associata è una gaussiana pura centrata nell'origine con varianza spaziale $\sigma^2$:
$$ |\psi_\alpha(x')|^2 = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{x'^2}{2\sigma^2}} $$
Calcolando i valori di aspettazione operatoriali per questo stato, otteniamo le dispersioni :
$$ \langle(\Delta x)^2\rangle = \langle x^2\rangle - \langle x\rangle^2 = \sigma^2 $$
$$ \langle(\Delta p)^2\rangle = \langle p^2\rangle - \langle p\rangle^2 = \frac{\hbar^2}{4\sigma^2} $$
Il prodotto delle rispettive indeterminazioni (le radici quadrate delle varianze) converge esattamente al limite inferiore consentito dalla meccanica quantistica:
$$ \Delta x \cdot \Delta p = \frac{\hbar}{2} $$
Il pacchetto gaussiano rappresenta dunque lo stato fisico che ottimizza il compromesso tra la localizzazione di una particella puntiforme e la propagazione intrinsecamente diffusa di un'onda. Questo oggetto matematico sintetizza alla perfezione il dualismo onda-particella prefigurato dall'Ipotesi di De Broglie.