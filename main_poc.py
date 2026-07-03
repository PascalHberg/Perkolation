import tkinter as tk
from tkinter import ttk
import random

CELL_SIZE = 20
GRID_W = 25
GRID_H = 25

STATE_WHITE = 0
STATE_BLACK = 1
STATE_RED = 2
STATE_BLUE = 3


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Perkolation - Grid Simulator")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ---------------- STATS ----------------
        self.stats_frame = ttk.LabelFrame(self.left_frame, text="Statistiken", padding=10)
        self.stats_frame.pack(fill=tk.X, pady=5)

        self.label_total = ttk.Label(self.stats_frame, text="Gesamt: 0")
        self.label_black = ttk.Label(self.stats_frame, text="Schwarz: 0")
        self.label_white = ttk.Label(self.stats_frame, text="Weiß: 0")
        self.label_red = ttk.Label(self.stats_frame, text="Rot: 0")
        self.label_blue = ttk.Label(self.stats_frame, text="Blau: 0")

        for l in (self.label_total, self.label_black, self.label_white, self.label_red, self.label_blue):
            l.pack(anchor="w")

        # ---------------- DENSITY ----------------
        self.density_frame = ttk.LabelFrame(self.left_frame, text="Dichte", padding=10)
        self.density_frame.pack(fill=tk.X, pady=5)

        self.density = tk.DoubleVar(value=50.0)

        self.slider = ttk.Scale(
            self.density_frame,
            from_=1.0,
            to=100.0,
            variable=self.density,
            command=self.on_slider_change
        )
        self.slider.pack(fill=tk.X)

        self.entry = ttk.Entry(self.density_frame)
        self.entry.insert(0, "50.00")
        self.entry.pack(fill=tk.X, pady=5)

        self.entry.bind("<Return>", self.on_entry_change)
        self.entry.bind("<FocusOut>", self.on_entry_change)

        # ---------------- BUTTONS ----------------
        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(fill=tk.X, pady=5)

        self.reset_btn = ttk.Button(self.button_frame, text="Reset", command=self.reset)
        self.reset_btn.pack(fill=tk.X, pady=2)

        # ---------------- INFO ----------------
        self.info = tk.Text(self.left_frame, height=12, width=30)
        self.info.pack(fill=tk.BOTH, expand=True)

        self.info.insert(tk.END,
            "Schwarz:\n"
            "- Klick → zusammenhängend rot\n\n"
            "Weiß:\n"
            "- Klick → zusammenhängend blau (automatisch)\n\n"
            "Dichte:\n"
            "- Slider oder Eingabe (1.00 - 100.00)\n"
        )
        self.info.config(state=tk.DISABLED)

        # ---------------- CANVAS ----------------
        self.canvas = tk.Canvas(
            self.right_frame,
            width=GRID_W * CELL_SIZE,
            height=GRID_H * CELL_SIZE,
            bg="white"
        )
        self.canvas.pack()

        self.grid = []
        self.rects = {}

        self.init_grid()
        self.apply_density()

        self.canvas.bind("<Button-1>", self.on_click)

    # ---------------- GRID ----------------
    def init_grid(self):
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

    def apply_density(self, _=None):
        d = float(self.density.get()) / 100.0

        for y in range(GRID_H):
            for x in range(GRID_W):
                state = STATE_BLACK if random.random() < d else STATE_WHITE
                self.set_cell(x, y, state)

        self.update_stats()

    def set_cell(self, x, y, state):
        self.grid[y][x] = state

        colors = {
            STATE_WHITE: "white",
            STATE_BLACK: "black",
            STATE_RED: "red",
            STATE_BLUE: "blue"
        }

        self.canvas.itemconfig(self.rects[(x, y)], fill=colors[state])

    # ---------------- INPUT ----------------
    def on_slider_change(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{float(value):.2f}")
        self.apply_density()

    def on_entry_change(self, _=None):
        try:
            val = float(self.entry.get().replace(",", "."))
            val = max(1.0, min(100.0, val))

            self.density.set(val)
            self.slider.set(val)
            self.apply_density()

        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"{self.density.get():.2f}")

    # ---------------- CLICK ----------------
    def on_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if not (0 <= x < GRID_W and 0 <= y < GRID_H):
            return

        if self.grid[y][x] == STATE_BLACK:
            self.flood(x, y, STATE_BLACK, STATE_RED)

        elif self.grid[y][x] == STATE_WHITE:
            self.flood(x, y, STATE_WHITE, STATE_BLUE)

        self.update_stats()

    # ---------------- FLOOD FILL ----------------
    def flood(self, x, y, target, replace):
        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            if not (0 <= cx < GRID_W and 0 <= cy < GRID_H):
                continue

            if self.grid[cy][cx] != target:
                continue

            self.set_cell(cx, cy, replace)

            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    # ---------------- RESET ----------------
    def reset(self):
        self.apply_density()

    # ---------------- STATS ----------------
    def update_stats(self):
        total = GRID_W * GRID_H
        black = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_BLACK)
        white = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_WHITE)
        red = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_RED)
        blue = sum(1 for y in range(GRID_H) for x in range(GRID_W) if self.grid[y][x] == STATE_BLUE)

        self.label_total.config(text=f"Gesamt: {total}")
        self.label_black.config(text=f"Schwarz: {black}")
        self.label_white.config(text=f"Weiß: {white}")
        self.label_red.config(text=f"Rot: {red}")
        self.label_blue.config(text=f"Blau: {blue}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
