import time
import pygame

from colors import BLACK, GRAY
from config import DEFAULT_HEIGHT, DEFAULT_WIDTH, FPS, SOLVING_SPEED
from draw import draw_maze
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
    maze = Maze(cols, rows)
    clock_main = pygame.time.Clock()
    running = True
    solve_maze = False
    dfs_step = False

    draw_maze(screen, maze.grid_cells, cols, rows)
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
                draw_maze,
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

        draw_maze(
            screen,
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
            info_font = pygame.font.SysFont("Arial", 24)
            info_text = info_font.render("Press Return to Solve the Maze", True, BLACK)
            info_rect = info_text.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )
            padding = 10
            info_box = info_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(screen, GRAY, info_box)
            pygame.draw.rect(screen, BLACK, info_box, 2)
            screen.blit(info_text, info_rect)

        pygame.display.flip()
        clock_main.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
