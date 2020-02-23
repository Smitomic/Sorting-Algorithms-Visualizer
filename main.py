import sys
import pygame
from sorts import *
import time
from random import randint, shuffle

unsorted_array = list(randint(0, 10000) for _ in range(100))
shuffle(unsorted_array)
algorithm = bubble_sort
mainClock = pygame.time.Clock()
size = width, height = 1000, 600
pygame.init()
screen = pygame.display.set_mode(size)
white = (255, 255, 255)
black = (0, 0, 0)
turquoise = (0, 180, 180)
light_turquoise = (0, 230, 230)
green = (0, 255, 0)
red = (255, 0, 0)

start = 1
compare = 2
move = 3
complete = 4


# ----------------------------------------------------------------------------#
class Button:
    def __init__(self, color, x, y, b_width, b_height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = b_width
        self.height = b_height
        self.text = text
        self.placement = (x, y, b_width, b_height)

    def draw(self, surface):
        pygame.draw.rect(screen, black, (
            self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(surface, self.color, self.placement, 0)
        if self.text != "":
            font = pygame.font.SysFont('comicsans', 24)
            text = font.render(self.text, 1, black)
            surface.blit(text,
                         (self.x + (self.width / 2 - text.get_width() / 2),
                          self.y + (self.height / 2 - text.get_height() / 2))
                         )

    def is_over(self, pos):
        # Pos is the mouse position
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


selected_sort = 'Bubble sort'


def redraw_menu():
    screen.fill(white)
    bubble_button.draw(screen)
    select_button.draw(screen)
    insert_button.draw(screen)
    quick_button.draw(screen)
    merge_button.draw(screen)
    radix_button.draw(screen)
    bogo_button.draw(screen)
    start_button.draw(screen)
    pygame.draw.rect(screen, black, (0, (height - (height - 200)) - 2,
                                     width + 4, height - 400 + 4))
    pygame.draw.rect(screen, turquoise, (0, (height - (height - 200)),
                                         width, height - 400))
    head_font = pygame.font.SysFont('comicsans', 50)
    text = head_font.render('Sorting algorithm visualizer', 1, black)
    screen.blit(text, (0 + (width / 2 - text.get_width() / 2),
                       (height - (height - 200)) +
                       ((height - 400) / 2 - text.get_height() / 2)))
    font = pygame.font.SysFont('comicsans', 24)
    text2 = font.render(f'Currently selected sort: {selected_sort}', 1, black)
    screen.blit(text2, (100 + (width / 2 - text.get_width() / 2),
                        (height - 200) +
                        ((height - 400) / 2 - text.get_height() / 2)))


# -----------------------------------------------------------------------------#
bubble_button = Button(turquoise, 30, 10, 100, 35, "Bubble sort")
select_button = Button(turquoise, 160, 10, 115, 35, "Selection sort")
insert_button = Button(turquoise, 305, 10, 115, 35, "Insertion sort")
quick_button = Button(turquoise, 450, 10, 100, 35, "Quicksort")
merge_button = Button(turquoise, 580, 10, 100, 35, "Merge sort")
radix_button = Button(turquoise, 710, 10, 100, 35, "Radix sort")
bogo_button = Button(turquoise, 840, 10, 100, 35, "Bogo sort")
start_button = Button(turquoise, width / 2 - 50, height - 45, 100, 35, "Start")


def menu():
    global selected_sort
    while True:
        redraw_menu()
        pygame.display.update()
        global algorithm

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN) and \
                    (event.key == pygame.K_ESCAPE):
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(pos):
                    animation(unsorted_array)
                if bubble_button.is_over(pos):
                    algorithm = bubble_sort
                    selected_sort = 'Bubble sort'
                if select_button.is_over(pos):
                    algorithm = selection_sort
                    selected_sort = 'Selection sort'
                if insert_button.is_over(pos):
                    algorithm = insertion_sort
                    selected_sort = 'Insertion sort'
                if quick_button.is_over(pos):
                    algorithm = quick_sort
                    selected_sort = 'Quicksort'
                if merge_button.is_over(pos):
                    algorithm = merge_sort
                    selected_sort = 'Merge sort'
                if radix_button.is_over(pos):
                    algorithm = radix_sort
                    selected_sort = 'Radix sort'
                if bogo_button.is_over(pos):
                    algorithm = bogo_sort
                    selected_sort = 'Bogo sort'

            if event.type == pygame.MOUSEMOTION:
                if start_button.is_over(pos):
                    start_button.color = light_turquoise
                else:
                    start_button.color = turquoise
                if bubble_button.is_over(pos):
                    bubble_button.color = light_turquoise
                else:
                    bubble_button.color = turquoise
                if select_button.is_over(pos):
                    select_button.color = light_turquoise
                else:
                    select_button.color = turquoise
                if insert_button.is_over(pos):
                    insert_button.color = light_turquoise
                else:
                    insert_button.color = turquoise
                if quick_button.is_over(pos):
                    quick_button.color = light_turquoise
                else:
                    quick_button.color = turquoise
                if merge_button.is_over(pos):
                    merge_button.color = light_turquoise
                else:
                    merge_button.color = turquoise
                if bogo_button.is_over(pos):
                    bogo_button.color = light_turquoise
                else:
                    bogo_button.color = turquoise
                if radix_button.is_over(pos):
                    radix_button.color = light_turquoise
                else:
                    radix_button.color = turquoise


# -----------------------------------------------------------------------------#
back_button = Button(turquoise, 10, 10, 120, 35, "Back to menu")


def animation(array):
    global unsorted_array
    line_width = width // 100
    line_height = height / 10000
    action = start
    screen.fill(white)
    pygame.display.update()
    if algorithm == quick_sort:
        generator = quick_sort(unsorted_array, 0, len(unsorted_array) - 1)
    elif algorithm == merge_sort:
        generator = merge_sort(unsorted_array, 0, len(unsorted_array) - 1)
    else:
        generator = algorithm(unsorted_array)

    while True:
        pygame.display.update()
        time.sleep(0.01)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_over(pos):
                    unsorted_array = list(
                        randint(0, 10000) for _ in range(100))
                    shuffle(unsorted_array)
                    menu()
            if event.type == pygame.MOUSEMOTION:
                if back_button.is_over(pos):
                    back_button.color = light_turquoise
                else:
                    back_button.color = turquoise

        if action != complete:
            sorted_array, action, i, j = next(generator)

        screen.fill(white)
        for index, element in enumerate(array):
            color = turquoise
            if index == i or index == j:
                if action == move:
                    color = red
                elif action == compare:
                    color = green

            pygame.draw.line(screen, color,
                             (line_width / 2 + (index * line_width),
                              height),
                             (line_width / 2 + (index * line_width),
                              height - (element * line_height)), line_width)
        back_button.draw(screen)


menu()
