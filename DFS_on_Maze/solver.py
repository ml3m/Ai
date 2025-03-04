import time
import pygame
from draw import Drawing

#    ╔═════════════════════════════════════════════════════════════════════════╗
#    ║                             run_dfs()                                   ║
#    ║                                                                         ║
#    ║  Executes a modified depth-first search that dynamically renders        ║
#    ║  maze exploration on-screen by updating at each step, while tracking    ║
#    ║  statistics (nodes visited, dead-ends, path length) and adjusting the   ║
#    ║  solving speed via key events; returns the solution path or a dead-end  ║
#    ║  if no valid route to the goal is found.                                ║
#    ╚═════════════════════════════════════════════════════════════════════════╝

def run_dfs(
    grid_cells,
    start,
    goal,
    cols,
    explored_cells,
    screen,
    draw_maze_func,
    clock,
    stats,
    SOLVING_SPEED,
):
    stats["start_time"] = time.time()
    stats["nodes_visited"] = 0
    stats["dead_ends"] = 0

    start_cell = grid_cells[start[0] + start[1] * cols]
    goal_cell = grid_cells[goal[0] + goal[1] * cols]
    stack = [(start_cell, [])]
    visited = set()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ([], False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    SOLVING_SPEED = max(5, SOLVING_SPEED - 5)
                elif event.key == pygame.K_DOWN:
                    SOLVING_SPEED = min(500, SOLVING_SPEED + 5)

        current, current_path = stack.pop()
        current_coords = (current.x, current.y)
        stats["nodes_visited"] += 1

        if current_coords in visited:
            continue
        visited.add(current_coords)
        explored_cells.add(current_coords)

        pygame.time.delay(SOLVING_SPEED)
        draw_maze_func(grid_cells, cols, len(grid_cells) // cols, explored_cells)
        pygame.display.flip()

        if current == goal_cell:
            final_path = current_path + [current_coords]
            draw_maze_func(
                grid_cells,
                cols,
                len(grid_cells) // cols,
                explored_cells,
                final_path,
                failed=False,
            )
            pygame.display.flip()
            stats["end_time"] = time.time()
            stats["path_length"] = len(final_path)
            return (final_path, True)

        neighbors = current.get_neighbors(grid_cells)
        unvisited_neighbors = [n for n in neighbors if (n.x, n.y) not in visited]

        if not unvisited_neighbors:
            stats["dead_ends"] += 1
            dead_end_path = current_path + [current_coords]
            draw_maze_func(
                grid_cells,
                cols,
                len(grid_cells) // cols,
                explored_cells,
                dead_end_path,
                failed=True,
            )
            pygame.display.flip()
            stats["end_time"] = time.time()
            stats["path_length"] = len(dead_end_path)
            return (dead_end_path, False)

        for neighbor in unvisited_neighbors:
            stack.append((neighbor, current_path + [current_coords]))

    stats["end_time"] = time.time()
    return ([], False)

# This function is kept for compatibility and will be imported back in the Maze class
# It's redundant but ensures smooth transition to the new architecture
