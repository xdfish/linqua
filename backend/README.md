# Warum haben wir uns für das SUBTLEX_US Lexikon entschieden?

Um unsere App zu Testen und die Funktionen zu evaluieren, benötigten wir einen Datensatz mit Wörtern, welche POS kategorisiert,  und mit Häufigkeitswerten versehen sind. Dieser Datensatz besitzt sehr viele Wörter und erfüllte unsere Kriterien. Andere frei verfügbare Datensätze sind bei weitem nicht so umfangreich oder es wurden unsere Anforderungen nicht erfüllt.

___
# Anleitung zum Starten des Backends auf einem UNIX System
## Voraussetzung 
Installiert sein muss:
1. Zip / Unzip
2. Docker
3. Python 3

## Initialisierung der Umgebung
 Mit dem Befehl `bash run.sh setup` wird das Sprachmodell für die Speech-to-Text (STT) Verarbeitung heruntergeladen und entpackt

## Entwicklungsumgebung 
Mit dem Befehl `bash run.sh dev` wird der Development Modus aktiviert. In diesem Modus ist der Inhalt der Datenbank **nicht** persistent gesichert.

## Produktionsumgebung
Mit dem Befehl `bash run.sh prod` wird der produktive Modus aktiviert. In diesem Modus wird der Inhalt der Datenbank unter `./server/database/` persistent gesichert.

___
Durch ausführen des Shell Skriptes ohne ein Argument, werden die 3 Modi erklärt.
`bash run.sh`