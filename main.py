from random import randrange, sample
from enum import Enum, auto
from functools import cached_property
from dataclasses import dataclass


@dataclass
class Presets:
    bomb_count: int
    rows: int
    cols: int


class Level(Enum):
    EASY = auto()
    DIFFICULT = auto()


LEVEL_CONFIGS = {Level.EASY: Presets(10, 10, 10)}


class Board:
    def __init__(self):
        self.set_difficulty(Level.EASY)
        self._board = [None for i in range(self.grid_size)]
        self.load_new_bombs()
        self.load_cell_numbers()
        self.board_visibility_mask = [False for i in range(self.grid_size)]

    @property
    def board(self):
        return self._board

    @cached_property
    def grid_size(self):
        return self._rows * self._cols

    def set_difficulty(self, level: Level):
        presets = LEVEL_CONFIGS[level]
        self._bomb_count = presets.bomb_count
        self._rows = presets.rows
        self._cols = presets.cols

    def load_new_bombs(self):
        self._loaded_cells = sample(range(self.grid_size), self._bomb_count)
        for i in self._loaded_cells:
            self.board[i] = "💣"

    def load_cell_numbers(self):
        for row in range(self._rows):
            for col in range(self._cols):
                index = row * self._cols + col
                if index in self._loaded_cells:
                    continue
                neighbor_indices = self.get_neighbor_indices(row, col)
                edge_col = col in [0, self._cols]

    def get_neighbor_indices(self, row, col):
        i = row * self._cols + col
        neighbor_indices = [
            (prev_row := i - self._cols) - 1,
            prev_row,
            prev_row + 1,
            i - 1,
            i + 1,
            (next_row := i + self._cols) - 1,
            next_row,
            next_row + 1,
        ]

        if col == 0:
            neighbor_indices[0] = neighbor_indices[3] = neighbor_indices[5] = -1
        if col == self._cols:
            neighbor_indices[2] = neighbor_indices[4] = neighbor_indices[8] = -1

        nearby_bomb_count = len(set(self._loaded_cells).intersection(neighbor_indices))
        self.board[i] = nearby_bomb_count

    def print_board(self, debug=True):
        display_board = [
            x if self.board_visibility_mask[i] else "X"
            for i, x in enumerate(self.board)
        ]
        for row in range(self._rows):
            board = display_board if not debug else self.board
            print(
                "  ".join(
                    map(
                        lambda x: f"{x: >2}" if isinstance(x, int) else x,
                        board[(i := row * self._cols) : i + self._cols],
                    )
                )
            )
            print()

    def click_cell(self):
        pass

    def expand_zero_mine_field(self):
        pass


def main():
    b = Board()
    b.print_board()


if __name__ == "__main__":
    main()
