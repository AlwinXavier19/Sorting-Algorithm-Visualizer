import pygame
import random
import math

pygame.init()

class VisualizerData:
    DARK_BLUE = (36, 90, 190)
    ORANGE = (255, 140, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    GREY = (160, 160, 160)

    BACKGROUND_COLOR = (0, 0, 0)
    SIDE_PADDING = 100
    TOP_PADDING = 140

    GRADIENT_COLORS = [
        (100, 149, 237),
        (123, 104, 238),
        (72, 209, 204)
    ]

    FONT = pygame.font.SysFont('arial', 18)
    LARGE_FONT = pygame.font.SysFont('arial', 26)

    def __init__(self, width, height, numbers):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sort Visualizer")
        self.set_numbers(numbers)
        self.start_btn = None
        self.newlist_btn = None
        self.asc_btn = None
        self.desc_btn = None

    def set_numbers(self, numbers):
        self.numbers = numbers
        self.min_val = min(numbers)
        self.max_val = max(numbers)
        self.block_width = round((self.width - self.SIDE_PADDING) / len(numbers))
        self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PADDING // 2

def draw_button(window, x, y, width, height, text, font, bg_color, text_color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window, bg_color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    window.blit(text_surf, text_rect)
    return rect

def draw(visualizer, algo_name, ascending):
    visualizer.window.fill(visualizer.BACKGROUND_COLOR)

    title = visualizer.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, visualizer.DARK_BLUE)
    visualizer.window.blit(title, (visualizer.width / 2 - title.get_width() / 2, 10))

    visualizer.start_btn = draw_button(visualizer.window, 100, 60, 120, 40, "Start", visualizer.FONT, visualizer.GREEN, visualizer.BLACK)
    visualizer.newlist_btn = draw_button(visualizer.window, 250, 60, 120, 40, "New List", visualizer.FONT, visualizer.ORANGE, visualizer.BLACK)
    visualizer.asc_btn = draw_button(visualizer.window, 400, 60, 100, 40, "Ascending", visualizer.FONT, visualizer.DARK_BLUE, visualizer.WHITE)
    visualizer.desc_btn = draw_button(visualizer.window, 520, 60, 100, 40, "Descending", visualizer.FONT, visualizer.RED, visualizer.WHITE)

    draw_bars(visualizer)
    pygame.display.update()

def draw_bars(visualizer, color_positions={}, clear_bg=False):
    numbers = visualizer.numbers

    if clear_bg:
        clear_rect = (visualizer.SIDE_PADDING // 2, visualizer.TOP_PADDING,
                      visualizer.width - visualizer.SIDE_PADDING,
                      visualizer.height - visualizer.TOP_PADDING)
        pygame.draw.rect(visualizer.window, visualizer.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(numbers):
        x = visualizer.start_x + i * visualizer.block_width
        y = visualizer.height - (val - visualizer.min_val) * visualizer.block_height

        color = visualizer.GRADIENT_COLORS[i % 3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(visualizer.window, color,
                         (x, y, visualizer.block_width, visualizer.height))

    if clear_bg:
        pygame.display.update()

def generate_random_list(n, max_value, min_value):
    return [random.randint(min_value, max_value) for _ in range(n)]

def bubble_sort(visualizer, ascending=True):
    numbers = visualizer.numbers

    for i in range(len(numbers) - 1):
        for j in range(len(numbers) - 1 - i):
            num1 = numbers[j]
            num2 = numbers[j + 1]

            if (num1 > num2 and ascending) or (num2 > num1 and not ascending):
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                draw_bars(visualizer, {j: visualizer.GREEN, j + 1: visualizer.RED}, True)
                yield True
    return numbers

def insertion_sort(visualizer, ascending=True):
    numbers = visualizer.numbers
    for i in range(1, len(numbers)):
        current = numbers[i]
        j = i - 1

        while j >= 0 and ((numbers[j] > current and ascending) or (numbers[j] < current and not ascending)):
            numbers[j + 1] = numbers[j]
            j -= 1
            draw_bars(visualizer, {j + 1: visualizer.GREEN, i: visualizer.RED}, True)
            yield True

        numbers[j + 1] = current
        draw_bars(visualizer, {j + 1: visualizer.GREEN, i: visualizer.RED}, True)
        yield True
    return numbers

def main():
    run = True
    clock = pygame.time.Clock()

    num_elements = 60
    max_value = 100
    min_value = 10

    numbers = generate_random_list(num_elements, max_value, min_value)
    visualizer = VisualizerData(800, 600, numbers)

    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    algorithm_name = "Bubble Sort"
    sort_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sort_generator)
            except StopIteration:
                sorting = False
        else:
            draw(visualizer, algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if visualizer.start_btn.collidepoint(pos) and not sorting:
                    sorting = True
                    sort_generator = sorting_algorithm(visualizer, ascending)
                elif visualizer.newlist_btn.collidepoint(pos):
                    numbers = generate_random_list(num_elements, max_value, min_value)
                    visualizer.set_numbers(numbers)
                    sorting = False
                elif visualizer.asc_btn.collidepoint(pos) and not sorting:
                    ascending = True
                elif visualizer.desc_btn.collidepoint(pos) and not sorting:
                    ascending = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    algorithm_name = "Bubble Sort"
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    algorithm_name = "Insertion Sort"

    pygame.quit()

if __name__ == "__main__":
    main()
