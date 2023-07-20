import numpy as np
import random

from ga.problem import Problem
from warehouse.cell import Cell
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual


class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        self.forklifts = agent_search.forklifts

        self.products_by_number = {} #added
        self.products = agent_search.products
        #added:
        i = 1
        for product in self.products:
            self.products_by_number[i] = product
            i+=1

        self.agent_search = agent_search

    def get_product(self, key) -> Cell:
        return self.products_by_number[key]

    def generate_individual(self) -> "WarehouseIndividual": #todo done #Gera individuo random consoante os parametros do problema (numero forklifts e produtos)
        individual = WarehouseIndividual(self, len(self.products) + len(self.forklifts) - 1)

        i = 0
        j = len(self.products) + 1 #j começa no numero de produtos + 1 -> numero do forklift
        for i in range(len(self.forklifts) - 1): #para cada forklift menos o ultimo (que nao aparece)
            individual.genome[i] = j #colocar numero do forklift no genoma
            j += 1
            i += 1  #este sera incrementado further no proximo loop for

        for key in self.products_by_number:
            individual.genome[i] = key #colocar numero do produto no genoma
            i += 1

        random.shuffle(individual.genome) #ja com produtos no individuo(solucao), randomizar

        individual.fitness = individual.compute_fitness() #guardar fitness correspondente

        return individual

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

