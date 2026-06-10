
Quando si costruisce un modello per spiegare una variabile dipendente attraverso un insieme di variabili esplicative, è comune ipotizzare che gli errori, e di conseguenza la variabile dipendente, seguano una distribuzione Normale. 
In questi casi, si utilizza una classe di modelli che generalizza il modello lineare gaussiano precedentemente discusso: i **Modelli Lineari Generalizzati**.

Siano $y_i$ e $x_i$, $i=1,...,n$, le $n$ osservazioni sulla variabile dipendente $Y$ e su $k$ variabili esplicative. Per costruire un Modello Lineare Generalizzato bisogna **specificare** le seguenti componenti:

1.  Distribuzione della componente casuale
    $$Y_i \sim f(y_i; \theta_i, \phi) = \exp\left\{\frac{y_i \theta_i - b(\theta_i)}{a(\phi)} + c(y_i; \phi)\right\}$$
    Dipendente dal fenomeno oggetto di studio e, di conseguenza, dalla natura della variabile casuale $Y$ che interpreta tale fenomeno.
    $Y$ può essere **quantitativa** oppure **qualitativa** (in tal caso viene discretizzata).

2.  Componente sistematica (predittore lineare)
    $$\eta_i = \mathbf{x}_i^t \boldsymbol{\beta} = \beta_0 + x_{i1}\beta_1 + ... + x_{ij}\beta_j + ... + x_{ik}\beta_k \quad i=1,...,n$$

3.  Funzione link tra la media e il predittore lineare
    $$g(\mu_i) = \eta_i \quad i=1,...,n$$

Utilizzando il metodo della massima verosimiglianza, si stimano i coefficienti di regressione $\boldsymbol{\beta}$.
Alla famiglia di distribuzioni $f(y; \theta, \phi)$ appartengono diverse funzioni di densità (o di probabilità) utilizzati nella modellistica statistica.
Nei casi in cui in un modello lineare generalizzato si utilizza la v.c. Normale per descrivere la variabile dipendente, il modello si riduce ad un modello lineare classico gaussiano.

In ciò che segue, studieremo il modello di regressione **Beta** che viene utilizzato per modellare variabili dipendenti continue nell'intervallo $(0,1)$. 
==Tale modello NON appartiene ai modelli lineari generalizzati, ma nella sua costruzione si sfrutta la logica sottostante i modelli lineari generalizzati.==

## Funzione di densità Beta.

Si dice che la v.c. $Y$ ha distribuzione Beta se la f.d. di $Y$ è data da:
$$f(y; p,q) = \frac{1}{B(p,q)} y^{p-1} (1-y)^{q-1}$$
per $y \in [0,1]$ con $p>0$ e $q>0$

dove $B(p,q)$ è la funzione matematica Beta così definita:
$$B(p,q) = \int_0^1 x^{p-1} (1-x)^{q-1} dx = \frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}$$
e $\Gamma(.)$ è la funzione matematica Gamma.

>[!DANGER] Osservazione
>La fd di una v.c. Beta non appartiene alla famiglia di dispersione esponenziale $f(y; \theta, \phi)$ descritta in precedenza.
>
>Conseguenza dell'osservazione: non possiamo utilizzare i risultati metodologici relativi ai Modelli Lineari Generalizzati.

Tuttavia, è semplice dimostrare che
$$E[Y] = \frac{p}{p+q} \quad \text{e} \quad V[Y] = \frac{pq}{(p+q)^2(p+q+1)}$$

Il momento di ordine $k$ è dato da
$$E[Y^k] = \int_0^1 y^k f(y; p,q)dy = \int_0^1 y^k \frac{1}{B(p,q)} y^{p-1} (1-y)^{q-1}dy = \frac{B(k+p,q)}{B(p,q)}$$

Posto $k=1$, otteniamo il momento primo
$$\begin{split}
E(Y) &= \frac{B(1+p,q)}{B(p,q)} = \frac{\frac{\Gamma(1+p)\Gamma(q)}{\Gamma(1+p+q)}}{\frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}} \\
&= \frac{\Gamma(1+p)\Gamma(q)}{\Gamma(1+p+q)} \frac{\Gamma(p+q)}{\Gamma(p)\Gamma(q)} \\
&= \frac{p\Gamma(p)\Gamma(q)}{(p+q)\Gamma(p+q)} \frac{\Gamma(p+q)}{\Gamma(p)\Gamma(q)} \\
&= \frac{p}{p+q}
\end{split}$$

