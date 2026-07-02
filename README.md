# 🔗 Perkolationsphänomen

## Marco-Polo Schwelle auf zweidimensionalen Gittern

**Live Demo:** [PascalHberg.github.io/Perkolation](https://PascalHberg.github.io/Perkolation)

### 📋 Beschreibung

Dieses Projekt visualisiert das **Perkolationsphänomen** mit Fokus auf die **Marco-Polo Schwelle** (59.2746050792%). Die Perkolationstheorie beschäftigt sich mit der Frage, ab welcher kritischen Dichte in einem zweidimensionalen Gitter eine durchgehende Verbindung (Perkolation) vom einen zum anderen Ende entsteht.

### 🎯 Die Marco-Polo Schwelle

Die **Marco-Polo Schwelle** oder **percolation threshold** bei ~59.27% ist der kritische Punkt, bei dem auf einem unendlichen zweidimensionalen quadratischen Gitter eine Perkolation mit einer Wahrscheinlichkeit von 50% auftritt. Diese Konstante ist von großer Bedeutung in:

- **Physik**: Perkolation in Materialien
- **Netzwerktheorie**: Ausbreitung von Infektionen oder Informationen
- **Hydrologie**: Flüssigkeitsfluss durch poröse Medien
- **Mathematik**: Kritische Phänomene und Phasenübergänge

### ✨ Funktionen

- 🎨 **Interaktive Visualisierung**: Echtzeit-Rendering auf HTML5 Canvas
- 🎚️ **Dichte-Slider**: Passen Sie die Gitterdichte an (1-100%)
- 🖱️ **Flood Fill**: Klicken Sie auf schwarze Zellen, um zusammenhängende Regionen hervorzuheben
- 📊 **Echtzeit-Statistiken**: Zeigt Gittergröße, besetzte Zellen und aktuelle Dichte
- 🔄 **Dynamisch**: Generieren Sie neue Perkolationsmuster auf Knopfdruck
- 📱 **Responsiv**: Funktioniert auf Desktop und mobilen Geräten

### 🚀 Quick Start

1. **Lokal ausführen**:
   ```bash
   git clone https://github.com/PascalHberg/Perkolation.git
   cd Perkolation
   # Öffnen Sie index.html in Ihrem Browser
   ```

2. **Online ansehen**:
   Besuchen Sie [https://PascalHberg.github.io/Perkolation](https://PascalHberg.github.io/Perkolation)

### 🎮 Bedienung

1. **Dichte einstellen**: Verwenden Sie den Slider oder geben Sie einen Wert ein (1-100%)
2. **Neue Perkolation**: Klicken Sie auf "Neue Perkolation", um ein neues Gittermuster zu generieren
3. **Regionen erkunden**: Klicken Sie auf schwarze Zellen, um zusammenhängende Regionen rot hervorzuheben
4. **Zurücksetzen**: Klicken Sie auf "Farben zurücksetzen", um zur Originalfärbung zurückzukehren

### 📐 Technische Details

- **Gittergröße**: 25×25 Zellen (625 Gesamtzellen)
- **Zellgröße**: 20 Pixel
- **Algorithmus**: Flood Fill (Tiefensuche/DFS)
- **Nachbarschaftsmodell**: Von-Neumann-Nachbarschaft (4 direkte Nachbarn)
- **Standard-Dichte**: 59.2746050792% (Marco-Polo Schwelle)

### 🏗️ Architektur

```
.
├── index.html          # HTML-Struktur und Styling
├── perkolation.js      # Kernlogik und Canvas-Rendering
├── README.md           # Diese Datei
└── LICENSE             # MIT License
```

### 🔬 Perkolationstheorie

Das Perkolationsphänomen tritt auf, wenn:
- Auf einem unendlichen Gitter
- Mit Verbindungswahrscheinlichkeit p (Dichte)
- Eine unendliche Cluster mit Wahrscheinlichkeit > 0 existiert

Der **kritische Punkt** (percolation threshold) p_c für ein 2D quadratisches Gitter ist bekannt:
- **Theoretisch**: ≈ 0.592746 (59.2746%)
- **Experimentell**: Durch Monte-Carlo-Simulationen bestätigt

### 📚 Referenzen

- Stauffer, D., & Aharony, A. (1994). Introduction to Percolation Theory
- Broadbent, S. R., & Hammersley, J. M. (1957). Percolation processes
- [NIST - Percolation Threshold](https://www.nist.gov/)

### 👤 Über den Entwickler

**Pascal Hässenberg**
- 🔗 GitHub: [@PascalHberg](https://github.com/PascalHberg)
- 💼 LinkedIn: [pascal-hässenberg-523480332](https://www.linkedin.com/in/pascal-ha%C3%9Fenberg-523480332/)

### 📄 Lizenz

MIT License - Siehe [LICENSE](LICENSE) für Details

### 🤝 Beiträge

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue.

---

**Version**: 1.0.0  
**Aktualisiert**: 2026-07-02  
**Status**: ✅ Aktiv
