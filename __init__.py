import pygame
from time import sleep

frameRate = 0.1


class Figure:
    def __init__(self,shape, x, y, width, cuadrant, color=(250,250,250)):
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.color = color
        self.shape = shape
        self.cuadrant = cuadrant

    def draw(self, screen, background=(0,0,0)):

        if self.shape == "x":
            start_pos = self.x - self.width/2, self.y - self.width/2
            end_pos = self.x + self.width/2, self.y + self.width/2
            draw_line(screen, self.color, 
                start_pos,
                end_pos, 5)
            start_pos = self.x - self.width/2, self.y + self.width/2
            end_pos = self.x + self.width/2, self.y - self.width/2
            draw_line(screen, self.color, 
                start_pos,
                end_pos, 5)
            
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.width/2))
            pygame.draw.circle(screen, background, (self.x, self.y), int(self.width/2)-5)


class Board:
    
    def __init__(self, color=(25,25,25)):
        self.width = 500
        self.height = 500
        self.color = color
        self.screen = None
        self.__figures = []
        self.winner = None


    def get_figures(self):
        return self.__figures

    
    def add_figure(self, figure):
        if not self.winner or not figure.cuadrant in [figure.cuadrant for figure in self.__figures]:
            self.__figures.append(figure)


    def start(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.color)

    def reset(self):
        self.winner = None
        self.__figures = []


    def draw(self):

        start_coordintes = [(0, self.height/3), (self.width/3, 0), (2*self.width/3, 0), (0, 2*self.height/3)]
        end_coordinates = [(self.width, self.height/3), (self.width/3, self.height), (2*self.width/3, self.height), (self.width, 2*self.height/3)]
        draw_line(self.screen, (250,250,250), start_coordintes, end_coordinates, 5)
        

        if self.__figures:
            for figure in self.__figures:
                figure.draw(self.screen, background=self.color)

        winner = self.check_winner()
        if winner:
            
            start_pos = (winner[0].x, winner[0].y)
            end_pos = (winner[-1].x, winner[-1].y)
            draw_line(self.screen, (250,0,0), start_pos, end_pos, 5)

    def check_winner(self):
        for i in range(1,4):
            # Check Columns
            figures = [figure for figure in self.__figures if figure.cuadrant[0] == i]
            figures = sorted(figures, key=lambda figure: figure.cuadrant[1])
            if len(figures)== 3 and all([figure.shape == figures[0].shape for figure in figures]):
                self.winner = figures[0]
                return figures

            # Check Rows
            figures = [figure for figure in self.__figures if figure.cuadrant[1] == i]
            figures = sorted(figures, key=lambda figure: figure.cuadrant[0])
            if len(figures)== 3 and all([figure.shape == figures[0].shape for figure in figures]):
                self.winner = figures[0]
                return figures

        # Check Diagonal \
        figures = [figure for figure in self.__figures if figure.cuadrant[0] == figure.cuadrant[1]]
        figures = sorted(figures, key=lambda figure: figure.cuadrant[1])
        if len(figures) ==3 and all([figure.shape == figures[0].shape for figure in figures]):
            self.winner = figures[0]
            return figures

        # Check Anti diagonal /
        figures = [figure for figure in self.__figures if sum(figure.cuadrant)==4]
        figures = sorted(figures, key=lambda figure: figure.cuadrant[1])
        
        if len(figures) ==3 and all([figure.shape == figures[0].shape for figure in figures]):
            self.winner = figures[0]
            return figures



    def get_cuadrant(self, cuadrant_pos):
        cuadrant_center = [0,0]
        cuadrant = [0,0]
        pos_x, pos_y = cuadrant_pos
        cuadrant_x = pos_x/self.width
        cuadrant_y = pos_y/self.width
        if cuadrant_x <= 0.33:
            cuadrant_center[0] = self.width / 6
            cuadrant[1] = 1
        elif cuadrant_x >= 0.66:
            cuadrant_center[0] = 5* self.width / 6
            cuadrant[1] = 3
        else:
            cuadrant_center[0] = 3*self.width / 6
            cuadrant[1] = 2
        if cuadrant_y <= 0.33:
            cuadrant_center[1] = self.width / 6
            cuadrant[0] = 1
        elif cuadrant_y >= 0.66:
            cuadrant_center[1] = 5* self.width / 6
            cuadrant[0] = 3
        else:
            cuadrant_center[1] = 3*self.width / 6
            cuadrant[0] = 2

        return {"center_pos": tuple(cuadrant_center), "cuadrant": tuple(cuadrant)}

def draw_line(screen, color, start_pos, end_pos, width):

    if type(start_pos) is list or type(end_pos) is list:
        if len(start_pos) != len(end_pos):
            raise Exception("The length of the start coordinate list is not equal to the length of the end coordinate list")

        for i in range(len(start_pos)):
            pygame.draw.line(screen, color, start_pos[i], end_pos[i], width)
    else:
        pygame.draw.line(screen, color, start_pos, end_pos, width)


if __name__ == '__main__':
    board = Board()
    board.start()   

    while True:
        pygame.event.pump()
        board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        click = pygame.mouse.get_pressed()
        
        if sum(click) > 0:
            cuadrant = board.get_cuadrant(pygame.mouse.get_pos())
            if click[0]:
                
                shape = "x" if len(board.get_figures()) % 2 == 0 else "o"
                figure = Figure(
                    shape, 
                    cuadrant["center_pos"][0], cuadrant["center_pos"][1], 
                    board.width/4, cuadrant["cuadrant"])
                board.add_figure(figure)   

        pygame.display.update()
        sleep(frameRate)
    