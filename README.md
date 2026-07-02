# Grid Flood Fill PoC

![Grid Demo](demo.png)

**Live Demo:** [PascalHberg.github.io/Perkolation](https://PascalHberg.github.io/Perkolation)

Dieses Projekt ist eine einfache Python-Tkinter-Anwendung zur Visualisierung eines Grids mit zufälliger Initialisierung über eine prozentuale Dichte.

Der Benutzer kann die Dichte zwischen 1.00 und 100.00 einstellen, auch mit Dezimalstellen oder Komma-Eingabe. Die Eingabe wird intern normalisiert.

Per Klick auf eine schwarze Zelle wird eine zusammenhängende Fläche sofort rot eingefärbt. Die Ausbreitung erfolgt über eine 4-Richtungs-Verbindung ohne diagonale Nachbarschaft.

Ein Reset stellt nur die ursprüngliche Farbverteilung wieder her, ohne die aktuellen Einstellungen zu verändern.

## Features

- Dynamisches Grid (25x25)
- Zufällige Initialisierung über Prozentwert
- Live-Slider für Dichte (1.00 – 100.00)
- Manuelle Eingabe mit Komma oder Punkt
- Synchronisation zwischen Slider und Eingabefeld
- Klick-basierte Flood-Fill-Funktion
- Sofortige Ausbreitung ohne Animation
- Reset ohne Verlust der Einstellungen
- Robuste Eingabevalidierung

Das Projekt dient als Proof of Concept für Grid-Logik, Flood-Fill-Algorithmen und einfache UI-Interaktion mit Tkinter.
