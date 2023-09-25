# Linqua Backend

Neben Systemfunktionalitäten wie Userverwaltung, Sessionmanagement etc. bietet das Backend mehrer Klassen um die sprachtechnologischen Anfprderungen zu erfüllen. Im Wesentlichen handelt es sich hierbei um folgende Module:

### Wortdatenbank ([words.py](server/server/words.ipynb))
Die Wortdatenbank bietet Möglichkeitne um die SUBTLEX datei in eine Wortdatenbank umzuwalnden und bitetet Funktionen um auf die Wörter zuzugreifen.

Im [jupyter notebook](example/words.ipynb) wird die zentrale Funktionalität der Wortdatenbank, welche für die auomatische Aufgabengenerierung zuständig ist, Schritt für Schritt erklärt.
Das Notebook ist bereits ausgeführt, kann aber Zellenweise nue ausgeführt werden.


### Sprache ([speech.py](server/server/speech.ipynb))
Die Klasse "Speech" wird mit einer Audioaufnahme initialisiert und bietet Funktionen zu Auswertung. So z.B. die gesprochenen Worte in form eines Strings und verschiedene Konvertierungsmethoden.

### Aufgaben ([task.py](server/server/speech.ipynb))
Als Basisklasse dient "Task" für alle Aufgabenarten und stellt sicher, dass grundlegende Funktionalitäten angeboten werden. So z.B der Score für eine Aufgabe oder die Fenerierung / Auswahl einer Aufgabe des bestimmten Typs.
Aktuell sind folgende Aufgabenarten implementiert:

1. Describe ([taskDescribe.py](server/server/taskDescribe.ipynb)) !DECPRECATED!
2. Talk ([taskTalk.py](server/server/taskTalk.ipynb))
3. TalkAuto ([taskTalkAuto.py](server/server/taskTalkAuto.ipynb))