from agentsearch.problem import Problem
from search_methods.node import Node
from warehouse.cell import Cell


class Solution:

    def __init__(self, problem: Problem, goal_node: Node):
        self.problem = problem
        self.goal_node = goal_node #guarda no final - o no que corresponde ao objetivo
        self.actions = [] #tem o UP DOWN LEFT RIGHT que forklift fará
        self.all_cells = [] #added - tem todas as celulas por onde o forklift passa
        node = self.goal_node
        while node.parent is not None: #enquanto no tiver pai (ou seja ate chegar ao inicio)
            self.actions.insert(0, node.state.action) #colocar para o indice 0 a celula que esta associada ao no naquele momento. 0 para inserir na posicao inicial. E como é "insert" push todos os outros elementos existentes para a direita
            self.all_cells.insert(0, Cell(node.state.line_forklift, node.state.column_forklift)) #added
            node = node.parent
        self.all_cells.insert(0, Cell(node.state.line_forklift, node.state.column_forklift)) #added (para colocar o ultimo, se nao ficaria a faltar esse)

    @property
    def cost(self) -> int:
        return self.problem.compute_path_cost(self.actions)

    def __str__(self):
        return str(self.cost) + " " + " ".join(str(obj) for obj in self.actions)
