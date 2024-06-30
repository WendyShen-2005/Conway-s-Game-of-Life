class Pixel:
    def __init__(self, grid, i, j):
        self.grid = grid
        self.i = i
        self.j = j
        self.value = grid[i][j]