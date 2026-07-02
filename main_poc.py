import tkinter as tk
import random

CELL_SIZE = 20
GRID_W = 25
GRID_H = 25


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid PoC")

        self.canvas = tk.Canvas(
            root,
            width=GRID_W * CELL_SIZE,
            height=GRID_H * CELL_SIZE
        )
        self.canvas.pack()

        tk.Label(root, text="Density (1.00 - 100.00)").pack()

        self.density = tk.DoubleVar(value=50.00)

        # Slider
        self.slider = tk.Scale(
            root,
            from_=1.00,
            to=100.00,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            variable=self.density,
            command=self.on_slider_change
        )
        self.slider.set(50.00)
        self.slider.pack(fill="x")

        # Entry field (manual input)
        self.entry = tk.Entry(root)
        self.entry.insert(0, "50.00")
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_entry_change)

        self.reset_btn = tk.Button(root, text="Reset", command=self.reset)
        self.reset_btn.pack()

        self.grid = []
        self.rects = {}

        self.init_grid()
        self.apply_density()

        self.canvas.bind("<Button-1>", self.on_click)

    def init_grid(self):
        self.canvas.delete("all")
        self.grid = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
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
        d = float(self.density.get()) / 100.0

        for y in range(GRID_H):
            for x in range(GRID_W):
                state = 1 if random.random() < d else 0
                self.set_cell(x, y, state)

    def set_cell(self, x, y, state):
        self.grid[y][x] = state
        color = "black" if state == 1 else "white"
        self.canvas.itemconfig(self.rects[(x, y)], fill=color)

    def on_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if 0 <= x < GRID_W and 0 <= y < GRID_H:
            if self.grid[y][x] == 1:
                self.paint_region(x, y)

    def paint_region(self, x, y):
        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            if not (0 <= cx < GRID_W and 0 <= cy < GRID_H):
                continue

            if self.grid[cy][cx] != 1:
                continue

            self.canvas.itemconfig(self.rects[(cx, cy)], fill="red")

            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def reset(self):
        for y in range(GRID_H):
            for x in range(GRID_W):
                color = "black" if self.grid[y][x] == 1 else "white"
                self.canvas.itemconfig(self.rects[(x, y)], fill=color)

    # Slider -> Entry sync
    def on_slider_change(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{float(value):.2f}")
        self.apply_density()

    # Entry -> Slider sync
    def on_entry_change(self, _event=None):
        try:
            val = float(self.entry.get())

            if val < 1.0:
                val = 1.0
            if val > 100.0:
                val = 100.0

            self.density.set(val)
            self.slider.set(val)
            self.apply_density()

        except ValueError:
            # ungültige Eingabe ignorieren
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"{self.density.get():.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
