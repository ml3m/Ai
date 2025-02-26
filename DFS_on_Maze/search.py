import pygame

#    ╔══════════════════════════════════════════════════════════════════════════╗
#    ║  Executes a depth-first search (DFS) through maze cells, dynamically     ║
#    ║  visualizing each step by updating the Pygame display, and returns the   ║
#    ║  solution path from the start to the goal—or an empty list if no path is ║
#    ║  found.                                                                  ║
#    ╚══════════════════════════════════════════════════════════════════════════╝

def dfs(grid_cells, start, goal, cols, explored_cells, screen, draw_maze, clock):
    start_cell = grid_cells[start[0] + start[1] * cols]
    goal_cell = grid_cells[goal[0] + goal[1] * cols]

    stack = [(start_cell, [])]
    visited = set()

    while stack:
        current, current_path = stack.pop()
        current_coords = (current.x, current.y)

        if current_coords in visited:
            continue

        visited.add(current_coords)
        explored_cells.add(current_coords)

        # update screen
        pygame.time.delay(50)
        draw_maze(screen, grid_cells, cols, len(grid_cells) // cols, explored_cells)
        pygame.display.flip()

        if current == goal_cell:
            return current_path + [current_coords]

        neighbors = current.get_neighbors(grid_cells)

        for neighbor in neighbors:
            if (neighbor.x, neighbor.y) not in visited:
                stack.append((neighbor, current_path + [current_coords]))

    return []
