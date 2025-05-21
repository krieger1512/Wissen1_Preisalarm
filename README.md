# Wissen1_Preisalarm

## Problemstellung

Preisvergleichsportale im Internet ermöglichen es, den aktuell verfügbaren günstigsten Preis für ein gewünschtes Produkt genau im Auge zu behalten. Ein lernfähiger Agent soll auf Basis des beobachteten günstigsten Preises ein Produkt online erwerben. Folgende Rahmenbedingungen charakterisieren die Aufgabenstellung: 
- Der Agent kann jeden Tag die Entscheidung treffen, ob er zum tagesaktuellen Preis das Produkt kaufen möchte, oder ob er weiter warten will.
- Da das gewünschte Produkt zu einem bestimmten Zeitpunkt garantiert vorliegen soll, gibt es einen spätestmöglichen Zeitpunkt \( t_{final} \), zu dem der Agent das Produkt kaufen muss. D.h. ein weiteres Warten (auf einen günstigeren Preis) ist dann nicht mehr möglich.

- Der Preis am ersten (\( t = 1 \)) Tag sei \( \mathcal{P}_1 \in \mathbb{N} \).

- Aufgrund der auf Angebot und Nachfrage basierenden Gesetze des Marktes nehmen wir an, dass der Preis des Produkts nicht negativ werden kann und sich von Tag zu Tag wie folgt ändert:

  \[
  \mathcal{P}_{t+1} = \max(0, \mathcal{P}_t + k - \delta)
  \]

  wobei sich der Wert \( k \in \{0, \ldots, 2\delta\} \) stochastisch gemäß einer Binomialverteilung \( B(k|n,q) \) mit \( n = 2\delta \) und \( q \in [0,1] \) ergibt. Hierbei steht \( \delta \) für die maximale absolute Preisschwankung an einem Tag.

- Ziel des Agenten ist es, das Produkt zum bestmöglichen (geringsten) Preis zu kaufen. Kosten entstehen aus Sicht des Agenten also ausschließlich im Moment des Kaufes.

## Problemspezifikation
MDP = \([T, S, A, p, c]\)

### T

\(N\) diskrete Entscheidungszeitpunkte: \(T = \{1, 2, \ldots, N\}\) (Problem mit endlichem Horizont)

### A

Aktionsmenge: \(A = \{k, w\}\) 

- \(k\) = kaufen; \(w\) = warten
- \(A\) ist endlich.

### S
Zustandsmenge:


\(S = \{(t,  \mathcal{P}_{t}) \mid t \in T; \forall t \in T, t \geq 2: \mathcal{P}_{t+1} = \max(0, \mathcal{P}_t + k - \delta))\} \cup \{"0"\} \)


- \(k \in \{0, \ldots, 2\delta\}, k \sim B(k \mid 2\delta, q), q \in [0,1]\)
- "0" ist ein Terminalzustand mit folgenden Eigenschaften:
  - "0" ist absorbierend (wird nicht mehr verlassen).
  - Es fallen in ihm keine Kosten mehr an.
- Umgangssprachlich: Mit Ausnahme vom Terminalzustand, jeder Zustand stellt einen Tag im Beobachtungszeitraum und einen möglichen Preis vom Produkt am Tag dar.
- \(S\) ist endlich, denn \(T\) ist endlich und \(k\) ist beschränkt. 




