import random

import pygame
from abc import ABCMeta, abstractmethod

pygame.init()
screen = pygame.display.set_mode((1440, 1040), 0)

font = pygame.font.SysFont("arial", 50, True, False)
yellow = (255, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255, 140, 0)
pink = (255, 15, 192)
cyan = (0, 255, 255)
white = (255, 255, 255)
up = 1
down = 2
right = 3
left = 4

class GameBehavior(metaclass=ABCMeta):
    @abstractmethod
    def print(self, tela):
        pass

    @abstractmethod
    def calculate_rules(self):
        pass

    @abstractmethod
    def game_events(self, world_events):
        pass


class Movable(metaclass=ABCMeta):

    @abstractmethod
    def allow_movement(self):
        pass

    @abstractmethod
    def disallow_movement(self,directions):
        pass

    @abstractmethod
    def corner(self, directions):
        pass

class GameWorld(GameBehavior):
    def __init__(self, size, pac):
        self.pacman = pac
        self.movables = []
        self.size = size
        self.score = 0
        #Game States | Playing = 0 | Pause = 1 | Game Over = 2 | Victory = 3
        self.state = 0
        self.life_points = 3
        self.world_array = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def add_movable(self, obj):
        self.movables.append(obj)

    def print_score(self, tela):
        score_x = 30 * self.size
        img_score = font.render("Score: {}".format(self.score), True, yellow)
        img_life  = font.render("Lives:  {}".format(self.life_points),True, yellow)
        tela.blit(img_score, (score_x, 50))
        tela.blit(img_life,(score_x, 100) )

    def print_line(self, tela, number_line, line):
        for column_number, column in enumerate(line):
            x = column_number * self.size
            y = number_line * self.size
            half_size = self.size / 2
            color = black
            if column == 2:
                color = blue
            pygame.draw.rect(tela, color, (x, y, self.size, self.size), 0)
            if column == 1:
                pygame.draw.circle(tela, yellow, (x + half_size, y + half_size), self.size / 10, 0)

    def print(self, tela):
        if self.state == 0:
            self.print_playing(tela)
        elif self.state == 1:
            self.print_playing(tela)
            self.print_paused(tela)
        elif self.state == 2:
            self.print_playing(tela)
            self.print_gameover()
        elif self.state == 3:
            self.print_playing(tela)
            self.print_victory(tela)


    def print_center_text(self, screen, text):
        text_img = font.render(text, True, yellow)
        text_x = (screen.get_width() - text_img.get_width()) // 2
        text_y = (screen.get_height() - text_img.get_height()) // 2
        screen.blit(text_img, (text_x, text_y))


    def print_gameover(self):
        self.print_center_text(screen , "G A M E  O V E R")

    def print_paused(self, tela):
        self.print_center_text(tela , "P A U S E")

    def print_playing(self, tela):
        for number_line, line in enumerate(self.world_array):
            self.print_line(tela, number_line, line)
        self.print_score(tela)

    def print_victory(self, tela):
        self.print_center_text(tela , "V I C T O R Y !")

    def get_directions(self, row, column):
        directions = []
        if self.world_array[int(row - 1)][int(column)] != 2:
            directions.append(up)
        if self.world_array[int(row + 1)][int(column)] != 2:
            directions.append(down)
        if self.world_array[int(row )][int(column - 1 )] != 2:
            directions.append(left)
        if self.world_array[int(row )][int(column + 1 )] != 2:
            directions.append(right)
        return directions

    def calculate_rules(self):
        if self.state == 0:
            self.calculate_rules_playing()
        elif self.state == 1:
            self.calculate_rules_paused()
        elif self.state == 2:
            self.calculate_rules_gameover()


    def calculate_rules_gameover(self):
        pass

    def calculate_rules_paused(self):
        pass

    def calculate_rules_playing(self):
        for movable in self.movables:
            row = int(movable.row)
            column = int(movable.column)
            row_intention = int(movable.row_intention)
            column_intention = int(movable.column_intention)
            directions = self.get_directions(row, column)
            if len(directions) >= 3:
                movable.corner(directions)
            if isinstance(movable, Ghost) and movable.row == self.pacman.row and movable.column == self.pacman.column:
                self.life_points -= 1
                if self.life_points <= 0:
                    self.state = 2
                else:
                    self.pacman.row = 1
                    self.pacman.column = 1
            else:
                if 0 <= column_intention < 28 and 0 <= row_intention < 29 and self.world_array[row_intention][column_intention] !=2:
                    movable.allow_movement()
                    if isinstance(movable,Pacman) and self.world_array[row][column] == 1:
                        self.score += 1
                        self.world_array[row][column] = 0
                        if self.score >= 306:
                            self.state = 3
                else:
                    movable.disallow_movement(directions)



    def game_events(self, world_events):
        for e in world_events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.state == 0:
                        self.state = 1
                    else:
                        self.state = 0

