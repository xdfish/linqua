# frontend

Das Frontend ist lediglich für die Visualisierung der Anwendung für den Benutzer über einen Brwoser (als webapp) zuständig. Alle Endpunkt können theoretisch auch ohne das Frontend betrieben werden, logische Abläufe/Vorgaben kommen ausschließlich vom Backend.
Eine Anbindung einer Desktopanwendung oder Mobileapp wären entsprechend schnell zu implementieren.
Das Frontend wurde mit Vue.js entwickelt und verwendet u.A. das nodejs package vuetify für eine ansprechendere visualisierung.


## Hinweis
Bei OSX und Windows muss die Umgebungsvariable NODE_OPTIONS mit folgendem Wert gesetzt sein --openssl-legacy-provider

Ausführlichere Hinweise finden sich in der Projekt [README](../README.md)

```bash
export NODE_OPTIONS=--openssl-legacy-provider
```

## Vue und NPM spezfische Entwicklungsanweisungen

### NPM Project setup
```
npm install
```

### NPM Compiles and hot-reloads for development
```
npm run serve
```

### NPM/Vue Compiles and minifies for production
```
npm run build
```

### NPM/Vue Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
