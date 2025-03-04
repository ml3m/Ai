import pygame
from colors import BLACK, GREEN, ORANGE, WHITE, GRAY, L_GREEN, D_YELLOW, L_GRAY
from config import MAZE_LINE_WIDTH, TILE_SIZE

#    ╔══════════════════════════════════════════════════════════════════════╗
#    ║    draw_element(screen, type {arrow, cell, walls}, *args, **kwargs)  ║
#    ║    handles all types.                                                ║
#    ╚══════════════════════════════════════════════════════════════════════╝

class Drawing:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = TILE_SIZE
        self.line_width = MAZE_LINE_WIDTH

    def draw_grid(self, cols, rows):
        """Draws a light gray grid on the screen."""
        for x in range(cols):
            for y in range(rows):
                rect = (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, L_GRAY, rect, 1)

    def draw_arrow(self, x, y, direction):
        """Draw an arrow indicating path direction"""
        center_x = x * self.tile_size + self.tile_size // 2
        center_y = y * self.tile_size + self.tile_size // 2
        size = self.tile_size // 5

        offsets = {
            "up": [(0, -size), (-size // 1.5, size), (size // 1.5, size)],
            "down": [(0, size), (-size // 1.5, -size), (size // 1.5, -size)],
            "left": [(-size, 0), (size, -size // 1.5), (size, size // 1.5)],
            "right": [(size, 0), (-size, -size // 1.5), (-size, size // 1.5)],
        }
        points = [(center_x + dx, center_y + dy) for dx, dy in offsets[direction]]
        pygame.draw.polygon(self.screen, BLACK, points)

    def draw_cell(self, x, y, color):
        """Draw a colored cell at the specified position"""
        pygame.draw.rect(
            self.screen, 
            color, 
            (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
        )

    def draw_walls(self, cell):
        """Draw the walls of a cell"""
        x, y = cell.x * self.tile_size, cell.y * self.tile_size
        if cell.walls.get("top"):
            pygame.draw.line(
                self.screen, 
                BLACK, 
                (x, y), 
                (x + self.tile_size, y), 
                self.line_width
            )
        if cell.walls.get("right"):
            pygame.draw.line(
                self.screen, 
                BLACK, 
                (x + self.tile_size, y), 
                (x + self.tile_size, y + self.tile_size), 
                self.line_width
            )
        if cell.walls.get("bottom"):
            pygame.draw.line(
                self.screen, 
                BLACK, 
                (x + self.tile_size, y + self.tile_size), 
                (x, y + self.tile_size), 
                self.line_width
            )
        if cell.walls.get("left"):
            pygame.draw.line(
                self.screen, 
                BLACK, 
                (x, y + self.tile_size), 
                (x, y), 
                self.line_width
            )

    def draw_maze(self, grid_cells, cols, rows, explored=None, path=None, failed=False):
        """Draw the complete maze with all its components"""
        self.screen.fill(L_GREEN)

        # Draw the grid
        self.draw_grid(cols, rows)

        # Draw explored cells
        if explored:
            for x, y in explored:
                self.draw_cell(x, y, D_YELLOW)

        # Draw path
        if path:
            path_color = GREEN if not failed else ORANGE
            for x, y in path:
                self.draw_cell(x, y, path_color)

            # Draw arrows along the path
            for (x, y), (next_x, next_y) in zip(path, path[1:]):
                direction = (
                    "right" if next_x > x else
                    "left" if next_x < x else
                    "down" if next_y > y else
                    "up"
                )
                self.draw_arrow(x, y, direction)

        # Draw walls
        for cell in grid_cells:
            self.draw_walls(cell)

    def draw_info_text(self, text, font_size=24):
        """Draw centered info text with background"""
        info_font = pygame.font.SysFont("Arial", font_size)
        info_text = info_font.render(text, True, BLACK)
        info_rect = info_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        padding = 10
        info_box = info_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(self.screen, GRAY, info_box)
        pygame.draw.rect(self.screen, BLACK, info_box, 2)
        self.screen.blit(info_text, info_rect)

# For backwards compatibility
def draw_maze(screen, grid_cells, cols, rows, explored=None, path=None, failed=False):
    drawer = Drawing(screen)
    drawer.draw_maze(grid_cells, cols, rows, explored, path, failed)
