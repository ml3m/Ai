import time
import pygame

from colors import BLACK, GRAY
from config import DEFAULT_HEIGHT, DEFAULT_WIDTH, FPS, SOLVING_SPEED
from draw import Drawing
from maze import Maze
from ui import get_maze_dimensions, setup_display

#      ╔══════════════════════╗
#      ║        main()        ║
#      ╚══════════════════════╝

def main():
    global SOLVING_SPEED
    pygame.init()
    # Initially create a screen for the input dialog.
    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    cols, rows = get_maze_dimensions(screen)
    if cols is None or rows is None:
        return

    screen = setup_display(cols, rows)
    drawer = Drawing(screen)
    maze = Maze(cols, rows)
    clock_main = pygame.time.Clock()
    running = True
    solve_maze = False
    dfs_step = False

    drawer.draw_maze(maze.grid_cells, cols, rows)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    solve_maze = True
                elif event.key == pygame.K_UP:
                    SOLVING_SPEED = max(5, SOLVING_SPEED - 5)
                elif event.key == pygame.K_DOWN:
                    SOLVING_SPEED = min(500, SOLVING_SPEED + 5)

        if solve_maze and not dfs_step:
            attempted_path, found_solution = maze.run_dfs(
                screen,
                drawer.draw_maze,
                clock_main,
                SOLVING_SPEED,
            )
            maze.correct_path = attempted_path
            dfs_step = True

            total_cells = cols * rows
            maze_coverage = (len(maze.explored_cells) / total_cells) * 100

            print("\n╔════════════════════════════════════╗")
            print("║        Statistics for this run     ║")
            print("╚════════════════════════════════════╝\n")
            print(f"Total Maze Cells: {total_cells}")
            print(f"Nodes Visited: {maze.stats.get('nodes_visited', 0)}")
            print(f"Maze Coverage: {maze_coverage:.2f}%")
            print(f"Execution Time: {maze.stats.get('end_time', time.time()) - maze.stats.get('start_time', time.time()):.2f} secs")

        drawer.draw_maze(
            maze.grid_cells,
            cols,
            rows,
            maze.explored_cells,
            maze.correct_path,
            failed=(
                dfs_step and maze.correct_path and maze.correct_path[-1] != (cols - 1, rows - 1)
            ),
        )

        if not solve_maze:
            drawer.draw_info_text("Press Return to Solve the Maze")

        pygame.display.flip()
        clock_main.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
