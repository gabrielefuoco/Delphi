### Introduzione e Formulazione del Problema
L'oscillatore armonico rappresenta uno dei modelli fondamentali della fisica teorica. Si consideri una particella vincolata a compiere piccole oscillazioni unidimensionali. Secondo la meccanica classica, l'energia potenziale di tale particella è pari a $\frac{1}{2}m\omega^2x^2$, dove $\omega$ rappresenta la frequenza propria delle oscillazioni classiche. 

Il passaggio alla meccanica quantistica richiede la formulazione dell'operatore Hamiltoniano del sistema, che è dato dalla somma dell'energia cinetica e dell'energia potenziale:
$$H = \frac{p^2}{2m} + \frac{1}{2}m\omega^2x^2$$ 
Poiché l'energia potenziale diverge, ovvero diventa infinita per $x \to \pm\infty$, la particella è costretta a compiere esclusivamente un moto finito. Da questa limitazione spaziale discende una conseguenza fisica di estrema importanza: l'intero spettro energetico dell'oscillatore armonico risulta essere strettamente discreto.

I livelli energetici dell'oscillatore si ricavano risolvendo l'equazione di Schrödinger indipendente dal tempo:
$$H\psi = -\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + \frac{1}{2}m\omega^2x^2\psi = E\psi$$ 
Alla suddetta equazione differenziale devono essere imposte rigorose condizioni al contorno affinché le soluzioni abbiano significato fisico. Nello specifico, la funzione d'onda deve annullarsi all'infinito:
$$\lim_{x\to\pm\infty} \psi(x) = 0$$ 

### Il Metodo Operatoriale di Dirac
Sebbene l'equazione di Schrödinger possa essere risolta analiticamente, il problema della determinazione dei livelli energetici e dei relativi autostati può essere affrontato attraverso un elegante metodo operatoriale sviluppato da Dirac. 

Il primo passo consiste nell'introdurre degli operatori adimensionali, dividendo entrambi i membri dell'operatore Hamiltoniano per la quantità $\hbar\omega$. Si definiscono pertanto i seguenti operatori adimensionali per l'Hamiltoniano, l'impulso e la posizione:
$$\hat{H} = \frac{H}{\hbar\omega} \quad, \quad \hat{p} = \frac{p}{\sqrt{m\hbar\omega}} \quad, \quad \hat{x} = \sqrt{\frac{m\omega}{\hbar}}x$$ 
Con queste definizioni, l'Hamiltoniano adimensionale assume la forma simmetrica:
$$\hat{H} = \frac{1}{2}(\hat{p}^2 + \hat{x}^2)$$ 

Procediamo con il calcolo del commutatore tra i nuovi operatori $\hat{p}$ e $\hat{x}$. Sfruttando le regole di commutazione canoniche standard $[p, x] = -i\hbar$, si ottiene:
$$[\hat{p}, \hat{x}] = \frac{1}{\sqrt{m\hbar\omega}} \sqrt{\frac{m\omega}{\hbar}} [p, x] = \frac{1}{\hbar}(-i\hbar) = -i$$ 

**Operatori di Creazione e Distruzione:**
Il nucleo del metodo di Dirac risiede nella definizione di due operatori non hermitiani lineari costruiti a partire da $\hat{x}$ e $\hat{p}$:
$$a = \frac{1}{\sqrt{2}}(\hat{x} + i\hat{p}) \quad, \quad a^+ = \frac{1}{\sqrt{2}}(\hat{x} - i\hat{p})$$ 
Il commutatore tra questi due operatori risulta fondamentale per l'algebra del sistema. Sfruttando la linearità del commutatore e il risultato $[\hat{p}, \hat{x}] = -i$, si calcola:
$$[a, a^+] = \frac{1}{2}[\hat{x} + i\hat{p}, \hat{x} - i\hat{p}] = \frac{1}{2}\left(-i[\hat{x}, \hat{p}] + i[\hat{p}, \hat{x}]\right) = i[\hat{p}, \hat{x}] = i(-i) = 1$$ 

