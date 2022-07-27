import enum
import numpy as np

BOARD_W = 3 # Number of vertical cells (M value)
BOARD_H = 3 # Number of horizontal cells (N value)
WIN_C = 3   # Number of cells in a row to win (K value)

class State(enum.Enum):
    N = -1 # Invalid Position
    E = 0  # Empty Block
    X = 1  # X Block
    O = 2  # O Block


class Paper:

    def __init__(self, width : int, height : int):
        self.width : int = width
        self.height : int = height
        self.board = np.array([State.E] * width * height).reshape((width, height))
        self.win_start = np.zeros(2, dtype=int)
        self.win_end = np.zeros(2, dtype=int)
        self.last_marked = np.zeros(2, dtype=int)
        self.last_mark : State = State.E
        self.mark_count : int = 0

    def mark(self, point, state : State):
        current_state = self.board[point[0]][point[1]]
        if current_state == State.E:
            self.board[point[0]][point[1]] = state
            self.last_marked = point
            self.last_mark = state
            self.mark_count += 1
            return True
        return False

    def get(self, point):
        if (point[0]  >= self.height or
            point[0] < 0 or
            point[1] >= self.width or
            point[1] < 0):
            return State.N
        return self.board[point[0]][point[1]]

    def is_winning(self):
        if (self._diag_win(self.last_marked, self.last_mark)):
            return True
        if (self._vert_win(self.last_marked, self.last_mark)):
            return True
        if (self._horiz_win(self.last_marked, self.last_mark)):
            return True
        return False


    def _diag_win(self, point, state : State):
        _rng : int = WIN_C - 1

        start_neg = [point[0] - _rng, point[1] - _rng]
        consec_count = 0
        for i in range(2 * _rng + 1):
            if (self.get(start_neg) == state):
                consec_count += 1
                if consec_count == WIN_C:
                    self.win_start = [start_neg[0] - _rng, start_neg[1] - _rng]
                    self.win_end = start_neg
                    return True
            else:
                consec_count = 0
            start_neg = [start_neg[0] + 1, start_neg[1] + 1]

        start_pos = [point[0] - _rng, point[1] + _rng]
        consec_count = 0
        for i in range(2 * _rng + 1):
            if (self.get(start_pos) == state):
                consec_count += 1
                if consec_count == WIN_C:
                    self.win_start = [start_pos[0] - _rng, start_pos[1] + _rng]
                    self.win_end = start_pos
                    return True
            else:
                consec_count = 0
            start_pos[0] += 1
            start_pos[1] -= 1


    def _vert_win(self, point, state : State):
        _rng = WIN_C - 1
        start = [point[0] - _rng, point[1]]
        consec_count = 0
        for i in range(2 * _rng + 1):
            if (self.get(start) == state):
                consec_count += 1
                if consec_count == WIN_C:
                    self.win_start = [start[0] - _rng, start[1]]
                    self.win_end = start
                    return True
            else:
                consec_count = 0
            start[0] += 1

    def _horiz_win(self, point, state : State):
        _rng = WIN_C - 1
        start = [point[0], point[1] - _rng]
        consec_count = 0
        for i in range(2 * _rng + 1):
            if (self.get(start) == state):
                consec_count += 1
                if consec_count == WIN_C:
                    self.win_start = [start[0], start[1] - _rng]
                    self.win_end = start
                    return True
            else:
                consec_count = 0
            start[1] += 1