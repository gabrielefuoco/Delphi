## Introduzione e Limiti del Modello Classico
Tra la fine del diciannovesimo e i primi anni del ventesimo secolo, lo sviluppo della fisica classica aveva raggiunto un grado di maturità tale per cui i fisici ritenevano di aver compreso le leggi fondamentali in grado di spiegare qualunque fenomeno naturale. Da un lato, la meccanica di Newton forniva un impianto rigorosamente deterministico: la seconda legge della dinamica, $F = ma$, costituiva un'equazione differenziale che, una volta note le posizioni e le velocità iniziali, permetteva di integrare esattamente il moto di ogni costituente di un sistema fisico per qualsiasi istante di tempo successivo. Dall'altro lato, le equazioni di Maxwell unificavano compiutamente i fenomeni elettrici e magnetici, dimostrando che i campi si propagano nello spazio sotto forma di onde elettromagnetiche e ponendo apparentemente fine all'antica disputa sulla natura della luce a favore della teoria ondulatoria. 

Tuttavia, una serie incalzante di evidenze sperimentali riguardanti i processi su scala atomica rese palese l'insufficienza di questo costrutto teorico. L'indagine di questi fenomeni microscopici richiese un mutamento radicale dei concetti fisici e matematici fondamentali, dando vita alla meccanica quantistica. Tale teoria non possiede più il carattere deterministico della meccanica classica, ma stabilisce che le leggi naturali governino le probabilità con cui occorrono determinati eventi fisici, in base a una caratteristica intrinseca della natura e non a causa di una presunta incompletezza dell'osservazione. Nel seguito, analizzeremo formalmente i fenomeni cruciali che segnarono l'avvento della teoria quantistica, evidenziando il dualismo onda-particella della radiazione e della materia.

## Lo Spettro di Corpo Nero e l'Ipotesi Quantistica di Planck
Un corpo nero è definito idealmente come un corpo capace di assorbire completamente tutta la radiazione elettromagnetica incidente su di esso. In base alla legge di Kirchhoff, il rapporto tra il potere emissivo $E(\omega, T)$ (energia emessa per unità di volume a frequenza $\omega$ e temperatura termodinamica $T$) e il potere assorbitivo $A(\omega, T)$ è una funzione universale $u(\omega, T)$ :
$$ \frac{E(\omega, T)}{A(\omega, T)} = u(\omega, T) $$ 
Poiché per un corpo nero il potere assorbitivo è strettamente pari all'unità, il suo potere emissivo coincide esattamente con la funzione universale, rappresentando la densità di energia della radiazione elettromagnetica in equilibrio termico in una cavità.

La descrizione classica di tale densità di energia risultava intrinsecamente incoerente. Secondo le leggi dell'elettrodinamica e della meccanica statistica classica, si perviene alla celebre formula di Rayleigh-Jeans :
$$ u(\omega, T) = \frac{\omega^2}{\pi^2 c^3} KT $$ 
dove $K$ è la costante di Boltzmann e $c$ la velocità della luce. Questa formulazione, pur essendo valida per basse frequenze, porta a un irrisolvibile assurdo fisico se integrata su tutto lo spettro, determinando un'energia totale infinita, fenomeno noto come "catastrofe ultravioletta" :
$$ E(T) = \int_0^\infty d\omega \, u(\omega, T)_{R.J.} = \frac{KT}{\pi^2 c^3} \int_0^\infty d\omega \, \omega^2 = \infty $$ 
Per frequenze molto alte, l'osservazione sperimentale era descritta empiricamente dalla formula di Wien, $u(\omega, T) = C \omega^3 e^{-\lambda\omega/T}$, priva di una rigorosa base teorica.

Max Planck risolse questa crisi derivando una nuova espressione analitica in grado di interpolare esattamente i regimi di alta e bassa frequenza. Planck ottenne la seguente funzione spettrale :
$$ u(\omega, T) = \frac{\hbar}{\pi^2 c^3} \frac{\omega^3}{e^{\hbar\omega/KT} - 1} $$ 
introducendo in tal modo una nuova costante fondamentale, la costante di Planck (nella sua forma ridotta $\hbar$), pari a $\hbar = 1.054 \cdot 10^{-27} \text{ erg} \cdot \text{s}$. Questa equazione riproduce la legge di Rayleigh-Jeans per $\hbar\omega \ll KT$ e la legge di Wien per $\hbar\omega \gg KT$. 