Invertendo le definizioni di $a$ e $a^+$ per isolare $\hat{x}$ e $\hat{p}$, si ha:
$$\hat{x} = \frac{1}{\sqrt{2}}(a + a^+) \quad, \quad \hat{p} = \frac{-i}{\sqrt{2}}(a - a^+)$$ 
Sostituendo queste espressioni nell'Hamiltoniano adimensionale, la forma dell'operatore si trasforma in:
$$\hat{H} = \frac{1}{4}\left[-(a - a^+)^2 + (a + a^+)^2\right] = \frac{1}{2}(aa^+ + a^+a) = \frac{1}{2}([a, a^+] + 2a^+a) = a^+a + \frac{1}{2}$$ 
Tornando alle unità fisiche originali, l'Hamiltoniano dell'oscillatore armonico si esprime definitivamente come:
$$H = \hbar\omega\left(a^+a + \frac{1}{2}\right)$$ 

### Spettro Energetico e Operatore Numero
Per studiare l'azione di $H$ sui suoi autostati, valutiamo i commutatori dell'Hamiltoniano con $a$ e $a^+$. Poiché $[a^+a, a] = a^+[a, a] + [a^+, a]a = -a$, si ricava:
$$[H, a] = \hbar\omega[a^+a + \frac{1}{2}, a] = \hbar\omega[a^+, a]a = -\hbar\omega a$$ 
Allo stesso modo, applicando le proprietà dell'aggiunto hermitiano, si ottiene:
$$[H, a^+] = -[H, a]^+ = \hbar\omega a^+$$ 

**L'azione sugli autostati:**
Si supponga che esista un autostato $|n\rangle$ dell'Hamiltoniano con autovalore $E_n$, tale che $H|n\rangle = E_n|n\rangle$. Applicando l'operatore $H$ allo stato modificato $a|n\rangle$, si evince:
$$H(a|n\rangle) = ([H, a] + aH)|n\rangle = (-\hbar\omega a + E_n a)|n\rangle = (E_n - \hbar\omega)(a|n\rangle)$$ 
Questo risultato dimostra che se $|n\rangle$ è un autostato con energia $E_n$, allora $a|n\rangle$ è a sua volta un autostato con energia ridotta di un quanto $\hbar\omega$. Per questo motivo, l'operatore $a$ prende il nome formale di **operatore di distruzione**.

In maniera speculare, applicando $H$ allo stato $a^+|n\rangle$:
$$H(a^+|n\rangle) = ([H, a^+] + a^+H)|n\rangle = (\hbar\omega a^+ + E_n a^+)|n\rangle = (E_n + \hbar\omega)(a^+|n\rangle)$$ 
Questo dimostra che $a^+|n\rangle$ è un autostato con energia incrementata di $\hbar\omega$, conferendo all'operatore $a^+$ il nome di **operatore di creazione**.

**Lo stato fondamentale e la quantizzazione dell'energia:**
È essenziale dimostrare che l'energia dell'oscillatore non può assumere valori arbitrariamente negativi. Valutando il valore di aspettazione dell'Hamiltoniano in uno stato generico $|n\rangle$:
$$E_n = \langle n|H|n\rangle = \hbar\omega\left\langle n\left|a^+a + \frac{1}{2}\right|n\right\rangle = \hbar\omega\left(\langle n'|n'\rangle + \frac{1}{2}\right) \ge \frac{1}{2}\hbar\omega$$ 
dove è stato posto $|n'\rangle = a|n\rangle$. Poiché la norma di un vettore $\langle n'|n'\rangle$ è definita positiva, l'energia ammette un limite inferiore. 

