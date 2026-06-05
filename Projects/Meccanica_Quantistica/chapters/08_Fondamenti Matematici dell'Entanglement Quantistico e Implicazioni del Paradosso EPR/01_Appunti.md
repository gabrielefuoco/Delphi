## Introduzione: Indeterminismo, Variabili Nascoste e Disuguaglianze di Bell
Lo sviluppo della meccanica quantistica ha rappresentato una profonda rivoluzione scientifica e concettuale, non solo per l'introduzione di nuove leggi, ma per il loro carattere intrinsecamente probabilistico. Diversamente dalla meccanica classica, le leggi quantistiche non sono deterministiche: esse non prevedono il verificarsi di un singolo evento, ma unicamente le probabilità con cui diverse alternative possono realizzarsi. 

Questa natura probabilistica non deriva da un'incompleta conoscenza del sistema, bensì da una proprietà intrinseca del mondo fisico. In risposta a queste peculiarità, alcuni fisici (tra cui Einstein, Podolsky e Rosen nel loro celebre paradosso) ipotizzarono l'esistenza di "variabili nascoste" per ripristinare il determinismo e la località classica. Tuttavia, il testo afferma chiaramente che la non esistenza di variabili nascoste locali è oggi un fatto sperimentalmente accertato, dimostrato attraverso lo studio delle **disuguaglianze di Bell**. Questo risultato chiude storicamente il dibattito iniziato, tra gli altri, tra Einstein e Bohr al Congresso Solvay del 1927 sancendo l'abbandono del realismo locale in favore delle correlazioni non-locali (entanglement).

## Il Principio di Sovrapposizione come Radice dell'Entanglement
Il concetto di entanglement affonda le sue radici matematiche nel principio di sovrapposizione degli stati. Secondo tale principio, ogni stato quantistico $|\phi\rangle$ può essere espresso come una combinazione lineare (o sovrapposizione) di un insieme completo di stati di base $|i\rangle$:

$$|\phi\rangle = \sum_i |i\rangle \langle i|\phi\rangle \equiv \sum_i c_i |i\rangle$$ 

I coefficienti complessi $c_i = \langle i|\phi\rangle$ rappresentano le ampiezze di probabilità. La possibilità per un sistema di trovarsi in una sovrapposizione simultanea di più stati è un concetto puramente quantistico, privo di analogo classico. Questa linearità dello spazio vettoriale complesso (spazio di Hilbert), applicata a sistemi composti da più particelle, dà origine agli stati intrinsecamente correlati (entangled).

## Sistemi Composti e Degenerazione di Scambio
Per comprendere formalmente l'entanglement (o non-separabilità), si consideri la costruzione dello spazio degli stati per un sistema di due particelle. Siano $|a\rangle$ e $|b\rangle$ i vettori di stato che descrivono i possibili stati di singola particella. Il sistema congiunto si descrive banalmente mediante il prodotto tensoriale dei due ket:

$$|a\rangle|b\rangle$$ 

In assenza di correlazioni quantistiche, il sistema è in uno stato separabile, in cui la particella 1 è esattamente nello stato $|a\rangle$ e la particella 2 nello stato $|b\rangle$. Tuttavia, se le due particelle sono indistinguibili o hanno interagito, lo stato generale del sistema diviene una sovrapposizione lineare di stati prodotto:

$$|\psi\rangle = c_1 |a\rangle|b\rangle + c_2 |b\rangle|a\rangle$$ 

Questa espressione rappresenta la cosiddetta "degenerazione di scambio". Uno stato di questo tipo, qualora non sia fattorizzabile come un singolo prodotto tensoriale, rappresenta uno **stato entangled**. In uno stato siffatto, non è più possibile attribuire un vettore di stato ben definito a ciascuna particella singolarmente; l'informazione è interamente codificata nelle correlazioni globali del sistema.

Il principio di indistinguibilità costringe i sistemi di particelle identiche ad assumere unicamente stati altamente entangled. Scambiando le particelle tramite l'operatore di permutazione $P_{12}$, tale che $P_{12}^2 = 1$ e $P_{12}^+ = P_{12}$ il sistema può variare solo per un fattore di fase:

$$P_{12} |\psi\rangle = \pm |\psi\rangle$$ 

Questo porta alla rigida classificazione in stati totalmente simmetrici (Bosoni, statistica di Bose-Einstein) e totalmente antisimmetrici (Fermioni, statistica di Fermi-Dirac). Le uniche configurazioni bipartite ammesse sono quindi combinazioni lineari massimamente entangled:

$$|\psi_S\rangle = \frac{1}{\sqrt{2}} \left( |a\rangle|b\rangle + |b\rangle|a\rangle \right)$$ 
$$|\psi_A\rangle = \frac{1}{\sqrt{2}} \left( |a\rangle|b\rangle - |b\rangle|a\rangle \right)$$ 

