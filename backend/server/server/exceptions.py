class LinquaExceptions:
    #Unbekannter Benutzer
    class UserUnknown(Exception):
        ...
    #Benutzer existiert bereits
    class UserAlreadyExists(Exception):
        ...
    #Aufgabe nicht bekannt
    class TaskUnknown(Exception):
        ...
    #Falsche Aufgaben Klasse
    class WrongTaskClass(Exception):
        ...

