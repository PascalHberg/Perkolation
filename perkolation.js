// Perkolation Marco-Polo Schwelle Visualizer
// Author: Pascal Hässenberg
// GitHub: https://github.com/PascalHberg/Perkolation
// LinkedIn: https://www.linkedin.com/in/pascal-hässenberg-523480332/

const CELL_SIZE = 20;
const GRID_W = 25;
const GRID_H = 25;
const MARCO_POLO_THRESHOLD = 59.2746050792;

// Zellenzustände
const STATE_WHITE = 0;     // Freies Feld (weiß)
const STATE_BLACK = 1;     // Blockiertes Feld (schwarz)
const STATE_RED = 2;       // Rot markiert (zusammenhängend schwarz)
const STATE_BLUE = 3;      // Blau markiert (zusammenhängend weiß)

class PercolationGrid {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.canvas.width = GRID_W * CELL_SIZE;
        this.canvas.height = GRID_H * CELL_SIZE;
        
        this.grid = [];
        this.colors = {};
        this.freeAreaMode = false;
        
        this.initGrid();
        this.applyDensity(MARCO_POLO_THRESHOLD);
        this.draw();
        
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    initGrid() {
        this.grid = [];
        this.colors = {};
        
        for (let y = 0; y < GRID_H; y++) {
            this.grid[y] = [];
            for (let x = 0; x < GRID_W; x++) {
                this.grid[y][x] = STATE_WHITE;
                this.colors[`${x},${y}`] = 'white';
            }
        }
    }

    applyDensity(density) {
        const d = density / 100.0;
        
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                const state = Math.random() < d ? STATE_BLACK : STATE_WHITE;
                this.grid[y][x] = state;
                this.colors[`${x},${y}`] = state === STATE_BLACK ? 'black' : 'white';
            }
        }
        
        this.updateStats();
    }

    draw() {
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                const color = this.getColorForState(this.grid[y][x]);
                this.drawCell(x, y, color);
            }
        }
    }

    getColorForState(state) {
        const colorMap = {
            [STATE_WHITE]: 'white',
            [STATE_BLACK]: 'black',
            [STATE_RED]: '#ff6b6b',
            [STATE_BLUE]: '#4169e1'
        };
        return colorMap[state] || 'white';
    }

    drawCell(x, y, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        );
        
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        );
    }

    handleClick(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / CELL_SIZE);
        const y = Math.floor((event.clientY - rect.top) / CELL_SIZE);
        
        if (x >= 0 && x < GRID_W && y >= 0 && y < GRID_H) {
            if (this.freeAreaMode) {
                if (this.grid[y][x] === STATE_WHITE) {
                    this.floodFillFree(x, y);
                    this.freeAreaMode = false;
                    updateMarkFreeButtonStyle();
                }
            } else {
                if (this.grid[y][x] === STATE_BLACK) {
                    this.floodFillBlack(x, y);
                }
            }
            this.updateStats();
        }
    }

    floodFillBlack(startX, startY) {
        const stack = [[startX, startY]];
        const visited = new Set();
        
        while (stack.length > 0) {
            const [x, y] = stack.pop();
            const key = `${x},${y}`;
            
            if (visited.has(key)) continue;
            visited.add(key);
            
            if (x < 0 || x >= GRID_W || y < 0 || y >= GRID_H) continue;
            if (this.grid[y][x] !== STATE_BLACK) continue;
            
            this.grid[y][x] = STATE_RED;
            this.colors[key] = '#ff6b6b';
            this.drawCell(x, y, '#ff6b6b');
            
            stack.push([x + 1, y]);
            stack.push([x - 1, y]);
            stack.push([x, y + 1]);
            stack.push([x, y - 1]);
        }
    }

    floodFillFree(startX, startY) {
        const stack = [[startX, startY]];
        const visited = new Set();
        
        while (stack.length > 0) {
            const [x, y] = stack.pop();
            const key = `${x},${y}`;
            
            if (visited.has(key)) continue;
            visited.add(key);
            
            if (x < 0 || x >= GRID_W || y < 0 || y >= GRID_H) continue;
            if (this.grid[y][x] !== STATE_WHITE) continue;
            
            this.grid[y][x] = STATE_BLUE;
            this.colors[key] = '#4169e1';
            this.drawCell(x, y, '#4169e1');
            
            stack.push([x + 1, y]);
            stack.push([x - 1, y]);
            stack.push([x, y + 1]);
            stack.push([x, y - 1]);
        }
    }

    resetColors() {
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                let state = this.grid[y][x];
                if (state === STATE_RED) {
                    state = STATE_BLACK;
                } else if (state === STATE_BLUE) {
                    state = STATE_WHITE;
                }
                this.grid[y][x] = state;
                
                const color = this.getColorForState(state);
                this.colors[`${x},${y}`] = color;
                this.drawCell(x, y, color);
            }
        }
        this.freeAreaMode = false;
        updateMarkFreeButtonStyle();
        this.updateStats();
    }

    updateStats() {
        let totalCells = 0;
        let blackCells = 0;
        let whiteCells = 0;
        let redCells = 0;
        let blueCells = 0;
        
        for (let y = 0; y < GRID_H; y++) {
            for (let x = 0; x < GRID_W; x++) {
                const state = this.grid[y][x];
                totalCells++;
                if (state === STATE_BLACK) blackCells++;
                else if (state === STATE_WHITE) whiteCells++;
                else if (state === STATE_RED) redCells++;
                else if (state === STATE_BLUE) blueCells++;
            }
        }
        
        document.getElementById('gridSize').textContent = `${GRID_W}×${GRID_H}`;
        document.getElementById('totalCells').textContent = totalCells.toString();
        document.getElementById('blackCells').textContent = blackCells.toString();
        document.getElementById('whiteCells').textContent = whiteCells.toString();
        document.getElementById('redCells').textContent = redCells.toString();
        document.getElementById('blueCells').textContent = blueCells.toString();
    }

    activateFreeAreaMode() {
        this.freeAreaMode = true;
        updateMarkFreeButtonStyle();
    }
}

function updateMarkFreeButtonStyle() {
    const btn = document.getElementById('markFreeBtn');
    if (percolation.freeAreaMode) {
        btn.classList.add('active-mode');
    } else {
        btn.classList.remove('active-mode');
    }
}

let percolation = null;

window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    percolation = new PercolationGrid(canvas);
    
    const slider = document.getElementById('densitySlider');
    const input = document.getElementById('densityInput');
    const display = document.getElementById('densityDisplay');
    const applyBtn = document.getElementById('applyBtn');
    const resetBtn = document.getElementById('resetBtn');
    const markFreeBtn = document.getElementById('markFreeBtn');
    
    slider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        input.value = value.toFixed(2);
        display.textContent = value.toFixed(2) + '%';
        percolation.initGrid();
        percolation.applyDensity(value);
        percolation.draw();
    });
    
    input.addEventListener('change', (e) => {
        let value = parseFloat(e.target.value);
        
        if (isNaN(value) || value < 1.0) value = 1.0;
        if (value > 100.0) value = 100.0;
        
        slider.value = value;
        input.value = value.toFixed(2);
        display.textContent = value.toFixed(2) + '%';
        percolation.initGrid();
        percolation.applyDensity(value);
        percolation.draw();
    });
    
    applyBtn.addEventListener('click', () => {
        const density = parseFloat(slider.value);
        percolation.initGrid();
        percolation.applyDensity(density);
        percolation.draw();
    });
    
    resetBtn.addEventListener('click', () => {
        percolation.resetColors();
    });
    
    markFreeBtn.addEventListener('click', () => {
        percolation.activateFreeAreaMode();
    });
});