Posto $k=2$ nel momento di ordine $k$, otteniamo il momento secondo
$$\begin{split}
E[Y^2] &= \frac{B(2+p,q)}{B(p,q)} \\
&= \frac{\frac{\Gamma(2+p)\Gamma(q)}{\Gamma(2+p+q)}}{\frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}} \\
&= \frac{\Gamma(2+p)\Gamma(q)}{\Gamma(2+p+q)} \frac{\Gamma(p+q)}{\Gamma(p)\Gamma(q)} \\
&= \frac{(1+p)p\Gamma(p)\Gamma(q)}{(1+p+q)(p+q)\Gamma(p+q)} \frac{\Gamma(p+q)}{\Gamma(p)\Gamma(q)} \\
&= \frac{(1+p)p}{(1+p+q)(p+q)}
\end{split}$$

Di conseguenza, la **varianza** è data da:
$$\begin{split}
V(Y) &= E[Y^2] - E(Y)^2 \\
&= \frac{(1+p)p}{(1+p+q)(p+q)} - \frac{p^2}{(p+q)^2} \\
&= \frac{p}{p+q} \left\{ \frac{1+p}{1+p+q} - \frac{p}{p+q} \right\} \\
&= \frac{pq}{(p+q)^2(1+p+q)}
\end{split}$$

**Osservazione:**
$$\begin{split}
\frac{\partial f(y; p,q)}{\partial y} &= \frac{1}{B(p,q)} y^{p-2} (1-y)^{q-2} \{(p-1)(1-y) - (q-1)y\} \\
&= 0 \Leftrightarrow y = \frac{p-1}{p+q-2} = y_m
\end{split}$$

## Flessibilità

La funzione di densità della v.c. Beta presenta una forma molto flessibile:

-   Se $p=q$, la densità è **simmetrica**, in particolare se $p=q=1$ la v.c. Beta si riduce ad una v.c. Uniforme in $(0,1)$
-   Se $p>q$, la densità è **asimmetrica negativa**
-   Se $p<q$, la densità è **asimmetrica positiva**

## Riparametrizzazione

La riparametrizzazione che effettueremo di seguito, ci consente di esprimere la densità in funzione di un parametro ($\mu$) che identifica la media.

Poniamo
$$\begin{cases} \mu = E[Y] = \frac{p}{p+q} \\ \phi = p+q \end{cases}$$
risolviamo il sistema rispetto a $p$ e $q$
$$\begin{cases} \mu = E[Y] = \frac{p}{p+q} \\ \phi = p+q \end{cases} \Rightarrow \begin{cases} p = \frac{\mu}{1-\mu} q \\ q = \phi-p \end{cases} \Rightarrow \begin{cases} p = \mu\phi \\ q = \phi(1-\mu) \end{cases}$$

Sostituendo i valori di $p$ e $q$ nella funzione di densità della v.c. Beta, otteniamo una Riparametrizzazione della densità Beta, cioè
$$f(y; \mu, \phi) = \frac{1}{B(\mu\phi, \phi(1-\mu))} y^{\mu\phi-1} (1-y)^{\phi(1-\mu)-1}$$
con $y \in [0,1]$, $\mu \in [0,1]$ e $\phi > 0$.

È semplice verificare che
$$E[Y] = \mu \quad \text{e} \quad V[Y] = \frac{\mu(1-\mu)}{1+\phi}$$

- Il parametro $\mu$ è un parametro di **locazione**, in particolare è la media di $Y$.
- Il parametro $\phi$ è un parametro di **precisione** (dispersione), nel senso che quando aumenta diminuisce la varianza.

## Inferenza

La funzione di verosimiglianza per un campione $Y_1, ..., Y_n$ estratto da $f(y; \mu, \phi)$ è:
$$L(\mu, \phi; \mathbf{y}) = \prod_{i=1}^n \left\{ \frac{1}{B(\mu_i\phi, \phi(1-\mu_i))} y_i^{\mu_i\phi-1} (1-y_i)^{\phi(1-\mu_i)-1} \right\}$$

