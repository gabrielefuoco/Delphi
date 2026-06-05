## Rotazioni e Definizione dell'Operatore Momento Angolare
Nella Meccanica Quantistica, il momento angolare è introdotto in stretta analogia con la meccanica analitica classica, assurgendo al ruolo di **generatore delle rotazioni spaziali** infinitesime. 

Se indichiamo con $D_{\hat{n}}(d\phi)$ l'operatore unitario che induce una rotazione di un angolo infinitesimo $d\phi$ attorno a un asse caratterizzato dal versore $\hat{n}$, la definizione quantistica dell'operatore momento angolare $\vec{J}$ è data dalla relazione:
$$D_{\hat{n}}(d\phi) = 1 - \frac{i}{\hbar} \vec{J} \cdot \hat{n} d\phi$$.

Una rotazione finita di un angolo $\varphi$ attorno, per esempio, all'asse $z$, si ottiene mediante l'applicazione successiva di rotazioni infinitesime, portando alla forma esponenziale:
$$D_z(\varphi) = \lim_{N\to\infty} \left( 1 - \frac{i}{\hbar} J_z \frac{\varphi}{N} \right)^N = e^{-\frac{i}{\hbar} J_z \varphi}$$.

### Regole di Commutazione Fondamentali
Un aspetto cruciale dello spazio tridimensionale è la non commutatività delle rotazioni lungo assi differenti. Matematicamente, questo implica che:
$$[D_x(\pi/2), D_z(\pi/2)] \neq 0$$.
Espandendo le matrici di rotazione spaziale $R_x, R_y, R_z$ fino al secondo ordine in un angolo infinitesimo $\epsilon$ e valutando il commutatore $R_x(\epsilon)R_y(\epsilon) - R_y(\epsilon)R_x(\epsilon)$, si osserva che esso coincide con $R_z(\epsilon^2) - 1$. Richiedendo che la medesima algebra sia rispettata dagli operatori quantistici su un generico vettore di stato si deduce la relazione fondamentale:
$$[J_x, J_y] = i\hbar J_z$$.
Tramite permutazioni cicliche, si ottengono le **regole di commutazione canoniche del momento angolare**:
$$[J_i, J_j] = i\hbar \varepsilon_{ijk} J_k$$.
Queste regole dimostrano che le tre componenti del momento angolare sono grandezze incompatibili e non possono assumere simultaneamente valori determinati.

Si definisce inoltre l'operatore corrispondente al **quadrato del momento angolare**:
$$J^2 = J_x^2 + J_y^2 + J_z^2$$.
Utilizzando le regole (14.23), è banale dimostrare che l'operatore $J^2$ commuta con ogni componente $J_k$:
$$[J^2, J_k] = 0 \quad (k = 1, 2, 3)$$.

## Spettro e Autovalori di $J^2$ e $J_z$
Dal momento che $[J^2, J_z] = 0$, è possibile determinare una base di autostati simultanei, che indicheremo con $|a, b\rangle$, tali che:
$$J^2 |a, b\rangle = a |a, b\rangle$$
$$J_z |a, b\rangle = b |a, b\rangle$$.

Per derivare i valori ammissibili di $a$ e $b$, si introducono gli **operatori a scala** (o operatori di innalzamento e abbassamento):
$$J_{\pm} = J_x \pm iJ_y$$.
Essi soddisfano le relazioni:
$$[J_z, J_{\pm}] = \pm \hbar J_{\pm}$$
$$[J^2, J_{\pm}] = 0$$.
Applicando $J_z$ allo stato $J_{\pm}|a, b\rangle$, si ottiene:
$$J_z (J_{\pm} |a, b\rangle) = (b \pm \hbar) (J_{\pm} |a, b\rangle)$$.
Questo implica che l'operatore $J_{\pm}$ trasforma l'autostato in un nuovo autostato avente lo stesso autovalore $a$ per $J^2$, ma con autovalore $J_z$ traslato di $\pm \hbar$.

