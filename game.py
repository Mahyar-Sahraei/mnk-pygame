import pygame

from paper import *

SCR_W = 400
SCR_H = 400
BOARD_W = 3
BOARD_H = 3

class Game:

    def __init__(self, width, height, screen):
        self.paper = Paper(width, height)
        self.screen = screen
        self.block_w = SCR_W // width
        self.block_h = SCR_H // height

    def run(self):
        #Buffers
        player = State.X
        winner = State.E
        clicked = True

        #Main Loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = pygame.mouse.get_pressed()
                    if pressed[0]:
                        game.mark_paper(pygame.mouse.get_pos(), player)
                        player = get_next(player)
                        clicked = True
                elif event.type == pygame.QUIT:
                    return
            if clicked:
                game.render(screen)
                if (game.paper.is_winning()):
                    winner = game.get_winner()
                    game.render_win_line(screen)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pass
                    break
                elif (game.is_finished()):
                    break
            clicked = False

        #Show result and wait for close event
        game.render_results(screen, winner)
        self._wait()

    def mark_paper(self, point, state : State):
        x = point[0] / self.block_h
        y = point[1] / self.block_w
        point = [x, y]
        self.paper.mark(point, state)

    def reset(self):
        for row in self.paper.board:
            for point in row:
                point = State.E

    def render(self, screen):
        #Draw blocks
        for x in range(0, self.paper.width):
            for y in range(0, self.paper.height):
                block = self.paper.board[x][y]
                if block == State.X:
                    pygame.draw.rect(screen, (0, 0, 255),
                        pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w))
                elif block == State.O:
                    pygame.draw.rect(screen, (255, 0, 0),
                        pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w))

        #Draw grid
        for x in range(0, self.paper.width):
            for y in range(0, self.paper.height):
                pygame.draw.rect(screen, (0, 255, 0), 
                    pygame.Rect(x * self.block_h, y * self.block_w, self.block_h, self.block_w), 3)
        pygame.display.flip()

    def render_win_line(self, screen):
        start = [self.paper.win_start[0] * self.block_h + self.block_h // 2, 
                 self.paper.win_start[1] * self.block_w + self.block_w // 2]
        end = [self.paper.win_end[0] * self.block_h + self.block_h // 2,
               self.paper.win_end[1] * self.block_w + self.block_w // 2]
        pygame.draw.line(screen, (255, 255, 0), start, end, 8)
        pygame.display.flip()

    def render_results(self, screen, winner : State):
        font = pygame.font.Font('./fonts/arial.ttf', 36)
        if (winner == State.E):
            text = font.render('Draw', True, (180, 100, 0))
        elif (winner == State.X):
            text = font.render('Blue Player Won!', True, (180, 100, 0))
        else:
            text = font.render('Red Player Won!', True, (180, 100, 0))

        screen.fill((0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCR_W // 2, SCR_H // 2)
        screen.blit(text, text_rect)
        pygame.display.set_caption('Result')
        pygame.display.flip()


    def get_winner(self):
        return self.paper.last_mark

    def is_finished(self):
        return self.paper.mark_count == BOARD_H * BOARD_W

    def _wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return


def get_next(state : State):
    if state == State.X:
        return State.O
    return State.X

if __name__ == "__main__":
    #Init video system
    pygame.init()
    screen = pygame.display.set_mode((SCR_W, SCR_H))
    pygame.display.set_caption('XO Game')

    #Init mixer
    pygame.mixer.init()
    pygame.mixer.music.load('./sounds/victory.mp3')
    pygame.mixer.music.set_volume(0.2)

    #Start the game
    game = Game(BOARD_W, BOARD_H, screen)
    game.run()

    #Exit pygame
    pygame.quit()