La radicale innovazione del lavoro di Planck risiede nella giustificazione statistica e termodinamica di questa formula. Secondo l'elettromagnetismo in cavità, il numero di modi normali di oscillazione $dn$ della radiazione per unità di volume compreso tra le frequenze $\omega$ e $\omega + d\omega$ è espresso da :
$$ \frac{1}{V} \frac{dn}{d\omega} = \frac{\omega^2}{\pi^2 c^3} $$ 
Nel calcolo classico, il teorema di equipartizione dell'energia stabilisce che l'energia media $\langle E \rangle$ di ogni oscillatore armonico è pari a $KT$. Planck rigettò il presupposto classico della continuità dell'energia postulando invece che un oscillatore potesse scambiare energia solo in multipli interi di una quantità elementare, detta "quanto". Egli assunse che tale quanto elementare di energia $\epsilon$ fosse linearmente legato alla frequenza del modo normale:
$$ \epsilon = \hbar\omega $$ 
Pertanto, le energie accessibili dell'oscillatore sono discrete e descritte da:
$$ E_n = n \epsilon = n \hbar\omega \quad, \quad n = 0, 1, 2\dots $$ 
Mediante la meccanica statistica, definendo $\beta = 1/(KT)$, la funzione di partizione $Z$ dell'oscillatore quantistico si calcola sommando su tutti gli stati possibili :
$$ Z = \sum_{n=0}^{\infty} e^{-\beta E_n} = \sum_{n=0}^{\infty} e^{-\beta n \hbar\omega} = \frac{1}{1 - e^{-\beta\hbar\omega}} $$ 
L'energia media dell'oscillatore è derivabile dalla funzione di partizione mediante $\langle E \rangle = -\frac{\partial \ln Z}{\partial \beta}$ che restituisce il risultato rigoroso:
$$ \langle E \rangle = -\frac{\partial}{\partial\beta} \ln\left( \frac{1}{1 - e^{-\beta\hbar\omega}} \right) = \frac{\hbar\omega}{e^{\hbar\omega/KT} - 1} $$ 
Il prodotto di questa energia termica quantizzata per il numero di modi per unità di volume riproduce senza approssimazioni l'equazione universale dello spettro di corpo nero. Si manifestava così, per la prima volta, la natura intrinsecamente corpuscolare dell'energia della radiazione.

## L'Effetto Fotoelettrico e il Fotone di Einstein
La dimostrazione della struttura particellare della radiazione trovò ulteriore e decisiva verifica nell'interpretazione dell'effetto fotoelettrico (scoperto da Hertz nel 1887), formulata da Albert Einstein nel 1905. Sperimentalmente, la superficie di un metallo irradiata da un'onda elettromagnetica emette elettroni. Tale fenomeno presenta tre proprietà cruciali inspiegabili per il formalismo dell'elettrodinamica classica. In primis, la comparsa della fotoemissione mostra l'esistenza di una frequenza di soglia $\omega_s$ (dipendente dal metallo), al di sotto della quale nessuna radiazione è in grado di innescare l'effetto. In secondo luogo, la quantità di fotoelettroni espulsi scala linearmente con l'intensità della luce. Infine, l'energia cinetica degli elettroni emessi dipende unicamente ed in modo lineare dalla frequenza della radiazione, essendo totalmente ininfluenzata dalla sua intensità. 

Secondo l'elettrodinamica classica, tale fenomeno è inammissibile: l'energia convogliata dall'onda è data dall'intensità e risulta scollegata dalla frequenza. Einstein superò radicalmente il modello ondulatorio, proponendo che la luce incidente non fosse continua, ma quantizzata in singole particelle dette "fotoni", la cui energia è espressa dalla medesima formula di Planck:
$$ E = \hbar\omega $$ 
Quando un elettrone del metallo assorbe un singolo fotone, il suo patrimonio energetico incrementa di una quota $\hbar\omega$. Affinché l'elettrone si disancori dal reticolo metallico è richiesta una frazione di energia, detta funzione di lavoro $W$, propria di ogni specifico materiale. Per il principio di conservazione dell'energia, la bilancia energetica del processo fotoelettrico è definita rigorosamente da:
$$ E_{el} = \frac{1}{2}mv^2 = \hbar\omega - W $$ 
Quest'ultima equazione include automaticamente sia la condizione di soglia (ossia l'esigenza di avere $\hbar\omega \ge W$) sia la correlazione lineare tra l'energia meccanica della carica estratta e la frequenza quantizzata. L'intensità del fascio luminoso si traduce macroscopicamente nel mero quantitativo totale di fotoni, e quindi nel numero proporzionale di elettroni fotoemessi, suggellando l'efficacia del costrutto einsteiniano.