Deve pertanto esistere uno stato fondamentale, denotato con $|0\rangle$, al di sotto del quale l'operatore di distruzione non può generare alcuno stato. Matematicamente questo si impone richiedendo:
$$a|0\rangle = 0$$ 
L'energia di questo stato fondamentale (o energia di punto zero) vale:
$$H|0\rangle = \hbar\omega\left(a^+a + \frac{1}{2}\right)|0\rangle = \frac{1}{2}\hbar\omega|0\rangle \implies E_0 = \frac{1}{2}\hbar\omega$$ 

Applicando ripetutamente l'operatore di creazione $a^+$, i livelli energetici superiori si ergono discreti e separati da intervalli costanti di $\hbar\omega$. Si giunge alla forma chiusa dello spettro energetico:
$$E_n = \left(n + \frac{1}{2}\right)\hbar\omega \quad, \quad n = 0, 1, 2, \dots$$ 
Tali livelli risultano interamente non degeneri. L'operatore $a^+a$, i cui autovalori corrispondono esattamente all'intero $n$, viene definito **operatore numero** $N = a^+a$, tale che $N|n\rangle = n|n\rangle$.

### Costruzione degli Autostati
Gli stati $|n\rangle$ costituiscono una base ortonormale completa e si generano mediante l'applicazione ripetuta di $a^+$ sullo stato vuoto. Includendo i fattori di normalizzazione tali per cui $\langle n|n\rangle = 1$, l'azione degli operatori a scala risulta rigorosamente definita come:
$$a|n\rangle = \sqrt{n}|n-1\rangle \quad ; \quad a^+|n-1\rangle = \sqrt{n}|n\rangle$$ 
L'autostato di ordine $n$-esimo è pertanto calcolabile tramite la formula generale iterativa:
$$|n\rangle = \frac{1}{\sqrt{n!}}(a^+)^n|0\rangle$$ 

### Rappresentazione delle Coordinate e Polinomi di Hermite
Al fine di determinare la forma esplicita delle funzioni d'onda spaziali dell'oscillatore, traduciamo l'algebra astratta nella rappresentazione delle coordinate. L'azione dell'operatore di distruzione sullo stato fondamentale si esprime come:
$$\langle x'|a|0\rangle = \frac{1}{\sqrt{2}}\langle x'|(\hat{x} + i\hat{p})|0\rangle = 0$$ 
Introducendo la variabile spaziale adimensionale $\xi = \frac{x'}{x_0}$ con $x_0 = \sqrt{\frac{\hbar}{m\omega}}$, gli operatori di posizione e impulso divengono differenziali: $\hat{x} = \xi$ e $\hat{p} = -i\frac{d}{d\xi}$. Gli operatori di costruzione e distruzione assumono la forma analitica:
$$a = \frac{1}{\sqrt{2}}\left(\xi + \frac{d}{d\xi}\right) \quad, \quad a^+ = \frac{1}{\sqrt{2}}\left(\xi - \frac{d}{d\xi}\right)$$ 

Sostituendo l'operatore $a$ nell'equazione che annulla lo stato fondamentale si origina una equazione differenziale del primo ordine:
$$\frac{1}{\sqrt{2}}\left(\xi + \frac{d}{d\xi}\right)\psi_0(\xi) = 0 \implies \frac{d\psi_0}{d\xi} = -\xi\psi_0$$ 
Separando le variabili ed integrando, la soluzione restituisce un andamento puramente gaussiano: $\psi_0(\xi) = C e^{-\xi^2/2}$. Imponendo la rigorosa normalizzazione spaziale:
$$\int_{-\infty}^{+\infty} dx' |\psi_0(x')|^2 = x_0 \int_{-\infty}^{+\infty} d\xi |C|^2 e^{-\xi^2} = |C|^2 x_0 \sqrt{\pi} = 1$$ 
si deduce che $C = \frac{1}{\pi^{1/4}\sqrt{x_0}}$ (assunto reale e positivo), giungendo alla forma canonica per la funzione d'onda del livello base:
$$\psi_0(\xi) = \frac{1}{\pi^{1/4}\sqrt{x_0}} e^{-\xi^2/2}$$ 

