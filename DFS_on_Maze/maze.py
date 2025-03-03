from random import choice

#    ╔══════════════════════════════════════════════════════════════════════╗
#    ║  Defines a maze with cell management, wall removal, and DFS-based    ║
#    ║  maze generation for constructing a perfect labyrinth.               ║
#    ╚══════════════════════════════════════════════════════════════════════╝

class Cell:
    def __init__(self, x, y, cols, rows):
        self.x, self.y = x, y
        self.cols, self.rows = cols, rows
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
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

    # retrieve neighbors
    def get_neighbors(self, grid_cells):
        neighbors = []
        if not self.walls["top"]:
            neighbors.append(self.check_cell(self.x, self.y - 1, grid_cells))
        if not self.walls["right"]:
            neighbors.append(self.check_cell(self.x + 1, self.y, grid_cells))
        if not self.walls["bottom"]:
            neighbors.append(self.check_cell(self.x, self.y + 1, grid_cells))
        if not self.walls["left"]:
            neighbors.append(self.check_cell(self.x - 1, self.y, grid_cells))
        return [n for n in neighbors if n]  # Return only valid neighbors

    # check for path between 2 cells
    def is_path_between(self, other):
        dx, dy = self.x - other.x, self.y - other.y
        return (
            (dx == 1 and not self.walls["left"] and not other.walls["right"]) or
            (dx == -1 and not self.walls["right"] and not other.walls["left"]) or
            (dy == 1 and not self.walls["top"] and not other.walls["bottom"]) or
            (dy == -1 and not self.walls["bottom"] and not other.walls["top"])
        )


class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid_cells = []
        self.explored_cells = set()
        self.correct_path = []
        self.start = (0, 0)
        self.goal = (cols - 1, rows - 1)
        self.stats = {}
        self.generate_maze()

    def generate_maze(self):
        """Generate a perfect maze using DFS algorithm"""
        self.grid_cells = [Cell(col, row, self.cols, self.rows) 
                           for row in range(self.rows) 
                           for col in range(self.cols)]
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1

        while break_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.grid_cells)
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        
        # Reset the visited status for all cells for future use
        for cell in self.grid_cells:
            cell.visited = False
        
        return self.grid_cells

    def remove_walls(self, current, next):
        """Remove walls between adjacent cells to create a path"""
        dx = current.x - next.x
        if dx == 1:
            current.walls["left"] = False
            next.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next.walls["left"] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls["top"] = False
            next.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next.walls["top"] = False

    def run_dfs(self, screen, draw_maze, clock, solving_speed):
        """Moved from solver.py - will serve as a placeholder for the actual implementation"""
        from solver import run_dfs
        return run_dfs(
            self.grid_cells,
            self.start,
            self.goal,
            self.cols,
            self.explored_cells,
            screen,
            draw_maze,
            clock,
            self.stats,
            solving_speed,
        )

    def reset(self):
        """Reset the maze for a new run"""
        self.explored_cells = set()
        self.correct_path = []
        self.stats = {}

# Maintain backwards compatibility with existing code
def generate_maze(cols, rows):
    maze = Maze(cols, rows)
    return maze.grid_cells

def remove_walls(current, next):
    Maze(1, 1).remove_walls(current, next)
