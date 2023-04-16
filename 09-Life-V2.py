import pygame
from sys import exit
from random import randint
import math
import time


class Field():
    def __init__(self, field_w: int, field_h: int, grid_width: int, point_w: int, point_h: int, display) -> None:
        self.field_w = field_w
        self.field_h = field_h
        self.grid_width = grid_width
        self.point_w = point_w
        self.point_h = point_h
        self.display = display
        self.play_field = []
        for a in range(field_h+2):
            self.play_field.append([])
            for b in range(field_w+2):
                self.play_field[a].append(
                    Point(b, a, self.play_field))

    def look_next_step(self):
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                if self.play_field[a][b].status_need_to_check:
                    # print(b,a)
                    self.play_field[a][b].check_future()

    def change_point_status(self, field_x, field_y):
        x = math.trunc(field_x/self.point_w)
        y = math.trunc(field_y/self.point_h)
        print("Меняем кв: ", x, y)
        if self.play_field[y][x].status:
            self.play_field[y][x].set_status(False)
        else:
            self.play_field[y][x].set_status(True)

    def set_rnd_status(self):
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                self.play_field[a][b].set_status(bool(randint(0, 1)))

    def change_field_status(self):
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                self.play_field[a][b].change_status()
                # print(a,b,self.play_field[a][b].x,self.play_field[a][b].y)

    def draw_field(self):
        # pygame.draw.rect(self.display, (100, 100, 100), (50, 50, 100, 100))
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                if self.play_field[a][b].status and self.play_field[a][b].need_to_draw:
                    pygame.draw.rect(self.display, (100, 100, 100),
                                     (b*self.point_w, a*self.point_h, self.point_w, self.point_h))
                if not self.play_field[a][b].status and self.play_field[a][b].need_to_draw:
                    pygame.draw.rect(self.display, (255, 255, 255),
                                     (b*self.point_w, a*self.point_h, self.point_w, self.point_h))


class Point():
    def __init__(self, x, y, play_field) -> None:
        self.x = x
        self.y = y
        self.play_field = play_field
        self.status = False
        self.future_status = False
        self.status_need_to_check = False
        self.future_status_need_to_check = False
        self.neighbours = 0
        self.need_to_draw = True

    def check_future(self):
        neighbours = 0
        # self.future_status_need_to_check = False

        for a in range(self.y-1, self.y+2):
            for b in range(self.x-1, self.x+2):
                if not (a == self.y and b == self.x):
                    neighbours += self.play_field[a][b].status

        if self.status and neighbours in [2, 3]:
            self.future_status = True
        elif self.status and not neighbours in [2, 3]:
            self.future_status = False
        elif not self.status and neighbours == 3:
            self.future_status = True
        else:
            self.future_status = False

        if self.future_status != self.status:
            self.tell_the_neighbors_to_check_themselv('future')
        return self.future_status

    def change_status(self):
        self.need_to_draw = True if self.status != self.future_status else False
        self.status = self.future_status
        self.status_need_to_check = self.future_status_need_to_check
        self.future_status_need_to_check=False

    def set_status(self, status):
        if self.status != status:
            self.status = status
            self.tell_the_neighbors_to_check_themselv('now')
            self.status_need_to_check=True

    def tell_the_neighbors_to_check_themselv(self, when):
        for a in range(self.y-1, self.y+2):
            for b in range(self.x-1, self.x+2):
                if not (a == self.y and b == self.x):
                    if when == 'now':
                        self.play_field[a][b].status_need_to_check = True
                    elif when == 'future':
                        self.play_field[a][b].future_status_need_to_check = True


w = 1000
h = 1000
time_s = 0
time_f = 0
duration_look_next_step = 0
duration_change_field_status = 0
duration_draw_field = 0
duration_update_screen = 0
pygame.init()
display = pygame.display.set_mode((w+8, h+8))
game_field = Field(w, h, 1, 1, 1, display)
game_field.set_rnd_status()
# with open("fi")
display.fill((255, 255, 255))
game_field.draw_field()
start_game = False
i=0
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < 20 and y < 20:
                start_game = True
                time_s=time.time()
            game_field.change_point_status(x, y)
            game_field.draw_field()
            print("MOUSEBUTTONDOWN:")
            print(event.pos)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if start_game:
        i+=1
        # time_s=time.time()
        game_field.look_next_step()
        # time_f=time.time()
        # duration_look_next_step=time_f-time_s
        # time_s=time.time()
        game_field.change_field_status()
        # time_f=time.time()
        # duration_change_field_status=time_f-time_s
        # time_s=time.time()
        game_field.draw_field()
        # time_f=time.time()
        # duration_draw_field=time_f-time_s
        if i%100 == 0:
            print (f"Iteration: {i}, time: {time.time()-time_s}")
    # time_s=time.time()
    pygame.display.update()
    # time_f=time.time()
    # duration_update_screen=time_f-time_s
    # print(f"Duration: (look_next_step:{round(duration_look_next_step, 2)})  (change_field_status:{round(duration_change_field_status,2)})  (draw_field:{round(duration_draw_field,2)})   (duration_update_screen:{round(duration_update_screen,3)})")
