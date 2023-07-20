import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action
from warehouse.cell import Cell


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()
        #Todo done e alterado

        self.line_forklift = None
        self.column_forklift = None
        self.line_exit = None
        self.column_exit = None
        self.line_goal = None
        self.column_goal = None

        self.forklift_position = None
        self.products_to_pick = 0

        self.rows = rows
        self.columns = columns

        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)
        self.matrix = matrix
        self.forklift_position = Cell(-1, -1)

    def set_goal(self, line_goal: int, column_goal: int):
        self.line_goal = line_goal
        self.column_goal = column_goal

    def set_exit(self, line_exit: int, column_exit: int):
        self.line_exit = line_exit
        self.column_exit = column_exit

    def set_forklift(self, line_forklift: int, column_forklift: int):
        self.line_forklift = line_forklift
        self.column_forklift = column_forklift
        self.forklift_position.line = line_forklift
        self.forklift_position.column = column_forklift

    def all_packages_delivered(self) -> bool:
        return self.products_to_pick == 0

    def can_move_up(self) -> bool:
        #TODO done
        return self.line_forklift - 1 >= 0 and \
            self.matrix[self.line_forklift - 1][self.column_forklift] != constants.SHELF and \
             self.matrix[self.line_forklift - 1][self.column_forklift] != constants.PRODUCT

    def can_move_right(self) -> bool:
        #TODO done
        return self.column_forklift + 1 < self.columns and \
            self.matrix[self.line_forklift][self.column_forklift + 1] != constants.SHELF and \
             self.matrix[self.line_forklift][self.column_forklift + 1] != constants.PRODUCT

    def can_move_down(self) -> bool:
        #TODO done
        return self.line_forklift + 1 < self.rows and \
            self.matrix[self.line_forklift + 1][self.column_forklift] != constants.SHELF and \
             self.matrix[self.line_forklift + 1][self.column_forklift] != constants.PRODUCT

    def can_move_left(self) -> bool:
        #TODO done
        return self.column_forklift - 1 >= 0 and \
            self.matrix[self.line_forklift][self.column_forklift - 1] != constants.SHELF and \
             self.matrix[self.line_forklift][self.column_forklift - 1] != constants.PRODUCT

    def move_up(self) -> None:
        #TODO done
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.line_forklift -= 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT
        self.forklift_position = Cell(self.line_forklift, self.column_forklift)

    def move_right(self) -> None:
        #TODO done
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.column_forklift += 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT
        self.forklift_position = Cell(self.line_forklift, self.column_forklift)

    def move_down(self) -> None:
        #TODO done
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.line_forklift += 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT
        self.forklift_position = Cell(self.line_forklift, self.column_forklift)

    def move_left(self) -> None:
        #TODO done
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.column_forklift -= 1
        self.matrix[self.line_forklift][self.column_forklift] = constants.FORKLIFT
        self.forklift_position = Cell(self.line_forklift, self.column_forklift)

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.line_forklift or column != self.column_forklift):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        if self.matrix[row][column] == constants.EXIT:
            return constants.COLOREXIT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
