import pygame
from sys import exit
from random import randint
import math



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
                self.play_field[a].append(Point(b, a, self.play_field))

    def look_next_step(self):
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                self.play_field[a][b].check_future()

    def change_point_status(self,field_x,field_y):
        x=math.trunc(field_x/self.point_w)
        y=math.trunc(field_y/self.point_h)
        print("Меняем кв: ",x,y)
        if self.play_field[y][x].status:
            self.play_field[y][x].set_status(False)
        else:
            self.play_field[y][x].set_status(True)

    def set_rnd_status(self):
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                self.play_field[a][b].set_status(randint(0,1))


    def change_field_status(self):
        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                self.play_field[a][b].change_status()

    def draw_field(self):
        # pygame.draw.rect(self.display, (100, 100, 100), (50, 50, 100, 100))

        for a in range(1, self.field_h):
            for b in range(1, self.field_w):
                if self.play_field[b][a].status and self.play_field[b][a].need_to_draw:
                    pygame.draw.rect(self.display, (100, 100, 100), (a*self.point_w, b*self.point_h, self.point_w, self.point_h))
                if not self.play_field[b][a].status and self.play_field[b][a].need_to_draw:
                    pygame.draw.rect(self.display, (255, 255, 255), (a*self.point_w, b*self.point_h, self.point_w, self.point_h))


class Point():
    def __init__(self, x, y, play_field) -> None:
        self.x = x
        self.y = y
        self.play_field = play_field
        self.status = False
        self.future_status = False
        self.need_to_draw = True

    def check_future(self):
        neighbours = 0
        for a in range(self.y-1, self.y+2):
            for b in range(self.x-1, self.x+2):
                neighbours += self.play_field[a][b].status
        neighbours -= self.status
        if self.status and neighbours in [2, 3]:
            self.future_status = True
        elif self.status and not neighbours in [2, 3]:
            self.future_status = False
        elif not self.status and neighbours == 3:
            self.future_status = True
        else:
            self.future_status = False
        return self.future_status

    def change_status(self):
        self.need_to_draw = True if self.status != self.future_status else False
        self.status = self.future_status

    def set_status(self, status):
        self.status=status

w=200
h=200
pygame.init()
display = pygame.display.set_mode((w+8, h+8))
game_field = Field(w, h, 1, 4, 4, display)
game_field.set_rnd_status()
display.fill((255, 255, 255))
game_field.draw_field()
start_game=False
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=event.pos
            if x<20 and y<20:
                start_game=True
            game_field.change_point_status(x,y)
            game_field.draw_field()
            print("MOUSEBUTTONDOWN:")
            print(event.pos)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if start_game:
        game_field.look_next_step()
        game_field.change_field_status()
        game_field.draw_field()
    pygame.display.update()
