from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
from ga.genetic_algorithm import GeneticAlgorithm

class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None: #pega num intervalo de genes (produtos ou forklifts) e inverte a ordem
        num_genes = len(ind.genome)
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        cut2 = cut1
        while (cut1 == cut2):
            cut2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        cut_array = ind.genome[cut1:cut2 + 1]
        ind.genome[cut1:cut2 + 1] = cut_array[::-1]

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
