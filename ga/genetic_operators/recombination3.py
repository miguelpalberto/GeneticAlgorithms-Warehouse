from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual

class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        #troca de alguns forklifts entre parents
        num_genes = ind1.num_genes
        number_of_products = len(ind1.problem.products)

        child1 = [-1] * len(ind1.genome)
        child2 = [-1] * len(ind1.genome)
        for i in range(0, num_genes):
            child1[i] = ind1.genome[i]  # Insere genoma do ind1 no child1
            child2[i] = ind2.genome[i]


        # child1
        # trocar forklifts:
        for i in range(0, num_genes):
            if ind2.genome[i] > number_of_products:  # se apanhar um forklift
                if ind2.genome[i] % 2 == 1: #para trocar so alguns forklifts (impares)
                    forkliftEncontrado = ind2.genome[i]
                    valorSubstituido = ind1.genome[i]
                    child1[i] = forkliftEncontrado  # forklift do ind2 vai para o child1

                    for j in range(0, num_genes):
                        if ind1.genome[j] == forkliftEncontrado:
                            child1[j] = valorSubstituido  # pôr valor substituido para nao haver forklifts repetidos
                            break

        #Confirmacao:
        vetorGenesQueFaltam = []
        for i in range(0, num_genes):
            if ind1.genome[i] not in child1:
                vetorGenesQueFaltam.append(ind1.genome[i])
        for i in range(0, num_genes-1):
            for j in range(i+1, num_genes):
                if child1[i] == child1[j]:
                    child1[j] = vetorGenesQueFaltam[0]
                    vetorGenesQueFaltam.remove(vetorGenesQueFaltam[0])

        #child2
        #trocar forklifts:
        for i in range(0, num_genes):
            if ind1.genome[i] > number_of_products:
                if ind1.genome[i] % 2 == 1:
                    forkliftEncontrado = ind1.genome[i]
                    valorSubstituido = ind2.genome[i]
                    child2[i] = forkliftEncontrado

                    for j in range(0, num_genes):
                        if ind2.genome[j] == forkliftEncontrado:
                            child2[j] = valorSubstituido
                            break

        vetorGenesQueFaltam2 = []
        for i in range(0, num_genes):
            if ind2.genome[i] not in child2:
                vetorGenesQueFaltam2.append(ind2.genome[i])
        for i in range(0, num_genes-1):
            for j in range(i+1, num_genes):
                if child2[i] == child2[j]:
                    child2[j] = vetorGenesQueFaltam2[0]
                    vetorGenesQueFaltam2.remove(vetorGenesQueFaltam2[0])

        ind1.genome = child1
        ind2.genome = child2


    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"