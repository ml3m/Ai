import pygame
from maze import generate_maze
from search import dfs

# Pygame initialization
pygame.init()

TILE_SIZE = 30
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)

# Initialize screen with a default size for input dialog
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
pygame.display.set_caption("Maze Visualization")

# Font setup
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Default solving speed (delay in milliseconds)
SOLVING_SPEED = 50

# Function to create text input box
def draw_text_input(prompt, value, active, x, y, width, height):
    # Draw the box
    box_color = BLUE if active else GRAY
    pygame.draw.rect(screen, box_color, (x, y, width, height), 2)
    pygame.draw.rect(screen, WHITE, (x+2, y+2, width-4, height-4))
    
    # Draw the prompt and value
    prompt_text = font.render(prompt, True, BLACK)
    screen.blit(prompt_text, (x - prompt_text.get_width() - 10, y + height//2 - prompt_text.get_height()//2))
    
    if value:
        value_text = font.render(value, True, BLACK)
        screen.blit(value_text, (x + 10, y + height//2 - value_text.get_height()//2))

# Function to get user input for maze dimensions
def get_maze_dimensions():
    global SOLVING_SPEED
    
    cols_input = ""
    rows_input = ""
    speed_input = "50"  # Default speed
    active_input = "cols"  # Which input box is active
    
    input_width = 200
    input_height = 40
    input_x = DEFAULT_WIDTH // 2 + 10
    cols_y = DEFAULT_HEIGHT // 2 - 100
    rows_y = DEFAULT_HEIGHT // 2 - 30
    speed_y = DEFAULT_HEIGHT // 2 + 40
    
    button_width = 180
    button_height = 50
    button_x = DEFAULT_WIDTH // 2 - button_width // 2
    button_y = DEFAULT_HEIGHT // 2 + 120
    
    running = True
    while running:
        screen.fill(WHITE)
        
        # Title
        title_text = font.render("Maze Generator and Solver", True, BLACK)
        screen.blit(title_text, (DEFAULT_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        # Instructions
        instructions1 = small_font.render("Enter maze dimensions and solving speed below", True, BLACK)
        instructions2 = small_font.render("Press Enter or click Start when ready", True, BLACK)
        instructions3 = small_font.render("Press Space during maze display to solve", True, BLACK)
        
        screen.blit(instructions1, (DEFAULT_WIDTH // 2 - instructions1.get_width() // 2, 120))
        screen.blit(instructions2, (DEFAULT_WIDTH // 2 - instructions2.get_width() // 2, 140))
        screen.blit(instructions3, (DEFAULT_WIDTH // 2 - instructions3.get_width() // 2, 160))
        
        # Draw input boxes
        draw_text_input("Columns:", cols_input, active_input == "cols", input_x, cols_y, input_width, input_height)
        draw_text_input("Rows:", rows_input, active_input == "rows", input_x, rows_y, input_width, input_height)
        draw_text_input("Speed (ms):", speed_input, active_input == "speed", input_x, speed_y, input_width, input_height)
        
        # Add speed explanation
        speed_info = small_font.render("Lower = faster, Higher = slower (10-500 recommended)", True, BLACK)
        screen.blit(speed_info, (DEFAULT_WIDTH // 2 - speed_info.get_width() // 2, speed_y + input_height + 5))
        
        # Draw start button
        pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
        button_text = font.render("Start Maze", True, BLACK)
        screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, 
                                  button_y + button_height // 2 - button_text.get_height() // 2))
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicked on cols input
                if input_x <= event.pos[0] <= input_x + input_width:
                    if cols_y <= event.pos[1] <= cols_y + input_height:
                        active_input = "cols"
                    elif rows_y <= event.pos[1] <= rows_y + input_height:
                        active_input = "rows"
                    elif speed_y <= event.pos[1] <= speed_y + input_height:
                        active_input = "speed"
                
                # Check if clicked on start button
                elif button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                    if cols_input and rows_input and speed_input:
                        try:
                            cols = int(cols_input)
                            rows = int(rows_input)
                            speed = int(speed_input)
                            if cols > 0 and rows > 0 and speed > 0:
                                SOLVING_SPEED = speed
                                return cols, rows
                        except ValueError:
                            pass
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    # Switch between input boxes
                    if active_input == "cols":
                        active_input = "rows"
                    elif active_input == "rows":
                        active_input = "speed"
                    else:
                        active_input = "cols"
                
                elif event.key == pygame.K_RETURN:
                    if cols_input and rows_input and speed_input:
                        try:
                            cols = int(cols_input)
                            rows = int(rows_input)
                            speed = int(speed_input)
                            if cols > 0 and rows > 0 and speed > 0:
                                SOLVING_SPEED = speed
                                return cols, rows
                        except ValueError:
                            pass
                
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == "cols":
                        cols_input = cols_input[:-1]
                    elif active_input == "rows":
                        rows_input = rows_input[:-1]
                    else:
                        speed_input = speed_input[:-1]
                
                else:
                    # Add character if it's a digit
                    if event.unicode.isdigit():
                        if active_input == "cols":
                            cols_input += event.unicode
                        elif active_input == "rows":
                            rows_input += event.unicode
                        else:
                            speed_input += event.unicode
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    return None, None

# setup display
def setup_display(cols, rows):
    width = cols * TILE_SIZE
    height = rows * TILE_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Visualization")
    return screen

# arrow direction
def draw_arrow(screen, x, y, direction):
    center_x = x * TILE_SIZE + TILE_SIZE // 2
    center_y = y * TILE_SIZE + TILE_SIZE // 2
    size = TILE_SIZE // 3  # Arrow size

    if direction == "up":
        pygame.draw.polygon(screen, BLACK, [(center_x, center_y - size), (center_x - size // 2, center_y + size),
                                            (center_x + size // 2, center_y + size)])
    elif direction == "down":
        pygame.draw.polygon(screen, BLACK, [(center_x, center_y + size), (center_x - size // 2, center_y - size),
                                            (center_x + size // 2, center_y - size)])
    elif direction == "left":
        pygame.draw.polygon(screen, BLACK, [(center_x - size, center_y), (center_x + size, center_y - size // 2),
                                            (center_x + size, center_y + size // 2)])
    elif direction == "right":
        pygame.draw.polygon(screen, BLACK, [(center_x + size, center_y), (center_x - size, center_y - size // 2),
                                            (center_x - size, center_y + size // 2)])

# draw the maze
def draw_maze(screen, grid_cells, cols, rows, explored=None, path=None):
    screen.fill(WHITE)

    # draw path gray during DFS
    if explored:
        for cell in explored:
            x, y = cell
            pygame.draw.rect(screen, (200, 200, 200), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # draw correct path green
    if path:
        for (x, y) in path:
            pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw arrows
        for i in range(len(path) - 1):
            x, y = path[i]
            next_x, next_y = path[i + 1]
            if next_x > x:
                draw_arrow(screen, x, y, "right")
            elif next_x < x:
                draw_arrow(screen, x, y, "left")
            elif next_y > y:
                draw_arrow(screen, x, y, "down")
            elif next_y < y:
                draw_arrow(screen, x, y, "up")

    # draw walls
    for cell in grid_cells:
        x, y = cell.x * TILE_SIZE, cell.y * TILE_SIZE
        if cell.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + TILE_SIZE, y), 2)
        if cell.walls['right']:
            pygame.draw.line(screen, BLACK, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 2)
        if cell.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE), 2)
        if cell.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y + TILE_SIZE), (x, y), 2)

    # Draw instruction at bottom
    font = pygame.font.SysFont('Arial', 16)
    text = font.render("Press SPACE to solve the maze", True, BLACK)
    screen.blit(text, (10, 10))
    
    # Show current speed
    speed_text = font.render(f"Solving Speed: {SOLVING_SPEED}ms", True, BLACK)
    screen.blit(speed_text, (10, 30))

# Modified dfs function
def modified_dfs(grid_cells, start, goal, cols, explored_cells, screen, draw_maze, clock):
    global SOLVING_SPEED

    start_cell = grid_cells[start[0] + start[1] * cols]
    goal_cell = grid_cells[goal[0] + goal[1] * cols]
    stack = [(start_cell, [])]  # Stack to hold the current cell and the path to it
    visited = set()  # Set to track visited cells

    while stack:
        # Check for events (including speed adjustments)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return []

            if event.type == pygame.KEYDOWN:
                # Speed up with up arrow
                if event.key == pygame.K_UP:
                    SOLVING_SPEED = max(5, SOLVING_SPEED - 5)
                # Slow down with down arrow
                elif event.key == pygame.K_DOWN:
                    SOLVING_SPEED = min(500, SOLVING_SPEED + 5)

        current, current_path = stack.pop()  # Get the current cell and the path to it
        current_coords = (current.x, current.y)

        # If the current cell has already been visited, skip it
        if current_coords in visited:
            continue

        # Mark the current cell as visited
        visited.add(current_coords)
        explored_cells.add(current_coords)

        # Update the screen during DFS
        pygame.time.delay(SOLVING_SPEED)  # Use the variable speed
        draw_maze(screen, grid_cells, cols, len(grid_cells) // cols, explored_cells)
        pygame.display.flip()

        # If the goal cell is reached, return the path
        if current == goal_cell:
            return current_path + [current_coords]

        # Get the neighbors of the current cell
        neighbors = current.get_neighbors(grid_cells)

        # Filter out neighbors that have already been visited
        unvisited_neighbors = [
            neighbor for neighbor in neighbors if (neighbor.x, neighbor.y) not in visited
        ]

        # If there are no unvisited neighbors, this is a dead end
        if not unvisited_neighbors:
            print("Dead end reached at:", current_coords)
            return []  # Stop the search completely

        # Add the first unvisited neighbor to the stack (no backtracking)
        for neighbor in unvisited_neighbors:
            stack.append((neighbor, current_path + [current_coords]))

    # If no path is found, return an empty list
    return []

# visualisation of the maze/DFS
def main():
    global SOLVING_SPEED
    
    # Get maze dimensions from Pygame interface
    cols, rows = get_maze_dimensions()
    
    # If user closed the window
    if cols is None or rows is None:
        return
    
    # display size
    screen = setup_display(cols, rows)

    # maze generator
    grid_cells = generate_maze(cols, rows)

    # var for DFS visualisation
    explored_cells = set()
    correct_path = []

    # start/goal
    start = (0, 0)
    goal = (cols - 1, rows - 1)

    clock = pygame.time.Clock()
    running = True
    solve_maze = False
    dfs_step = False

    # display maze
    draw_maze(screen, grid_cells, cols, rows)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solve_maze = True
                    print("SPACE pressed...")
                # Add speed controls while viewing the maze
                elif event.key == pygame.K_UP:
                    SOLVING_SPEED = max(5, SOLVING_SPEED - 5)
                    print(f"Speed increased: {SOLVING_SPEED}ms delay")
                elif event.key == pygame.K_DOWN:
                    SOLVING_SPEED = min(500, SOLVING_SPEED + 5)
                    print(f"Speed decreased: {SOLVING_SPEED}ms delay")

        if solve_maze and not dfs_step:
            print("DFS is starting...")
            # Use the modified DFS function
            correct_path = modified_dfs(grid_cells, start, goal, cols, explored_cells, screen, draw_maze, clock)
            dfs_step = True
            print("DFS completed.")

            # print correct path cells in terminal
            if correct_path:
                print(f"Correct path (total {len(correct_path)} cells):")
                # break every 10 cells
                for i in range(0, len(correct_path), 10):
                    chunk = correct_path[i:i + 10]
                    path_str = " -> ".join([f"({x}, {y})" for (x, y) in chunk])
                    print(path_str)
            else:
                print("No path found.")

        # draw correct/wrong paths
        draw_maze(screen, grid_cells, cols, rows, explored_cells, correct_path)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
