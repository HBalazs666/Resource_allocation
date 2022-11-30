from init_simulation import init_sa
import math
import random
from genetic import calculate_fitness
from classes import Individual


# 1 ms-t random VM-re átpakolunk
def change_one(best_individual_matrix):
    
    # random választunk egy ms-t, amit át szeretnénk pakolni
    ms_num = random.randint(0, len(best_individual_matrix[0]) - 1)

    # random választunk egy új VM-et
    new_VM = random.randint(0, len(best_individual_matrix) - 1)

    # mindent kinullázunk, kivéve az újat
    for VM in range(len(best_individual_matrix)):

        if VM == new_VM:
            best_individual_matrix[VM][ms_num] = 1
        else:
            best_individual_matrix[VM][ms_num] = 0

    return best_individual_matrix


# csak szomszédos állapotok generálhatóak a legjobb egyedből
def gen_individual_matrices(best_individual, states_per_iteration):
    
    new_matrices = []

    for state in range(states_per_iteration):

        new_matrix = change_one(best_individual.matrix)
        new_matrices.append(new_matrix)

    return new_matrices


def simulated_annealing(nodes, ms_list, states_per_iteration,
                        VM_num, ms_num, service_num, ms_num_per_service,
                        T_0, alpha, k_max):
    
    init_individual = init_sa(VM_num, ms_num, nodes, service_num, ms_num_per_service, ms_list)

    best_individual = init_individual

    for k in range(k_max):

        individuals = []

        T = T_0 * (alpha**k)

        individual_matrices = gen_individual_matrices(best_individual, states_per_iteration)

        for individual in range(len(individual_matrices)):
            fitness_of_individual = calculate_fitness(individual_matrices[individual],
                                                      nodes, service_num,
                                                      ms_num_per_service, ms_list)
            created_individual = Individual(individual_matrices[individual], fitness_of_individual)
            individuals.append(created_individual)

        for individual in range(len(individuals)):

            if individuals[individual].fitness < best_individual.fitness:
                best_individual = individuals[individual]
            else:
                p = math.exp(-(individuals[individual].fitness - best_individual.fitness) / (T))
                if random.uniform(0, 1) <= p:
                    best_individual = individuals[individual]

    return best_individual
        