## La Cinematica Quantistica dell'Effetto Compton
La suprema e incrollabile evidenza della validità della concezione particellare o "corpuscolare" della luce giunse nel 1922 ad opera dell'effetto Compton. Sperimentalmente, investendo un foglio metallico con radiazione avente lunghezza d'onda caratteristica dei raggi X, Compton rilevò che i raggi venivano diffusi con una lunghezza d'onda variata; questo spostamento si rivelò in stretta dipendenza con l'angolo di deviazione osservato. La dottrina classica (scattering Thomson), al contrario, supponendo che l'onda spingesse gli elettroni a moti di oscillazione forzata, prevedeva una successiva irradiazione priva di variazioni nella lunghezza d'onda. 

Compton analizzò teoricamente la diffusione come un autentico urto elastico su scala microscopica fra un singolo corpuscolo di luce (fotone) e un elettrone a riposo. Il fotone incidente, di frequenza $\omega$ e vettore d'onda $\vec{k}$, detiene energia pari a $E = \hbar\omega$ e impulso di modulo $q = \hbar|\vec{k}|$. Trattandosi di particelle a massa nulla e valendo la relazione relativistica $E = cq$, ne deriva che $\omega = c|\vec{k}|$. L'apparato cinematico è descritto attraverso il formalismo dei quadrivettori energia-impulso. Per il fotone incidente e quello diffuso si definiscono:
$$ q = \left(\frac{\hbar\omega}{c}, \hbar\vec{k}\right) \quad, \quad q' = \left(\frac{\hbar\omega'}{c}, \hbar\vec{k}'\right) $$ 
tali da soddisfare rigorosamente $q^2 = q'^2 = 0$. 
L'elettrone bersaglio, posizionato staticamente, possiede quadrimpulso pari a:
$$ p = (mc, \vec{0}) \quad \text{con} \quad p^2 = m^2 c^2 $$ 
La conservazione del quadrimpulso per il sistema globale isolato stabilisce che:
$$ p + q = p' + q' $$ 
Elevando al quadrato il termine dell'elettrone diffuso $p'$, la massa a riposo è preservata, donde:
$$ p'^2 = m^2 c^2 = (p + q - q')^2 = p^2 + q^2 + q'^2 + 2pq - 2pq' - 2qq' $$ 
Sviluppando in dettaglio i prodotti scalari quadridimensionali e ricordando che $\omega = ck$ e $\omega' = ck'$, si manifesta la seguente eguaglianza:
$$ m^2 c^2 + \frac{2m\hbar\omega}{c} - \frac{2m\hbar\omega'}{c} - \frac{2\hbar^2\omega\omega'}{c^2} + \frac{2\hbar^2 k k' \cos\theta}{c} = m^2 c^2 $$ 
Semplificando e procedendo all'isolamento della variazione di frequenza:
$$ \omega - \omega' = \frac{\hbar}{mc^2} \omega\omega'(1 - \cos\theta) $$ 
Poiché lunghezza d'onda e frequenza sono intrecciate dalla legge di proporzionalità $\lambda = \frac{2\pi c}{\omega}$ moltiplicando la relazione per il fattore di conversione $\frac{2\pi c}{\omega\omega'}$, la deduzione conduce immancabilmente all'equazione nota come "Formula di Compton" :
$$ \lambda' - \lambda = \frac{h}{mc} (1 - \cos\theta) $$ 
La costante dimensionale di natura spaziale $h/mc$ generata dai calcoli è detta "lunghezza d'onda Compton dell'elettrone", formalizzata in $\lambda_C \equiv \frac{h}{mc} \simeq 2.4 \cdot 10^{-10}$ cm. Questo mirabile accordo teorico-sperimentale impose l'adozione definitiva di un modello della materia dualistico.

