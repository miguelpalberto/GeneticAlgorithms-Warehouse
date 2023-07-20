from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()

    def compute(self, state: WarehouseState) -> float: #Simplesmente ve a distancia de Manhattan entre a posicao atual e a posicao final
        #TODO done
        goal_position = self.problem.goal_position
        current_position = state.forklift_position
        return abs(goal_position.line - current_position.line) + abs(goal_position.column - current_position.column) #abs torna valor sempre positivo


    def __str__(self):
        return "Distance to the goal position"