## Composizione dei Momenti Angolari e lo Stato Paradigmatico EPR (Singoletto)
La formulazione matematica più celebre del paradosso EPR, proposta da David Bohm, si basa su un sistema di due particelle a spin $\frac{1}{2}$ preparate in uno stato con spin totale nullo. Le fonti fornite espongono rigorosamente l'algebra alla base di tale configurazione.

Considerando due particelle di spin $\frac{1}{2}$ ($s_1 = s_2 = \frac{1}{2}$), lo spin totale del sistema è:

$$\vec{S} = \vec{S}_1 + \vec{S}_2$$ 

I possibili autovalori per il momento angolare totale $s$ obbediscono alla regola $|s_1 - s_2| \leq s \leq s_1 + s_2$ consentendo in questo caso solo due valori di spin totale per il sistema:

$$s = 0, 1$$ 

Lo spazio di Hilbert complessivo ha dimensione $(2s_1 + 1)(2s_2 + 1) = 2 \times 2 = 4$. I vettori di base del prodotto tensoriale (stati non-entangled) per le singole proiezioni sull'asse $z$ sono:

$$|++\rangle, \quad |+-\rangle, \quad |-+\rangle, \quad |--\rangle$$ 

Per transire alla base del momento angolare totale accoppiato (dove $S^2$ e $S_z$ sono diagonali, fornendo i numeri quantici $s$ e $m$), si applicano gli operatori a scala $\vec{S}_\pm = \vec{S}_{1\pm} + \vec{S}_{2\pm}$ per derivare i coefficienti di Clebsch-Gordan. Le configurazioni si suddividono in due multipletti:

**1. Il Tripletto ($s=1$):**
Stati simmetrici rispetto allo scambio delle due particelle, massimamente o parzialmente entangled:
$$|1, 1\rangle = |++\rangle$$ 
$$|1, 0\rangle = \frac{1}{\sqrt{2}} \left( |+-\rangle + |-+\rangle \right)$$ 
$$|1, -1\rangle = |--\rangle$$ 

**2. Il Singoletto ($s=0$):**
È l'autostato di spin totale nullo. Questo vettore è antisimmetrico rispetto allo scambio delle particelle, risultando isotropo e ortogonale a tutti gli stati del tripletto. Derivandolo matematicamente, si ottiene:

$$|0, 0\rangle = \frac{1}{\sqrt{2}} \left( |+-\rangle - |-+\rangle \right)$$ 

Questo è lo *stato puro EPR-Bohm per eccellenza*. Se una misurazione selettiva viene effettuata sulla prima particella tramite un filtro di Stern-Gerlach (misurando ad esempio la proiezione $S_{1z}$) e fornisce l'autovalore $+ \frac{\hbar}{2}$ (corrispondente all'autostato $|+\rangle$ ), la conservazione del momento angolare totale e il collasso della funzione d'onda obbligano istantaneamente lo stato della seconda particella a ridursi a $|-\rangle$ (corrispondente all'autovalore $- \frac{\hbar}{2}$), indipendentemente dalla separazione spaziale macroscopica tra i due rivelatori. 

## Correlazioni e Non-Località: Operatori Incompatibili
Il paradosso risalta maggiormente esaminando grandezze incompatibili. In accordo con il principio di indeterminazione generalizzato formulato su operatori non commutanti, se due operatori soddisfano la disuguaglianza $[A, B] \neq 0$ le grandezze fisiche corrispondenti non possono avere simultaneamente valori determinati. 

Nell'algebra di Pauli per particelle a spin $\frac{1}{2}$, le componenti spaziali dello spin anticommutano e commutano in forma ciclica:
$$[\sigma_i, \sigma_j] = 2 i \epsilon_{ijk} \sigma_k \quad \Rightarrow \quad [S_x, S_y] = i\hbar S_z$$ 
Portando alla relazione di indeterminazione per lo spin:
$$\langle (\Delta S_x)^2 \rangle \langle (\Delta S_y)^2 \rangle \geq \frac{\hbar^2}{4} \langle S_z \rangle^2$$ 

Se un osservatore sceglie di misurare $S_{1x}$ al posto di $S_{1z}$ sulla prima particella dello stato di singoletto, egli non apprende nulla su $S_{2z}$, ma, data l'invarianza per rotazioni dello stato di singoletto $|0,0\rangle$, ridurrà lo stato del sistema in modo da determinare istantaneamente il valore di $S_{2x}$ sull'altra particella in maniera perfettamente anti-correlata. Nessuna "variabile nascosta" codificata in fase di interazione può riprodurre le previsioni matematiche corrette che intercorrono tra le combinazioni di misurazioni spazialmente distanziate; ciò è inoppugnabilmente sancito dalla violazione delle disuguaglianze di Bell citate nel testo originale.