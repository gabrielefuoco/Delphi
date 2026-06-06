# Delphi Academic Engine - Agent Guidelines

Benvenuto in Delphi, il motore di generazione accademica. 
Questo file serve come "Punto di Ingresso" (Entrypoint) per l'agente.

Sei in una directory di progetto (o nella root) di **Delphi**. Ogni volta che operi in questo repository o ricevi richieste per creare "dispense", "libri", "ricerche" o progetti accademici completi, **DEVI obbligatoriamente** consultare il manuale principale della skill prima di iniziare:

**Path del manuale operativo:**
`C:\Users\gabri\.gemini\config\skills\delphi-academic\SKILL.md`

### Regole Base Immediate:
1. Usa **sempre** il tool `view_file` per leggere la skill menzionata sopra non appena ti viene assegnato un task in Delphi.
2. Rispetta rigorosamente i 5 Step del Workflow delineati nella skill (Init -> Fetch -> Setup -> Generate -> Export).
3. Non creare mai file Markdown "sciolti" fuori dalla gerarchia di progetto che inizializzi con `delphi init`.
4. Affidati esclusivamente a `delphi fetch` (non ad altre skill esterne) per raccogliere fonti letterarie da Z-Library, curandoti di usare chiavi di ricerca in lingua inglese.
