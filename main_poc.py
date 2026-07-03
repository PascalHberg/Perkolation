import tkinter as tk
from tkinter import ttk
import random

CELL_SIZE = 20
GRID_W = 25
GRID_H = 25

# Zustände für Zellen
STATE_WHITE = 0     # Freies Feld (weiß)
STATE_BLACK = 1     # Blockiertes Feld (schwarz)
STATE_RED = 2       # Rot markiert (zusammenhängend schwarz)
STATE_BLUE = 3      # Blau markiert (zusammenhängend weiß)


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Perkolation - Grid Simulator")
        
        # Hauptcontainer mit zwei Spalten: Links Info/Controls, Rechts Canvas
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # LINKE SPALTE: Info-Box und Steuerungselemente
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Statistikbereich
        self.stats_frame = ttk.LabelFrame(self.left_frame, text="Statistiken", padding=10)
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Statistik-Labels
        self.label_total = ttk.Label(self.stats_frame, text="Gesamtzahl: 0")
        self.label_total.pack(anchor=tk.W)
        
        self.label_black = ttk.Label(self.stats_frame, text="Schwarze Felder: 0")
        self.label_black.pack(anchor=tk.W)
        
        self.label_white = ttk.Label(self.stats_frame, text="Weiße Felder: 0")
        self.label_white.pack(anchor=tk.W)
        
        self.label_red = ttk.Label(self.stats_frame, text="Rote Felder: 0")
        self.label_red.pack(anchor=tk.W)
        
        self.label_blue = ttk.Label(self.stats_frame, text="Blaue Felder: 0")
        self.label_blue.pack(anchor=tk.W)
        
        # Dichte-Steuerung
        self.density_frame = ttk.LabelFrame(self.left_frame, text="Dichte-Regler", padding=10)
        self.density_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.density_frame, text="Dichte (1.00 - 100.00)").pack(fill=tk.X)
        
        self.density = tk.DoubleVar(value=50.00)
        
        # Slider mit verbesserter Bindung
        self.slider = ttk.Scale(
            self.density_frame,
            from_=1.00,
            to=100.00,
            orient=tk.HORIZONTAL,
            variable=self.density,
            command=self.on_slider_change
        )
        self.slider.pack(fill=tk.X, pady=5)
        
        # Entry-Feld für manuelle Eingabe
        self.entry = ttk.Entry(self.density_frame, width=10)
        self.entry.insert(0, "50.00")
        self.entry.pack(fill=tk.X, pady=5)
        self.entry.bind("<Return>", self.on_entry_change)
        self.entry.bind("<FocusOut>", self.on_entry_change)
        
        # Button-Frame für Buttons
        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.reset_btn = ttk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset
        )
        self.reset_btn.pack(fill=tk.X, pady=2)
        
        self.mark_free_btn = ttk.Button(
            self.button_frame,
            text="Freie Bereiche markieren",
            command=self.activate_free_area_mode
        )
        self.mark_free_btn.pack(fill=tk.X, pady=2)
        
        # Info-Text
        self.info_frame = ttk.LabelFrame(self.left_frame, text="Info", padding=10)
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(self.info_frame, height=8, width=30, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.insert(tk.END,
            "Schwarze Felder:\n"
            "Klick = Zusammenhängender\n"
            "Bereich färbt sich rot\n\n"
            "Weiße Felder:\n"
            "Button klicken, dann auf\n"
            "Feld klicken = Bereich\n"
            "färbt sich blau\n\n"
            "Slider/Feld ändern =\n"
            "Neues Gitter mit\n"
            "gegebener Dichte"
        )
        self.info_text.config(state=tk.DISABLED)
        
        # RECHTE SPALTE: Canvas
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            self.right_frame,
            width=GRID_W * CELL_SIZE,
            height=GRID_H * CELL_SIZE,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack()
        
        # Interne Variablen
        self.grid = []
        self.rects = {}
        self.free_area_mode = False  # Modus für Freie-Bereiche-Markierung
        
        # Grid initialisieren
        self.init_grid()
        self.apply_density()
        
        # Click-Handler
        self.canvas.bind("<Button-1>", self.on_click)

    def init_grid(self):
        """Initialisiert das Grid mit leeren (weißen) Zellen"""
        self.canvas.delete("all")
        self.grid = [[STATE_WHITE for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.rects = {}

        for y in range(GRID_H):
            for x in range(GRID_W):
                r = self.canvas.create_rectangle(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    (x + 1) * CELL_SIZE,
                    (y + 1) * CELL_SIZE,
                    fill="white",
                    outline="gray"
                )
                self.rects[(x, y)] = r

    def apply_density(self):
        """Wendet die Dichte auf das Grid an und generiert zufällig schwarze Felder"""
        # Density als Dezimalzahl (0-1)
        d = float(self.density.get()) / 100.0
        
        # Grid auf Anfangszustand zurücksetzen
        for y in range(GRID_H):
            for x in range(GRID_W):
                state = STATE_BLACK if random.random() < d else STATE_WHITE
                self.set_cell(x, y, state)
        
        # Statistiken aktualisieren
        self.update_stats()

    def set_cell(self, x, y, state):
        """Setzt die Farbe einer Zelle basierend auf ihrem Zustand"""
        self.grid[y][x] = state
        
        color_map = {
            STATE_WHITE: "white",
            STATE_BLACK: "black",
            STATE_RED: "red",
            STATE_BLUE: "blue"
        }
        
        color = color_map.get(state, "white")
        self.canvas.itemconfig(self.rects[(x, y)], fill=color)

    def update_stats(self):
        """Aktualisiert die Statistik-Labels"""
        total = GRID_W * GRID_H
        black = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_BLACK)
        white = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_WHITE)
        red = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_RED)
        blue = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_BLUE)
        
        self.label_total.config(text=f"Gesamtzahl: {total}")
        self.label_black.config(text=f"Schwarze Felder: {black}")
        self.label_white.config(text=f"Weiße Felder: {white}")
        self.label_red.config(text=f"Rote Felder: {red}")
        self.label_blue.config(text=f"Blaue Felder: {blue}")

    def on_click(self, event):
        """Behandelt Klicks auf das Grid"""
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if 0 <= x < GRID_W and 0 <= y < GRID_H:
            if self.free_area_mode:
                # Modus: Freie Bereiche markieren
                if self.grid[y][x] == STATE_WHITE:
                    self.paint_free_region(x, y)
                    self.free_area_mode = False
                    self.mark_free_btn.config(relief=tk.RAISED)
            else:
                # Standard-Modus: Schwarze Bereiche markieren
                if self.grid[y][x] == STATE_BLACK:
                    self.paint_black_region(x, y)
            
            self.update_stats()

    def paint_black_region(self, x, y):
        """Flood-Fill für schwarze Felder (4er-Nachbarschaft)"""
        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            if not (0 <= cx < GRID_W and 0 <= cy < GRID_H):
                continue

            if self.grid[cy][cx] != STATE_BLACK:
                continue

            self.set_cell(cx, cy, STATE_RED)

            # 4er-Nachbarschaft: oben, unten, links, rechts
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def paint_free_region(self, x, y):
        """Flood-Fill für freie (weiße) Felder (4er-Nachbarschaft)"""
        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            if not (0 <= cx < GRID_W and 0 <= cy < GRID_H):
                continue

            if self.grid[cy][cx] != STATE_WHITE:
                continue

            self.set_cell(cx, cy, STATE_BLUE)

            # 4er-Nachbarschaft: oben, unten, links, rechts
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def activate_free_area_mode(self):
        """Aktiviert den Modus zum Markieren freier Bereiche"""
        self.free_area_mode = True
        self.mark_free_btn.config(relief=tk.SUNKEN)

    def reset(self):
        """Setzt alle roten und blauen Markierungen zurück zu Ursprungszustand"""
        for y in range(GRID_H):
            for x in range(GRID_W):
                state = self.grid[y][x]
                # Umwandlung: Rot -> Schwarz, Blau -> Weiß
                if state == STATE_RED:
                    self.set_cell(x, y, STATE_BLACK)
                elif state == STATE_BLUE:
                    self.set_cell(x, y, STATE_WHITE)
        
        self.free_area_mode = False
        self.mark_free_btn.config(relief=tk.RAISED)
        self.update_stats()

    def on_slider_change(self, value):
        """Handler für Slider-Änderungen"""
        # Slider-Wert in Entry synchronisieren
        try:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"{float(value):.2f}")
        except Exception:
            pass
        
        # Sofort Gitter mit neuer Dichte generieren
        self.apply_density()

    def on_entry_change(self, _event=None):
        """Handler für Entry-Feld-Änderungen"""
        try:
            val = float(self.entry.get())

            # Wertbereich erzwingen
            if val < 1.0:
                val = 1.0
            if val > 100.0:
                val = 100.0

            # Density-Variable und Slider synchronisieren
            self.density.set(val)
            
            # Sofort Gitter mit neuer Dichte generieren
            self.apply_density()

        except ValueError:
            # Ungültige Eingabe ignorieren und auf aktuellen Wert zurücksetzen
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"{self.density.get():.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