Per studiare le variazioni della media di $Y$ in funzione di regressori, si specifica la media come:
$$\mu_i = h(\mathbf{x}_i^t \boldsymbol{\beta})$$
Se esiste la funzione inversa $g() = h^{-1}()$, la funzione link è:
$$g(\mu_i) = \mathbf{x}_i^t \boldsymbol{\beta} = \eta_i$$
Poiché $\mu_i$ deve essere compreso tra 0 e 1, la funzione link deve garantire che la sua contro-immagine rientri in questo intervallo. Le funzioni link comuni sono logit, probit e log-log complementare.

La regressione Beta è intrinsecamente eteroschedastica, con varianza:
$$V[Y_i] = \frac{\mu_i(1-\mu_i)}{1+\phi} = \frac{g^{-1}(\mathbf{x}_i^t \boldsymbol{\beta})[1-g^{-1}(\mathbf{x}_i^t \boldsymbol{\beta})]}{1+\phi}$$

Estensioni del modello possono includere un modello regressivo anche per il parametro di dispersione $\phi$:
$$\begin{cases} g_1(\mu_i) = \eta_{1i} = \mathbf{x}_i^t \boldsymbol{\beta} \\ g_2(\phi_i) = \eta_{2i} = \mathbf{z}_i^t \boldsymbol{\gamma} \end{cases}$$

---

### Funzione di densità Gamma.

Si dice che la v.c. $X$ ha distribuzione Gamma se la f.d. di $X$ è data da:
$$f(x; a, \lambda) = \frac{\lambda}{\Gamma(a)} (\lambda x)^{a-1} e^{-\lambda x}$$
Verrà indicata con $G(a, \lambda)$.
per $x > 0$ con $a>0$ e $\lambda > 0$
dove
$$\Gamma(a) = \int_0^\infty w^{a-1} e^{-w} dw$$
è la funzione matematica Gamma.

$$E[X] = \frac{a}{\lambda} \quad V[X] = \frac{a}{\lambda^2}$$
---
### Funzione di densità Esponenziale (negativa).

Si dice che la v.c. $X$ ha distribuzione Esponenziale se la f.d. di $X$ è data da:
$$f(x; \lambda) = \lambda e^{-\lambda x}$$
Verrà indicata con $E(\lambda)$.
per $x > 0$ con $\lambda > 0$

>[!NOTE] Osservazione
>Se nella fd Gamma si pone $a=1$ si ottiene la fd Esponenziale. Cioè $E(\lambda)=G(1, \lambda)$

$$E[X] = \frac{1}{\lambda} \quad V[X] = \frac{1}{\lambda^2}$$

---

### Alcune funzioni link più usate in letteratura

**1) Funzione logit**

La funzione link più usata è la **funzione logit**, la quale assume la seguente forma
$$g(\mu_i) = \ln\left(\frac{\mu_i}{1-\mu_i}\right) = \ln\left(\frac{\pi_i}{1-\pi_i}\right) = \mathbf{x}_i^t \boldsymbol{\beta}$$
Invertendo la funzione $g(.)$ otteniamo la media ovvero la funzione $h(.)$
$$\mu_i = \pi_i = \frac{\exp\{\mathbf{x}_i^t \boldsymbol{\beta}\}}{1+\exp\{\mathbf{x}_i^t \boldsymbol{\beta}\}}$$

**2) Funzione probit** (contrazione di "probability unit")

È usata la cosiddetta **funzione probit**, che è del tipo:
$$g(\pi_i) = \Phi^{-1}(\pi_i) = \mathbf{x}_i^t \boldsymbol{\beta}$$
dove $\Phi(.)$ è la funzione di ripartizione della v.c. normale standardizzata $N(0,1)$.
Invertendo la funzione $g(.)$ otteniamo la media ovvero la funzione $h(.)$
$$\pi_i = \Phi(\mathbf{x}_i^t \boldsymbol{\beta})$$

**3) Funzione doppio-logaritmo**

In letteratura sono utilizzate le funzioni doppio-logaritmo, definite nel seguente modo:
$$g(\pi_i) = \ln[-\ln(1-\pi_i)] = \mathbf{x}_i^t \boldsymbol{\beta}$$
con inversa
$$\pi_i = 1-\exp\{-\exp(\mathbf{x}_i^t \boldsymbol{\beta})\}$$

**4) Funzione identità**
$$g(\mu_i) = \mu_i = \mathbf{x}_i^t \boldsymbol{\beta}$$

**5) Funzione logaritmo**
$$g(\mu_i) = \ln(\mu_i) = \mathbf{x}_i^t \boldsymbol{\beta}$$
