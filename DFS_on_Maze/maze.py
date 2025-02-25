from random import choice

class Cell:
    def __init__(self, x, y, cols, rows):
        self.x, self.y = x, y
        self.cols, self.rows = cols, rows
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def check_cell(self, x, y, grid_cells):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        return grid_cells[x + y * self.cols]

    def check_neighbors(self, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, grid_cells)
        right = self.check_cell(self.x + 1, self.y, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        left = self.check_cell(self.x - 1, self.y, grid_cells)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    # retrieve  neighbors
    def get_neighbors(self, grid_cells):
        neighbors = []
        if not self.walls['top']:
            neighbors.append(self.check_cell(self.x, self.y - 1, grid_cells))
        if not self.walls['right']:
            neighbors.append(self.check_cell(self.x + 1, self.y, grid_cells))
        if not self.walls['bottom']:
            neighbors.append(self.check_cell(self.x, self.y + 1, grid_cells))
        if not self.walls['left']:
            neighbors.append(self.check_cell(self.x - 1, self.y, grid_cells))
        return [n for n in neighbors if n]  # Return only valid neighbors

    # check for path between 2 cells
    def is_path_between(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        if dx == 1 and not self.walls['left'] and not other.walls['right']:
            return True
        if dx == -1 and not self.walls['right'] and not other.walls['left']:
            return True
        if dy == 1 and not self.walls['top'] and not other.walls['bottom']:
            return True
        if dy == -1 and not self.walls['bottom'] and not other.walls['top']:
            return True
        return False

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze(cols, rows):
    grid_cells = [Cell(col, row, cols, rows) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()

    return grid_cells