Tuttavia, poiché l'operatore $J^2 - J_z^2 = J_x^2 + J_y^2$ è un operatore definito positivo, gli autovalori devono rispettare il vincolo $b^2 \leq a$. Esiste pertanto un autovalore massimo $b_{MAX}$ e un autovalore minimo $b_{MIN}$ tali per cui la scala deve arrestarsi:
$$J_+ |a, b_{MAX}\rangle = 0 \quad \text{e} \quad J_- |a, b_{MIN}\rangle = 0$$.
Sfruttando l'identità operatoriale $J_- J_+ = J^2 - J_z^2 - \hbar J_z$ (e la sua simmetrica), si deduce che:
$$b_{MAX}(b_{MAX} + \hbar) = a \quad \text{e} \quad b_{MIN}(b_{MIN} - \hbar) = a$$.
Da cui segue necessariamente che $b_{MIN} = -b_{MAX}$. Poiché lo stato di massimo si ottiene applicando $n$ volte $J_+$ allo stato di minimo, avremo $b_{MAX} = -b_{MAX} + n\hbar$, portando alla quantizzazione del momento angolare:
$$b_{MAX} = \frac{n}{2} \hbar \quad \text{(con } n \text{ intero)}$$.

Adottando la notazione convenzionale $j = b_{MAX}/\hbar$ e $b = m\hbar$, possiamo riscrivere le equazioni agli autovalori:
$$J^2 |j, m\rangle = \hbar^2 j(j+1) |j, m\rangle$$
$$J_z |j, m\rangle = \hbar m |j, m\rangle$$.
Qui, $j$ assume i valori $0, 1/2, 1, 3/2 \dots$ ed $m$ è compreso in intervalli di unità tra $-j$ e $j$.
Gli elementi di matrice per gli operatori a scala, scelti con fase reale positiva, risultano:
$$J_{\pm} |j, m\rangle = \hbar \sqrt{j(j+1) - m(m \pm 1)} |j, m \pm 1\rangle$$.

## Il Momento Angolare Orbitale $\vec{L}$
Per una particella priva di spin, il momento angolare coincide con il **momento angolare orbitale**, definito in analogia con la fisica classica:
$$\vec{L} = \vec{x} \wedge \vec{p}$$.
L'algebra di commutazione $[L_i, L_j] = i\hbar \varepsilon_{ijk} L_k$ segue banalmente dalle parentesi di commutazione tra posizione e impulso $[x_i, p_j] = i\hbar \delta_{ij}$.

Passando alla rappresentazione delle coordinate sferiche $(r, \theta, \phi)$, l'operatore proiezione $L_z$ assume la forma puramente differenziale:
$$L_z = -i\hbar \frac{\partial}{\partial \phi}$$.
Allo stesso modo, l'operatore $L^2$ coincide a meno di un fattore con la parte angolare del Laplaciano $\nabla^2$:
$$L^2 = -\hbar^2 \left[ \frac{1}{\sin^2\theta}\frac{\partial^2}{\partial \phi^2} + \frac{1}{\sin\theta}\frac{\partial}{\partial \theta}\left(\sin\theta\frac{\partial}{\partial \theta}\right) \right]$$.

Gli autostati simultanei di $L^2$ e $L_z$ nella rappresentazione delle coordinate sono le **armoniche sferiche** $Y_{l,m}(\theta, \phi) = \langle \theta, \phi | l, m\rangle$. 
La condizione di monodromia della funzione d'onda, specificamente la dipendenza $e^{im\phi}$ impone una restrizione cruciale rispetto al caso generale trattato prima: **per il momento angolare orbitale, $l$ ed $m$ possono assumere esclusivamente valori interi**.
La dipendenza zenitale $\theta$ è data dai Polinomi di Legendre associati $P_l^m(\cos\theta)$. 
Sotto operazione di parità (inversione spaziale $\vec{x} \to -\vec{x}$), le armoniche sferiche trasformano con l'autovalore $(-1)^l$:
$$P|l, m\rangle = (-1)^l|l, m\rangle$$.

## Spin $\vec{S}$ e Formalismo di Pauli
L'esperimento di Stern-Gerlach evidenzia come le particelle posseggano un momento angolare intrinseco, lo **Spin**, non derivabile da moti nello spazio ordinario. Lo spin svanisce nel limite classico ($\hbar \to 0$).