class Pacman(GameBehavior, Movable):
    side_right = True
    max_speed = 1

    def __init__(self, tamanho):
        self.column = 1
        self.row = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.raio = self.tamanho // 2
        self.speed_x = 0
        self.speed_y = 0
        self.column_intention = self.column
        self.row_intention = self.row
        self.mouth_opening = 0
        self.mouth_opening_speed = 1

    def calculate_rules(self):
        self.column_intention = self.column + self.speed_x
        self.row_intention = self.row + self.speed_y
        self.centro_x = int(self.column * self.tamanho + self.raio)
        self.centro_y = int(self.row * self.tamanho + self.raio)

    def print(self, tela):
        # Body
        pygame.draw.circle(tela, yellow, (self.centro_x, self.centro_y), self.raio, 0)

        # Mouth
        self.mouth_opening += self.mouth_opening_speed
        if self.mouth_opening > self.raio:
            self.mouth_opening_speed = - 1
        if self.mouth_opening <= 0:
            self.mouth_opening_speed = 1

        mounth_corner = (self.centro_x, self.centro_y)

        if self.side_right:
            upper_lip = (self.centro_x + self.raio, self.centro_y - self.mouth_opening)
            lower_lip = (self.centro_x + self.raio, self.centro_y + self.mouth_opening)
            mouth_points = [mounth_corner, upper_lip, lower_lip]

            pygame.draw.polygon(tela, black, mouth_points, 0)

            # Eyes

            eye_x = int(self.centro_x + self.raio / 3)
            eye_y = int(self.centro_y - self.raio * 0.70)
            eye_raio = int(self.raio / 5)
            pygame.draw.circle(tela, black, (eye_x, eye_y), eye_raio, 0)

        else:
            upper_lip = (self.centro_x - self.raio, self.centro_y - self.mouth_opening)
            lower_lip = (self.centro_x - self.raio, self.centro_y + self.mouth_opening)
            mouth_points = [mounth_corner, upper_lip, lower_lip]

            pygame.draw.polygon(tela, black, mouth_points, 0)

            # Eyes

            eye_x = int(self.centro_x - self.raio / 3)
            eye_y = int(self.centro_y - self.raio * 0.70)
            eye_raio = int(self.raio / 5)
            pygame.draw.circle(tela, black, (eye_x, eye_y), eye_raio, 0)

    def game_events(self, events):

        # Captura os eventos
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = Pacman.max_speed
                    self.side_right = True
                elif e.key == pygame.K_LEFT:
                    self.speed_x = - Pacman.max_speed
                    self.side_right = False
                elif e.key == pygame.K_UP:
                    self.speed_y = - Pacman.max_speed
                elif e.key == pygame.K_DOWN:
                    self.speed_y = + Pacman.max_speed

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = 0
                elif e.key == pygame.K_LEFT:
                    self.speed_x = 0
                elif e.key == pygame.K_UP:
                    self.speed_y = 0
                elif e.key == pygame.K_DOWN:
                    self.speed_y = 0

    def allow_movement(self):
        self.row = self.row_intention
        self.column = self.column_intention

    def disallow_movement(self,directions):
        self.row_intention = self.row
        self.column_intention = self.column

    def corner(self, directions):
        pass

class Ghost(GameBehavior):
    def __init__(self, ghost_color, size):
        self.column = 13.0
        self.row = 15.0
        self.speed = 1
        self.row_intention = self.row
        self.column_intention = self.column
        self.direction = up
        self.size = size
        self.ghost_color = ghost_color

    def print(self, tela):
        slice = self.size / 8
        px = int(self.column * self.size)
        py = int(self.row * self.size)
        outline = [(px, py + self.size),
                   (px + slice, py + slice * 2 ),
                   (px + slice * 2, py + slice / 2),
                   (px + slice * 3, py),
                   (px + slice * 5, py),
                   (px + slice * 6, py + slice / 2),
                   (px + slice * 7, py + slice * 2),
                   (px +self.size, py + self. size)]
        pygame.draw.polygon(tela, self.ghost_color, outline, 0)

        eye_raio_ext = slice
        eye_raio_int = slice // 2

        eye_left_x = int(px + slice * 2.5)
        eye_left_y = int(py + slice * 2.5)

        eye_right_x = int(px + slice * 5.5)
        eye_right_y = int(py + slice * 2.5)

        pygame.draw.circle(tela, white, (eye_left_x, eye_left_y), eye_raio_ext, 0)
        pygame.draw.circle(tela, black, (eye_left_x, eye_left_y), eye_raio_int, 0)
        pygame.draw.circle(tela, white, (eye_right_x, eye_right_y), eye_raio_ext, 0)
        pygame.draw.circle(tela, black, (eye_right_x, eye_right_y), eye_raio_int, 0)


    def calculate_rules(self):
        if self.direction == up:
            self.row_intention -= self.speed
        elif self.direction == down:
            self.row_intention += self.speed
        elif self.direction == left:
            self.column_intention -= self.speed
        elif self.direction == right:
            self.column_intention += self.speed

    def change_direction(self, directions):
        self.direction = random.choice(directions)

    def corner(self, directions):
        self.change_direction(directions)

    def allow_movement(self):
        self.row = self.row_intention
        self.column = self.column_intention

    def disallow_movement(self, directions):
        self.row_intention = self.row
        self.column_intention = self.column
        self.change_direction(directions)

    def game_events(self, events):
        pass


if __name__ == "__main__":
    size = 1080 // 30
    pacman = Pacman(size)
    blinky = Ghost(red, size)
    inky = Ghost(cyan,size)
    cylde = Ghost(orange,size)
    pinky = Ghost(pink,size)
    game_world = GameWorld(size, pacman)
    game_world.add_movable(pacman)
    game_world.add_movable(blinky)
    game_world.add_movable(inky)
    game_world.add_movable(cylde)
    game_world.add_movable(pinky)


    while True:
        # Calcular as regras
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        cylde.calculate_rules()
        pinky.calculate_rules()
        game_world.calculate_rules()

        # Printar a tela
        screen.fill(black)
        game_world.print(screen)
        pacman.print(screen)
        blinky.print(screen)
        inky.print(screen)
        cylde.print(screen)
        pinky.print(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Captura os eventos
        events = pygame.event.get()
        game_world.game_events(events)
        pacman.game_events(events)
        # pacman.game_events_mouse(events)
