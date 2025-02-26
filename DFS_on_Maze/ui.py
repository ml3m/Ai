import pygame
from colors import BLACK, BLUE, GRAY, GREEN, WHITE
from config import DEFAULT_HEIGHT, DEFAULT_WIDTH, FPS, TILE_SIZE

#      ╔═════════════════════════════════════════════════════╗
#      ║        handles all maze <-> screen interactions     ║
#      ╚═════════════════════════════════════════════════════╝

pygame.font.init()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

def draw_text_input(screen, prompt, value, active, x, y, width, height):
    box_color = BLUE if active else GRAY
    pygame.draw.rect(screen, box_color, (x, y, width, height), 2)
    pygame.draw.rect(screen, WHITE, (x + 2, y + 2, width - 4, height - 4))
    prompt_text = font.render(prompt, True, BLACK)
    screen.blit(prompt_text, (x - prompt_text.get_width() - 10, y + height // 2 - prompt_text.get_height() // 2))
    if value:
        value_text = font.render(value, True, BLACK)
        screen.blit(value_text, (x + 10, y + height // 2 - value_text.get_height() // 2))

def render_text_centered(screen, text, font, y_offset):
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (DEFAULT_WIDTH // 2 - rendered_text.get_width() // 2, y_offset))

def handle_input(event, active_input, inputs):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            return {"cols": "rows", "rows": "speed", "speed": "cols"}[active_input]
        elif event.key == pygame.K_RETURN:
            return "submit"
        elif event.key == pygame.K_BACKSPACE:
            inputs[active_input] = inputs[active_input][:-1]
        elif event.unicode.isdigit():
            inputs[active_input] += event.unicode
    return active_input

def get_maze_dimensions(screen):
    global SOLVING_SPEED
    inputs = {"cols": "", "rows": "", "speed": "50"}
    active_input = "cols"

    input_rects = {
        "cols": (DEFAULT_WIDTH // 2 + 10, DEFAULT_HEIGHT // 2 - 100, 200, 40),
        "rows": (DEFAULT_WIDTH // 2 + 10, DEFAULT_HEIGHT // 2 - 30, 200, 40),
        "speed": (DEFAULT_WIDTH // 2 + 10, DEFAULT_HEIGHT // 2 + 40, 200, 40),
    }
    button_rect = (DEFAULT_WIDTH // 2 - 90, DEFAULT_HEIGHT // 2 + 120, 180, 50)

    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        render_text_centered(screen, "Maze Generator and Solver", font, 100)
        render_text_centered(screen, "Enter maze dimensions and solving speed below", small_font, 120)
        render_text_centered(screen, "Press Enter or click Start when ready", small_font, 140)

        for key, rect in input_rects.items():
            draw_text_input(screen, key.capitalize() + ":", inputs[key], active_input == key, *rect)

        render_text_centered(screen, "Lower = faster, Higher = slower (10-500 recommended)", small_font, input_rects["speed"][1] + 45)
        pygame.draw.rect(screen, GREEN, button_rect)
        render_text_centered(screen, "Start Maze", font, button_rect[1] + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(rect[0] <= event.pos[0] <= rect[0] + rect[2] and rect[1] <= event.pos[1] <= rect[1] + rect[3] for key, rect in input_rects.items()):
                    active_input = next(key for key, rect in input_rects.items() if rect[0] <= event.pos[0] <= rect[0] + rect[2] and rect[1] <= event.pos[1] <= rect[1] + rect[3])
                elif button_rect[0] <= event.pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= event.pos[1] <= button_rect[1] + button_rect[3]:
                    active_input = "submit"
            else:
                active_input = handle_input(event, active_input, inputs)

        if active_input == "submit":
            try:
                cols, rows, speed = int(inputs["cols"]), int(inputs["rows"]), int(inputs["speed"])
                if cols > 0 and rows > 0 and 10 <= speed <= 500:
                    SOLVING_SPEED = speed
                    return cols, rows
            except ValueError:
                pass

        pygame.display.flip()
        clock.tick(FPS)

def setup_display(cols, rows):
    screen = pygame.display.set_mode((cols * TILE_SIZE, rows * TILE_SIZE))
    pygame.display.set_caption("Maze Visualization")
    return screen
