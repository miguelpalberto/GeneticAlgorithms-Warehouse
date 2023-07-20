from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual
from ga.genetic_algorithm import GeneticAlgorithm
import random
class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        # Faz 4 particoes, troca 2 com 2 intercaladas e corrige os elementos repetidos

        num_genes = ind1.num_genes
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 4)
        cut2 = GeneticAlgorithm.rand.randint(cut1+1, num_genes - 3)
        cut3 = GeneticAlgorithm.rand.randint(cut2 + 1, num_genes - 2)

        mappingA1 = {}
        mappingA2 = {}
        mappingB1 = {}
        mappingB2 = {}
        mappingC1 = {}
        mappingC2 = {}
        mappingD1 = {}
        mappingD2 = {}

        #Coloca em cada mapping os genes a serem trocados entre os dois individuos:
        for i in range(0, cut1):
            mappingA1[i] = ind1.genome[i]
            mappingA2[i] = ind2.genome[i]
        for i in range(cut1, cut2):
            mappingB1[i] = ind1.genome[i]
            mappingB2[i] = ind2.genome[i]
        for i in range(cut2, cut3):
            mappingC1[i] = ind1.genome[i]
            mappingC2[i] = ind2.genome[i]
        for i in range(cut3, num_genes):
            mappingD1[i] = ind1.genome[i]
            mappingD2[i] = ind2.genome[i]

        ####
        # Child1
        child1 = [-1] * len(ind1.genome)
        for i in range(0, cut1):
            child1[i] = ind1.genome[i] #Insere parte do genoma do ind1 no child1)
        for i in range(cut1, cut2):
            child1[i] = ind2.genome[i]
        for i in range(cut2, cut3):
            child1[i] = ind1.genome[i]
        for i in range(cut3, num_genes):
            child1[i] = ind2.genome[i]

        #Ver e tratar repeticoes:
        for i in range(cut1, cut2):

            for j in range(0, i):
                if child1[i] == child1[j]:
                    child1[i] = ind1.genome[i]
            for j in range(cut2, cut3):
                if child1[i] == child1[j]:
                    child1[i] = ind1.genome[i]

        for i in range(cut3, num_genes):  # ver dentro particao 4
            for j in range(0, i):
                if child1[i] == child1[j]:
                    child1[i] = ind1.genome[j]

        #Se ainda assim houver genes iguais:
        vetorGenesQueFaltam = []
        for i in range(0, num_genes):
            if ind1.genome[i] not in child1:
                vetorGenesQueFaltam.append(ind1.genome[i])
        for i in range(0, num_genes-1):
            for j in range(i+1, num_genes):
                if child1[i] == child1[j]:
                    child1[j] = vetorGenesQueFaltam[0]
                    vetorGenesQueFaltam.remove(vetorGenesQueFaltam[0])

        ####
        # Child2
        child2 = [-1] * len(ind2.genome)
        for i in range(0, cut1):
            child2[i] = ind2.genome[i]
        for i in range(cut1, cut2):
            child2[i] = ind1.genome[i]
        for i in range(cut2, cut3):
            child2[i] = ind2.genome[i]
        for i in range(cut3, num_genes):
            child2[i] = ind1.genome[i]

        # Ver e tratar repeticoes:
        for i in range(cut1, cut2):  # ver dentro particao 2
            for j in range(0, i):
                if child2[i] == child2[j]:
                    child2[i] = ind2.genome[i]
            for j in range(cut2, cut3):
                if child2[i] == child2[i]:
                    child2[i] = ind2.genome[i]

        for i in range(cut3, num_genes):  # ver dentro particao 4
            for j in range(0, i):
                if child2[i] == child2[j]:
                    child2[i] = ind2.genome[j]

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
        return "Recombination 2 (" + f'{self.probability}' + ")"
