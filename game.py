import pygame

from time import sleep
from paper import *

SCR_W = 400 # Screen width
SCR_H = 400 # Screen height

B_COLOR = (0x00, 0x00, 0x00) # Background color
G_COLOR = (0x00, 0xFF, 0x00) # Grid color
X_COLOR = (0x00, 0x00, 0xFF) # X player's color
O_COLOR = (0xFF, 0x00, 0x00) # O player's color
Z_COLOR = (0xFF, 0x00, 0xFF) # Z player's color
L_COLOR = (0xFF, 0xFF, 0x00) # Win line color

class Game:

    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.paper = Paper(width, height)
        self.screen = screen

        # Width and Height of the cells on screen
        self.block_w = SCR_W // width
        self.block_h = SCR_H // height

    def run(self):
        self.render(self.screen)
        pygame.display.set_caption('MNK Game')
        player = State.X # First player
        clicked = False # Game renders the paper if this value is True

        #Main Loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = pygame.mouse.get_pressed()
                    if pressed[0]:
                        clicked = self.mark_paper(pygame.mouse.get_pos(), player)
                        player = self.get_next(player)
                elif event.type == pygame.QUIT:
                    return False

            if clicked:
                self.render(self.screen)
                if (self.paper.is_winning()):
                    self.render_win_line(self.screen)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pass # Wait for the winner to celebrate!
                    return True
                
                elif (self.is_finished()):
                    sleep(1)
                    return True
            clicked = False

    def render(self, screen):
        screen.fill(B_COLOR)
        #Draw blocks
        for x in range(0, self.width):
            for y in range(0, self.height):
                block = self.paper.board[x][y]
                if block == State.X:
                    pygame.draw.rect(screen, X_COLOR,
                        pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w))
                elif block == State.O:
                    pygame.draw.rect(screen, O_COLOR,
                        pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w))
                elif block == State.Z:
                    pygame.draw.rect(screen, Z_COLOR,
                        pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w))

        #Draw grid
        for x in range(0, self.width):
            for y in range(0, self.height):
                pygame.draw.rect(screen, G_COLOR, 
                    pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w), 3)
        pygame.display.flip()

    def render_win_line(self, screen):
        start = [
            self.paper.win_start[0] * self.block_h + self.block_h // 2, 
            self.paper.win_start[1] * self.block_w + self.block_w // 2
        ]
        end = [
            self.paper.win_end[0] * self.block_h + self.block_h // 2,
            self.paper.win_end[1] * self.block_w + self.block_w // 2
        ]

        pygame.draw.line(screen, L_COLOR, start, end, 8)
        pygame.display.flip()

    def mark_paper(self, point, state : State):
        point = [
            point[0] // self.block_h, # Horizontal position of the cell
            point[1] // self.block_w  # Vertical position of the cell
        ]
        return self.paper.mark(point, state)

    def reset(self):
        self.paper = Paper(self.width, self.height)

    def get_winner(self):
        return self.paper.last_mark

    def is_finished(self):
        return self.paper.mark_count == BOARD_H * BOARD_W

    def get_next(self, state : State):
        if state == State.X:
            return State.O
        if state == State.O:
            return State.Z
        return State.X

if __name__ == "__main__":
    #Init video system
    pygame.init()
    screen = pygame.display.set_mode((SCR_W, SCR_H))

    #Init mixer
    pygame.mixer.init()
    pygame.mixer.music.load('./sounds/victory.mp3')
    pygame.mixer.music.set_volume(0.2)

    #Start the game
    game = Game(BOARD_W, BOARD_H, screen)
    while True:
        if game.run() == False:
            pygame.quit()
            exit(0)
        game.reset()