Gli operatori di spin rispettano le medesime relazioni canoniche $[S_i, S_j] = i\hbar \varepsilon_{ijk} S_k$. Gli autovalori di $S^2$ sono dati da $\hbar^2 s(s+1)$, dove $s$ può essere intero o semintero. La funzione d'onda spaziale deve allora essere espansa per includere la variabile discreta di spin, formando un vettore colonna detto **spinore** a $2s+1$ componenti.

### Particelle a Spin 1/2
Per fermioni come l'elettrone, ove $s=1/2$, gli operatori vettoriali $\vec{S}$ sono convenientemente scritti utilizzando le matrici di dimensione $2\times2$ introdotte da Pauli :
$$\vec{S} = \frac{\hbar}{2}\vec{\sigma}$$.
Dove:
$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$.
Tali matrici sono caratterizzate dalla relazione algebrica:
$$\sigma_i \sigma_j = \delta_{ij} + i \varepsilon_{ijk} \sigma_k$$ 
che codifica le relazioni sia di commutazione $[ \sigma_i, \sigma_j ] = 2i\varepsilon_{ijk}\sigma_k$ che di anticommutazione $\{ \sigma_i, \sigma_j \} = 2\delta_{ij}$. 
Gli stati di base in cui $S_z$ è diagonale sono rappresentati banalmente dagli spinori vettoriali costanti:
$$|+\rangle \doteq \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |-\rangle \doteq \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$.

## Composizione dei Momenti Angolari
Per un sistema composto da due parti (o un'unica particella con momento angolare orbitale e di spin), si definisce l'operatore momento angolare totale $\vec{J}$:
$$\vec{J} = \vec{J}_1 + \vec{J}_2 \quad \text{ovvero} \quad \vec{J} = \vec{L} + \vec{S}$$.

Passare dalla base disaccoppiata $|j_1, j_2, m_1, m_2\rangle$ (che diagonalizza simultaneamente $J_1^2, J_2^2, J_{1z}, J_{2z}$) alla base accoppiata $|j, m, j_1, j_2\rangle$ (che diagonalizza $J^2, J_z, J_1^2, J_2^2$) implica l'utilizzo di coefficienti di trasformazione unitaria denominati **Coefficienti di Clebsch-Gordan**:
$$|j, m, j_1, j_2\rangle = \sum_{m_1, m_2} |j_1, j_2, m_1, m_2\rangle \langle j_1, j_2, m_1, m_2 | j, m, j_1, j_2 \rangle$$.
Tali coefficienti sono non-nulli unicamente in virtù delle regole di selezione spaziali:
$$m = m_1 + m_2$$
$$|j_1 - j_2| \leq j \leq j_1 + j_2$$.

### Composizione di Due Spin 1/2: Singoletto e Tripletto
Se consideriamo due particelle identiche di spin 1/2 ($s_1 = s_2 = 1/2$), i possibili valori per il momento angolare totale $S$ sono esclusivamente $0$ o $1$.
Nella base disaccoppiata abbiamo 4 stati: $|++\rangle, |+-\rangle, |-+\rangle, |--\rangle$.
Tramite ripetute applicazioni dell'operatore $S_- = S_{1-} + S_{2-}$ ed imposizione della condizione di ortogonalità, si perviene alla decomposizione nei 4 stati accoppiati :

**Stati di Tripletto ($s=1$, simmetrici per scambio):**
$$|1, 1\rangle = |++\rangle$$
$$|1, 0\rangle = \frac{1}{\sqrt{2}}(|++\rangle + |-+\rangle)$$
$$|1, -1\rangle = |--\rangle$$.

**Stato di Singoletto ($s=0$, antisimmetrico per scambio):**
$$|0, 0\rangle = \frac{1}{\sqrt{2}}(|+-\rangle - |-+\rangle)$$.
La natura intrinseca di simmetria o antisimmetria di tali combinazioni spinoriali sarà determinante, mediante il **Principio di Pauli**, per definire i livelli quantistici ammissibili per fermioni multifunzione.