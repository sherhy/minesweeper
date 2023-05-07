from random import randrange, sample
from enum import Enum, auto
from functools import cached_property
from dataclasses import dataclass
import sys


class Level(Enum):
    EASY = auto()
    DIFFICULT = auto()


@dataclass
class Presets:
    bomb_count: int
    rows: int
    cols: int


LEVEL_CONFIGS = {Level.EASY: Presets(9, 10, 10)}


class Board:
    def __init__(self):
        self.set_difficulty(Level.EASY)
        self._board = [None for i in range(self.grid_size)]
        self.load_new_bombs()
        self.load_cell_numbers()
        self._board_visibility_mask = [False for i in range(self.grid_size)]

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
        for index in range(self.grid_size):
            if index in self._loaded_cells:
                continue
            neighbor_indices = self.get_neighbor_indices(index)
            nearby_bomb_count = len(
                set(self._loaded_cells).intersection(neighbor_indices)
            )
            self.board[index] = nearby_bomb_count

    def row_col_to_index(self, row, col):
        return row * self._cols + col

    def get_neighbor_indices(self, i):
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

        if (r := i % self._cols) == 0:
            neighbor_indices[0] = neighbor_indices[3] = neighbor_indices[5] = -1
        if r == self._cols - 1:
            neighbor_indices[2] = neighbor_indices[4] = neighbor_indices[7] = -1

        return filter(lambda x: x > -1 and x < self.grid_size, neighbor_indices)

    def print_board(self, debug=False):
        display_board = [
            x if self._board_visibility_mask[i] else "X"
            for i, x in enumerate(self.board)
        ]
        print("  ".join(map(str, [i for i in range(self._cols)])))
        for row in range(self._rows):
            board = display_board if not debug else self.board
            sys.stdout.flush()
            print(
                "  ".join(
                    map(
                        lambda x: f"{x: >1}" if isinstance(x, int) else x,
                        board[(i := row * self._cols) : i + self._cols],
                    )
                )
                + "\n"
            )

    def click_cell(self, i):
        if i in self._loaded_cells:
            self.print_board()
            print("kaboom")
            sys.exit(1)
        self._board_visibility_mask[i] = True
        if self.board[i] == 0:
            self.expand_zero_mine_field(i)
        if self._board_visibility_mask.count(False) == self._bomb_count:
            print("you're a winner")
            sys.exit(0)

    def expand_zero_mine_field(self, i):
        for j in self.get_neighbor_indices(i):
            if self._board_visibility_mask[j]:
                continue
            self.click_cell(j)

    def play(self):
        while True:
            self.print_board()
            try:
                row, col = map(int, input("open [row,col] ").split(","))
                i = self.row_col_to_index(row, col)
                if i > self.grid_size:
                    continue
            except ValueError:
                continue
            self.click_cell(i)


def main():
    b = Board()
    b.play()


if __name__ == "__main__":
    main()
