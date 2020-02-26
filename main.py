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
trans = (1, 1, 1)
orange = (200, 100, 50)

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


# ----------------------------------------------------------------------------#
# Slider class from:
# https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/
class Slider():
    def __init__(self, name, val, maxi, mini, pos):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 450
        self.surf = pygame.surface.Surface((150, 75))
        # the hit attribute indicates slider movement due to mouse interaction
        self.hit = False
        font = pygame.font.SysFont("comicsans", 20)
        self.txt_surf = font.render(name, 1, white)
        self.txt_rect = self.txt_surf.get_rect(center=(75, 25))

        # Static graphics - slider background #
        self.surf.fill(turquoise)
        pygame.draw.rect(self.surf, black, [0, 0, 150, 75], 3)
        pygame.draw.rect(self.surf, black, [6, 15, 138, 20], 0)
        pygame.draw.rect(self.surf, white, [15, 45, 120, 8], 0)
        # this surface never changes
        self.surf.blit(self.txt_surf, self.txt_rect)

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((50, 55))
        self.button_surf.fill(trans)
        self.button_surf.set_colorkey(trans)
        pygame.draw.circle(self.button_surf, black, (25, 42), 9, 0)

    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        pos = (15+int((self.val-self.mini)/(self.maxi-self.mini)*120), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        # move of button box to correct screen position
        self.button_rect.move_ip(self.xpos, self.ypos)

        # screen
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 15) \
                   / 120 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


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
    speed.draw()
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
buttons = [bubble_button, select_button, insert_button, quick_button,
           merge_button, radix_button, bogo_button, start_button]
speed = Slider("Animation slowdown", 0.0001, 0.2, 0.0001, 100)


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
                if speed.button_rect.collidepoint(pos):
                    speed.hit = True

            if event.type == pygame.MOUSEMOTION:
                for s in buttons:
                    if s.is_over(pos):
                        s.color = light_turquoise
                    else:
                        s.color = turquoise

            if event.type == pygame.MOUSEBUTTONUP:
                    speed.hit = False

        if speed.hit:
            speed.move()


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
        time.sleep(speed.val)

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
