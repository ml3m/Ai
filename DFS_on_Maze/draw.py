import pygame
from colors import BLACK, GREEN, ORANGE, WHITE, GRAY, L_GREEN, D_YELLOW, L_GRAY
from config import MAZE_LINE_WIDTH, TILE_SIZE

#    ╔══════════════════════════════════════════════════════════════════════╗
#    ║    draw_element(screen, type {arrow, cell, walls}, *args, **kwargs)  ║
#    ║    handles all types.                                                ║
#    ╚══════════════════════════════════════════════════════════════════════╝

def draw_grid(surface, cols, rows):
    """Draws a light gray grid on the screen."""
    for x in range(cols):
        for y in range(rows):
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, L_GRAY, rect, 1)  # Draw the rectangle outline

def draw_element(screen, element_type, *args, **kwargs):
    if element_type == "arrow":
        x, y, direction = args
        center_x = x * TILE_SIZE + TILE_SIZE // 2
        center_y = y * TILE_SIZE + TILE_SIZE // 2
        size = TILE_SIZE // 5
#    ╔══════════════════════════════════════════════════════════════════════╗
#    ║    defines the arrow that represents the direction of the path.      ║
#    ╚══════════════════════════════════════════════════════════════════════╝
        offsets = {
            "up": [(0, -size), (-size // 1.5, size), (size // 1.5, size)],
            "down": [(0, size), (-size // 1.5, -size), (size // 1.5, -size)],
            "left": [(-size, 0), (size, -size // 1.5), (size, size // 1.5)],
            "right": [(size, 0), (-size, -size // 1.5), (-size, size // 1.5)],
        }
        points = [(center_x + dx, center_y + dy) for dx, dy in offsets[direction]]
        pygame.draw.polygon(screen, BLACK, points)

    elif element_type == "cell":
        x, y, color = args
        pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    elif element_type == "walls":
        cell = args[0]
        x, y = cell.x * TILE_SIZE, cell.y * TILE_SIZE
        if cell.walls.get("top"):
            pygame.draw.line(screen, BLACK, (x, y), (x + TILE_SIZE, y), MAZE_LINE_WIDTH)
        if cell.walls.get("right"):
            pygame.draw.line(
                screen, BLACK, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), MAZE_LINE_WIDTH
            )
        if cell.walls.get("bottom"):
            pygame.draw.line(
                screen, BLACK, (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE), MAZE_LINE_WIDTH
            )
        if cell.walls.get("left"):
            pygame.draw.line(screen, BLACK, (x, y + TILE_SIZE), (x, y), MAZE_LINE_WIDTH)

#    ╔══════════════════════════════════════════════════════════════════════╗
#    ║  renders the maze on screen by drawing its walls and, if provided,   ║
#    ║   highlighting explored cells and the solution path                  ║
#    ║  (with arrows from the function above)                               ║
#    ╚══════════════════════════════════════════════════════════════════════╝

def draw_maze(screen, grid_cells, cols, rows, explored=None, path=None, failed=False):
    screen.fill(L_GREEN)

    # Draw the grid
    draw_grid(screen, cols, rows)

    # Draw explored cells
    [draw_element(screen, "cell", x, y, D_YELLOW) for x, y in (explored if explored else [])]

    # Draw path
    if path:
        path_color = GREEN if not failed else ORANGE
        for x, y in path:
            draw_element(screen, "cell", x, y, path_color)

        # Draw arrows along the path
        for (x, y), (next_x, next_y) in zip(path, path[1:]):
            direction = (
                "right" if next_x > x else
                "left" if next_x < x else
                "down" if next_y > y else
                "up"
            )

            draw_element(screen, "arrow", x, y, direction)

    # Draw walls
    [draw_element(screen, "walls", cell) for cell in grid_cells]