## Onde di Materia di De Broglie e Modello Atomico di Bohr
Nel 1923 il fisico Louis De Broglie, colpito dall'apparente dualismo della radiazione elettromagnetica, sollevò l'ipotesi di una totale simmetria ontologica tra radiazione e corpuscoli dotati di massa: se la luce si comportava come particelle, la materia doveva godere di peculiarità ondulatorie. Richiamandosi all'equazione del fotone, l'impulso $p$ e la lunghezza d'onda di materia $\lambda$ sarebbero governati dalla relazione:
$$ p = \hbar k = \frac{2\pi \hbar}{\lambda} = \frac{h}{\lambda} \Rightarrow \lambda = \frac{h}{p} $$ 
Questa grandiosa intuizione ha ricevuto collaudo fattuale dai celebri esperimenti di Davisson-Germer in cui lo scattering e la diffrazione di fasci di elettroni obbedivano pienamente alle leggi di interferenza governate dalla formula di Bragg:
$$ 2a \sin\theta = n\lambda $$ 
Tale concezione fornì la tanto attesa spiegazione fisica agli insormontabili dilemmi del modello atomico. Il modello nucleare e planetario formulato da Rutherford si rivelò infatti instabile: per le leggi classiche dell'elettrodinamica, un elettrone ruotante, in quanto carica perennemente accelerata dal nucleo, deve irradiare di continuo collassando verso il centro di massa del sistema, distruggendo l'atomo in scale temporali asintoticamente trascurabili (10$^{-10}$ s). Al contempo, il modello planetario falliva clamorosamente nel razionalizzare il comportamento prettamente discreto dello spettro ottico atomico, governato secondo precise proporzioni intere:
$$ \frac{1}{\lambda} = cost. \left( \frac{1}{n_1^2} - \frac{1}{n_2^2} \right) $$ 

Il quadro venne formalizzato dal genio danese di Niels Bohr nel 1913. Sulla base di stringenti assiomi "ad hoc", Bohr statuì un modello d'atomo d'idrogeno dove l'elettrone permane su orbite in uno "stato stazionario" esente da emissioni radiative. Il nucleo concettuale risiedeva nella quantizzazione rigorosa del momento angolare orbitale: l'elettrone si fissa in moto stazionario solamente in quelle peculiari orbite per le quali il momento angolare si rivela essere multiplo intero della costante di Planck ridotta :
$$ L = mvr = n\hbar $$ 
con radiazione intercettata o espulsa solo in occasione di transizioni nette ed istantanee fra questi precisi salti di livelli energetici $E$, calcolate attraverso $\hbar\omega = E - E'$. L'equazione di equilibrio gravitante fra la reazione coulombiana e le forze centripete:
$$ F_{coul} = F_{centr} \Rightarrow \frac{e^2}{r^2} = \frac{mv^2}{r} $$ 
si risolve accoppiandola all'ipotesi della quantizzazione di $L$, originando per il raggio orbitale e per la velocità elettronica le definizioni quantizzate:
$$ r = n^2 \frac{\hbar^2}{me^2} \equiv n^2 a_0 \quad, \quad \frac{v}{c} = \frac{1}{n} \frac{e^2}{\hbar c} \equiv \frac{\alpha}{n} $$ 
ove emergono due costanti preminenti per tutta la fisica teorica: il raggio di Bohr $a_0 = \frac{\hbar^2}{me^2} \simeq 0.529 \cdot 10^{-8}$ cm e la costante di struttura fine adimensionale $\alpha = \frac{e^2}{\hbar c} \simeq \frac{1}{137}$. Attraverso simili presupposti orbitali, procediamo all'esatta deduzione dell'energia totale del sistema:
$$ E = \frac{p^2}{2m} - \frac{e^2}{r} = -\frac{1}{2n^2} m c^2 \alpha^2 $$ 
La formidabile esattezza matematica del modello Bohr eguaglia le discrepanze spettroscopiche classiche derivando senza alcuno scostamento la formula di emissione degli idrogenoidi :
$$ \hbar\omega = E - E' = \frac{1}{2} m c^2 \alpha^2 \left( \frac{1}{n'^2} - \frac{1}{n^2} \right) $$ 
A consacrare ulteriormente i calcoli di Bohr, l'assunzione di quantizzazione del momento angolare fu in un secondo momento perfettamente derivata per corollario dalla meccanica ondulatoria postulabile da De Broglie. L'elettrone confinato ad una circonferenza in un dominio quantistico assume l'identità di un'onda di forma stazionaria; la condizione affinché tale espansione risuoni sul proprio spazio orbitante necessita l'inserimento esatto di un numero di nodi interi di lunghezza d'onda :
$$ L = mvr = pr = \frac{h}{\lambda}r = n\hbar = n\frac{h}{2\pi} \Rightarrow 2\pi r = n\lambda $$ 
Così, la chiusura topologica del cammino circolare attorno al nucleo esige che la circonferenza equivalga a un multiplo di autovalori stazionari di onde costituenti la materia.