// Perkolation Marco-Polo Schwelle Visualizer
// Author: Pascal Hässenberg
// GitHub: https://github.com/PascalHberg/Perkolation
// LinkedIn: https://www.linkedin.com/in/pascal-ha%C3%9Fenberg-523480332/

const CELL_SIZE = 20;
const GRID_W = 25;
const GRID_H = 25;
const MARCO_POLO_THRESHOLD = 59.2746050792;

class PercolationGrid {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.canvas.width = GRID_W * CELL_SIZE;
        this.canvas.height = GRID_H * CELL_SIZE;
        
        this.grid = [];
        this.colors = {}; // Store cell colors for visualization
        
        this.initGrid();
        this.applyDensity(MARCO_POLO_THRESHOLD);
        this.draw();
        
        // Event listeners
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    // Initialize empty grid
    initGrid() {
        this.grid = [];
        this.colors = {};
        
        for (let y = 0; y < GRID_H; y++) {
            this.grid[y] = [];
            for (let x = 0; x < GRID_W; x++) {
                this.grid[y][x] = 0;
                this.colors[`${x},${y}`] = 'white';
            }
        }
    }

    // Apply random density to grid
    applyDensity(density) {
        const d = density / 100.0;
        let occupiedCount = 0;
        
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                const state = Math.random() < d ? 1 : 0;
                this.grid[y][x] = state;
                this.colors[`${x},${y}`] = state === 1 ? 'black' : 'white';
                if (state === 1) occupiedCount++;
            }
        }
        
        this.updateStats(occupiedCount);
    }

    // Draw grid on canvas
    draw() {
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                this.drawCell(x, y, this.colors[`${x},${y}`]);
            }
        }
    }

    // Draw single cell
    drawCell(x, y, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        );
        
        // Draw grid lines
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        );
    }

    // Handle canvas click - flood fill from clicked cell
    handleClick(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / CELL_SIZE);
        const y = Math.floor((event.clientY - rect.top) / CELL_SIZE);
        
        if (x >= 0 && x < GRID_W && y >= 0 && y < GRID_H) {
            if (this.grid[y][x] === 1) {
                this.floodFill(x, y);
            }
        }
    }

    // Flood fill algorithm using stack (DFS)
    floodFill(startX, startY) {
        const stack = [[startX, startY]];
        const visited = new Set();
        
        while (stack.length > 0) {
            const [x, y] = stack.pop();
            const key = `${x},${y}`;
            
            if (visited.has(key)) continue;
            visited.add(key);
            
            // Check bounds
            if (x < 0 || x >= GRID_W || y < 0 || y >= GRID_H) continue;
            
            // Check if cell is occupied
            if (this.grid[y][x] !== 1) continue;
            
            // Color the cell
            this.colors[key] = '#ff6b6b';
            this.drawCell(x, y, '#ff6b6b');
            
            // Add neighbors to stack
            stack.push([x + 1, y]);
            stack.push([x - 1, y]);
            stack.push([x, y + 1]);
            stack.push([x, y - 1]);
        }
    }

    // Reset colors while keeping grid state
    resetColors() {
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                const color = this.grid[y][x] === 1 ? 'black' : 'white';
                this.colors[`${x},${y}`] = color;
                this.drawCell(x, y, color);
            }
        }
    }

    // Update statistics display
    updateStats(occupiedCount) {
        const total = GRID_W * GRID_H;
        const currentDensity = ((occupiedCount / total) * 100).toFixed(2);
        
        document.getElementById('gridSize').textContent = `${GRID_W}×${GRID_H}`;
        document.getElementById('totalCells').textContent = total.toString();
        document.getElementById('occupiedCells').textContent = occupiedCount.toString();
        document.getElementById('currentDensity').textContent = `${currentDensity}%`;
    }
}

// Initialize application
let percolation = null;

window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    percolation = new PercolationGrid(canvas);
    
    // Slider and input synchronization
    const slider = document.getElementById('densitySlider');
    const input = document.getElementById('densityInput');
    const display = document.getElementById('densityDisplay');
    const applyBtn = document.getElementById('applyBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    // Slider change
    slider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        input.value = value.toFixed(2);
        display.textContent = value.toFixed(2) + '%';
    });
    
    // Input change
    input.addEventListener('change', (e) => {
        let value = parseFloat(e.target.value);
        
        // Validate range
        if (value < 1.0) value = 1.0;
        if (value > 100.0) value = 100.0;
        
        slider.value = value;
        input.value = value.toFixed(2);
        display.textContent = value.toFixed(2) + '%';
    });
    
    // Apply button - regenerate grid
    applyBtn.addEventListener('click', () => {
        const density = parseFloat(slider.value);
        percolation.initGrid();
        percolation.applyDensity(density);
        percolation.draw();
    });
    
    // Reset button - reset colors only
    resetBtn.addEventListener('click', () => {
        percolation.resetColors();
    });
});
