import numpy as np

from ga.individual_int_vector import IntVectorIndividual
from warehouse.cell import Cell
from warehouse.pair import Pair





class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.path_matrix = [] #added contem o numero de produto a produto (o caminho) que cada forklift fará. Ex: [6, 1, 2, 3, 4, S][7, 5, S]
        self.fitness = 0
        self.path_costs = [] #added contem custos (distancia) entre cada caminho (total) que cada forklift fará
        self.total_distances = 0 #added


    def compute_fitness(self) -> float: #Fitness
        self.compute_all_path()
        initial_fitness = np.max(self.path_costs)
        self.fitness = initial_fitness + self.total_distances
        return initial_fitness + self.total_distances

    def calculate_total_distances(self): #Calcular distancia total da solucao(individuo) (e preencher path_costs)
        self.total_distances = 0
        self.path_costs = []
        for path in self.path_matrix:
            i = 0
            isLast = False
            path_dist = 0
            while not isLast:
                cell1 = path[i] #path (camihnho) é uma lista que vai de produto a produto. Path[i] será o produto
                if path[i+1] != 'S':
                    cell2 = path[i + 1]
                else:
                    cell2 = self.problem.agent_search.exit
                    isLast = True

                pair = Pair(cell1, cell2)
                if pair not in self.problem.agent_search.solution_by_pair:
                    pair = Pair(cell2, cell1) #se nao encontrar o par, inverte porque esse de certeza que já existe

                pair_dist = self.problem.agent_search.get_pair_solution(pair).cost #vai buscar o custo do par - que será igual a distancia

                path_dist += pair_dist  # soma a distancia do par à distancia total
                i += 1
            self.total_distances += path_dist #soma a distancia do caminho à distancia total do individuo
            self.path_costs.append(path_dist) #adiciona custo do caminho ao path_costs

    def compute_all_path(self): #preencher matriz(path_matrix) com o caminho a fazer de produto a produto (usado no fitness e no obtain_all_path). (e chama o calculate_total_distances())
        i,j,k = 0,0,0
        self.path_matrix = []
        for i in range(len(self.genome)):
            #Colocar forklift no 1º elemento, depois os produtos, e depois o 'S'
            if self.genome[i] > len(self.problem.products) or i == len(self.genome) - 1:# se for forklift ou estiver na ultima iteracao:
                if i == len(self.genome) - 1: #para na ultima iteracao fazer skip para o proximo
                    i += 1
                line = []
                line.append(self.problem.forklifts[k]) #coloca forklift no primeiro elemento da line
                while j < i:
                    if self.genome[j] <= len(self.problem.products): #se genome[j] for produto
                        line.append(self.problem.get_product(self.genome[j])) #colocar
                    j += 1
                if j == i: #se isto for verdade, significa que o ultimo elemento da linha era um produto
                    j += 1
                    line.append('S') #nesse caso colocar agora lá a saida tambem
                k+=1
                self.path_matrix.append(line)

        if self.genome[-1] > len(self.problem.products): # se ultimo elemento(-1 em python anda no indice para tras) for um forklift, é porque o ultimo forklift (que nao é mencionado no vetor, nao tem produtos)
            line = []
            line.append(self.problem.forklifts[k]) #colocar o forklift na linha, pois nao foi mencionado no vetor
            line.append('S')
            self.path_matrix.append(line)

        self.calculate_total_distances()


    def obtain_all_path(self) -> []: #usado para na classe SimulationRunner do GUI para saber onde colocar a visualizacao dos forklifts a andarem - buscar todas posicoes do forklift para renderizar posicao a posicao. (e chama o compute_all_path())
        all_path = []
        if len(self.path_matrix) == 0:
            self.compute_all_path()
            self.calculate_total_distances()
        for line in self.path_matrix: #para cada um dos caminhos de cada forklift
            new_line = []
            new_line.append(line[0]) #adiciona forklift
            for i in range(0, len(line) - 1, 1): #range(começa, acaba (com -1 porque se nao o seguinte ia buscar null - a seguir a 'S'), step)
                cell1 = line[i]
                if line[i+1] != 'S': #se posicao seguinte nao for saida ver seguinte na cell2
                    cell2 = line[i + 1]
                else:
                    cell2 = self.problem.agent_search.exit #se nao, acabar
                pair = Pair(cell1, cell2)
                reverse = False #flag
                if pair not in self.problem.agent_search.solution_by_pair:
                    pair = Pair(cell2, cell1) #se par nao existir o contrario ha de existir
                    reverse = True
                pair_solution = self.problem.agent_search.get_pair_solution(pair)
                if not reverse: #se nao tiver feito o reverse
                    new_line.extend(pair_solution.all_cells[1:]) #extend - adiciona all_cells a new_line desde o indice 1 ate ao ultimo (no indice 0 tem o forklift)
                else:
                    all_cells = pair_solution.all_cells[::-1]#::1 reverte ordem e itera lista
                    new_line.extend(all_cells[1:])

            all_path.append(new_line) #em cada step posicao forklift

        return all_path, np.max(self.path_costs) + 1 #devolve 2 coisas: posicao em cada step, numero de steps maximo

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        string += "Forklifts path:\n"
        for i in range(len(self.problem.forklifts)):
            string += str((' -> '.join(map(str, self.path_matrix[i])))) + "\n"
            string += "Steps: " + str(self.path_costs[i]) + "\n\n"
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.total_distances = self.total_distances #added
        new_instance.fitness = self.fitness                 #added
        new_instance.path_matrix = self.path_matrix.copy()  #added
        new_instance.path_costs = self.path_costs.copy()    #added
        return new_instance

