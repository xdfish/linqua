# Linqua Backend

Neben Systemfunktionalitäten wie Userverwaltung, Sessionmanagement etc. bietet das Backend mehrere Klassen um die sprachtechnologischen Anforderungen zu erfüllen. Im wesentlichen handelt es sich hierbei um folgende Module:

### Wortdatenbank ([words.py](server/server/words.ipynb))
Die Wortdatenbank bietet Möglichkeiten um die SUBTLEX Datei in eine Wortdatenbank umzuwandeln, diese anschließend in der MongoDB abzuspeichern und stellt Funktionen bereit um auf sie zuzugreifen.

Im [jupyter notebook](example/words.ipynb) wird die zentrale Funktionalität der Wortdatenbank, welche für die auomatische Aufgabengenerierung verwendet wird, Schritt für Schritt erklärt.
Das Notebook ist bereits ausgeführt, kann aber mit der im Ordner bereitgestellten Exceldatei von SUBTLEX, Zellenweise neu ausgeführt werden.

### Sprache ([speech.py](server/server/speech.ipynb))
Die Klasse "Speech" wird mit einer Audioaufnahme initialisiert und bietet Funktionen zur Auswertung. So z.B. die gesprochenen Worte in Form eines/r Strings/Liste und verschiedene Konvertierungsmethoden.

### Aufgaben ([task.py](server/server/speech.ipynb))
Als Basisklasse dient "Task" für alle Aufgabenarten und stellt sicher, dass grundlegende Funktionalitäten von den Implementierenden Klassen angeboten werden. So z.B der Score für eine Aufgabe oder die Generierung / Auswahl einer Aufgabe.
Aktuell sind folgende Aufgabenarten implementiert:

1. Describe ([taskDescribe.py](server/server/taskDescribe.ipynb)) !DECPRECATED!
2. Talk ([taskTalk.py](server/server/taskTalk.ipynb))
3. TalkAuto ([taskTalkAuto.py](server/server/taskTalkAuto.ipynb))