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