Le funzioni d'onda degli stati eccitati $\psi_n(\xi)$ vengono derivate iterativamente applicando l'operatore $a^+$ nella rappresentazione spaziale:
$$\psi_n(\xi) = \frac{1}{\sqrt{2^n n!}}\left(\xi - \frac{d}{d\xi}\right)^n \psi_0(\xi) = \frac{1}{\pi^{1/4}\sqrt{2^n n! x_0}}\left(\xi - \frac{d}{d\xi}\right)^n e^{-\xi^2/2}$$ 
La sequenza differenziale inquadrata tra le parentesi definisce implicitamente una classe nota di polinomi. L'espressione matematica:
$$\left(\xi - \frac{d}{d\xi}\right)^n e^{-\xi^2/2} = H_n(\xi) e^{-\xi^2/2}$$ 
costituisce la definizione dei **Polinomi di Hermite**, $H_n(\xi)$, polinomi di grado $n$ che esibiscono parità definita e alternante in concomitanza all'indice $n$. 

Le autofunzioni complete dell'oscillatore armonico sono in definitiva il prodotto di tali polinomi per un decadimento gaussiano:
$$\psi_n(\xi) = \frac{1}{\pi^{1/4}\sqrt{2^n n! x_0}} H_n(\xi) e^{-\xi^2/2}$$ 

**Parità degli autostati:**
Il potenziale originario $V(x) = \frac{1}{2}m\omega^2x^2$ è una funzione rigidamente pari, ovvero $V(x) = V(-x)$, la qual cosa garantisce la commutazione tra l'Hamiltoniano e l'operatore di Parità spaziale $[H, P] = 0$. Siccome i polinomi di Hermite $H_n(\xi)$ contengono solo potenze pari per $n$ pari e potenze dispari per $n$ dispari, le autofunzioni risultanti $\psi_n(\xi)$ possiedono anch'esse la medesima parità quantistica del numero associato allo stato: sono simultaneamente autostati sia dell'energia che dell'operatore di Parità.

### Relazioni Termodinamiche e Meccaniche Avanzate
**Energia Statistica in Equilibrio Termico:**
Come dimostrazione di convergenza con la Meccanica Statistica Classica che storicamente evidenziò la crisi pre-quantistica, se si studia l'energia media di un oscillatore armonico unidimensionale classiaco all'equilibrio termodinamico tramite la funzione di partizione $Z = \iint_{-\infty}^{+\infty} dp\,dx\,e^{-\beta (\frac{p^2}{2m} + \frac{1}{2}m\omega^2x^2)}$, questa riproduce infallibilmente l'energia equipartita dell'oscillatore $\langle E \rangle = KT$. Tuttavia, la deviazione della natura da tale legge (catastrofe ultravioletta) spinse Planck ad imporre proprio il postulato della quantizzazione dell'energia $E = n\hbar\omega$ preannunciando la struttura discreta dello spettro esaminato sopra in equazione (10.27).

**Teorema del Viriale Quantistico:**
Si ricorda, infine, che l'oscillatore armonico offre una splendida applicazione del *Teorema del Viriale* in meccanica quantistica. Tale teorema afferma che, per un potenziale funzione omogenea delle coordinate di grado $k$ tale che $\sum_i x_i \frac{\partial V}{\partial x_i} = k V$, i valori medi dell'energia cinetica e potenziale in stati stazionari sono correlati da $\langle n|T|n\rangle = \frac{k}{2}\langle n|V|n\rangle$. Poiché il potenziale dell'oscillatore armonico è unicamente quadratico nelle variabili ($k=2$), ne scaturisce l'elegante uguaglianza per cui in qualsiasi stato stazionario $\langle T \rangle = \langle V \rangle$.