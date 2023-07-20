import copy
from typing import TypeVar

import numpy as np

import constants
from agentsearch.agent import Agent
from agentsearch.state import State
from search_methods.solution import Solution
from warehouse.actions import ActionUp, ActionDown, ActionLeft, ActionRight
from warehouse.cell import Cell
from warehouse.heuristic_warehouse import HeuristicWarehouse
from warehouse.pair import Pair


class WarehouseAgentSearch(Agent):
    S = TypeVar('S', bound=State)

    def __init__(self, environment: S):
        super().__init__()
        self.initial_environment = environment
        self.heuristic = HeuristicWarehouse()
        self.forklifts = []
        self.products = []
        self.exit = None
        self.pairs = []
        self.solution_by_pair = {}
        for i in range(environment.rows):
            for j in range(environment.columns):
                if environment.matrix[i][j] == constants.FORKLIFT:
                    self.forklifts.append(Cell(i, j))
                elif environment.matrix[i][j] == constants.EXIT:
                    self.exit = Cell(i, j)
                elif environment.matrix[i][j] == constants.PRODUCT:
                    self.products.append(Cell(i, j))

        for a in self.forklifts:
            for p in self.products:
                self.pairs.append(Pair(a, p))

        for i in range(len(self.products) - 1):
            for j in range(i + 1, len(self.products)):
                self.pairs.append(Pair(self.products[i], self.products[j]))

        for p in self.products:
            self.pairs.append(Pair(p, self.exit))

        for a in self.forklifts:
            self.pairs.append(Pair(a, self.exit))

    def __str__(self) -> str:
        str = "Pairs:\n"
        for p in self.pairs:
            str += f"{p}\n"
        return str

    #added
    def add_solution_to_pair(self, pair, pair_solution):
        self.solution_by_pair[pair] = pair_solution

    #added
    def get_pair_solution(self, pair) -> Solution:
        return self.solution_by_pair[pair]

    # added
    def invert_solution(self, pair_solution):
        inverted_solution = copy.deepcopy(pair_solution)
        inverted_solution.actions.reverse()
        copied_actions = copy.deepcopy(inverted_solution.actions)
        inverted_solution.actions = []
        for action in copied_actions:
            if isinstance(action, ActionUp):
                inverted_solution.actions.append(ActionDown())
            elif isinstance(action, ActionDown):
                inverted_solution.actions.append(ActionUp())
            elif isinstance(action, ActionLeft):
                inverted_solution.actions.append(ActionRight())
            else:
                inverted_solution.actions.append(ActionLeft())
        inverted_solution.all_cells.reverse()
        inverted_solution.goal_node = None
        inverted_solution.problem = None
        return inverted_solution


def read_state_from_txt_file(filename: str):
    with open(filename, 'r') as file:
        num_rows, num_columns = map(int, file.readline().split())
        float_puzzle = np.genfromtxt(file, delimiter=' ')
        return float_puzzle, num_rows, num_columns
