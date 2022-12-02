from init_simulation import init_sa
import math
import random
import copy
from genetic import calculate_fitness
from genetic import cost_calculator
from genetic import calculate_backup_fitness
from classes import Individual


# 1 ms-t random VM-re átpakolunk
def change_one(best_individual_matrix):
    
    new = copy.deepcopy(best_individual_matrix)

    # random választunk egy ms-t, amit át szeretnénk pakolni
    ms_num = random.randint(0, len(new[0]) - 1)

    # random választunk egy új VM-et
    new_VM = random.randint(0, len(new) - 1)

    # mindent kinullázunk, kivéve az újat
    for VM in range(len(new)):

        if VM == new_VM:
            new[VM][ms_num] = 1
        else:
            new[VM][ms_num] = 0

    return new


# csak szomszédos állapotok generálhatóak a legjobb egyedből
def gen_individual_matrices(best_individual, states_per_iteration):
    
    new_matrices = []

    for state in range(states_per_iteration):

        new_matrix = change_one(best_individual.matrix)
        new_matrices.append(new_matrix)

    return new_matrices


def simulated_annealing(nodes, ms_list, states_per_iteration,
                        VM_num, ms_num, service_num, ms_num_per_service,
                        T_0, alpha, k_max, cost_max):
    
    init_individual = init_sa(VM_num, ms_num, nodes, service_num, ms_num_per_service, ms_list,
                              cost_max)

    best_individual = init_individual

    for k in range(k_max):

        individuals = []

        T = T_0 * (alpha**k)

        individual_matrices = gen_individual_matrices(best_individual, states_per_iteration)
        #for i in range(len(individual_matrices)):    
        #    print("GENERÁLT INDIVIDUAL MÁTRIX ",i,": ",individual_matrices[i], "\n")

        for individual in range(len(individual_matrices)):
        #    print("A ",individual,". mátrix: ", individual_matrices[individual], "\n")
            fitness_of_individual = calculate_fitness(individual_matrices[individual],
                                                      nodes, service_num,
                                                      ms_num_per_service, ms_list,
                                                      cost_max)
        #    print("A ",individual,". mátrix fitnesse: ",fitness_of_individual,"\n")
            created_individual = Individual(individual_matrices[individual], fitness_of_individual)
            individuals.append(created_individual)

        for individual in range(len(individuals)):
            print("A ",individual,". egyed fitnesse: ",individuals[individual].fitness,"\n")

            if individuals[individual].fitness < best_individual.fitness:
                best_individual = copy.deepcopy(individuals[individual])
            else:
                p = math.exp(-(individuals[individual].fitness - best_individual.fitness) / (T))
                if random.uniform(0, 1) <= p:
                    best_individual = copy.deepcopy(individuals[individual])
        print("Best individual in k=",k," : ",best_individual.fitness)
    return best_individual
        

def backup_simulated_annealing(nodes, ms_list, states_per_iteration,
                               VM_num, ms_num, service_num,
                               ms_num_per_service,
                               T_0, alpha, k_max, allocated_matrix):

    cost_max_backup = 9999999
    init_individual = init_sa(VM_num, ms_num, nodes, service_num, ms_num_per_service, ms_list,
                              cost_max_backup)

    best_individual = init_individual

    for k in range(k_max):

        individuals = []

        T = T_0 * (alpha**k)

        individual_matrices = gen_individual_matrices(best_individual, states_per_iteration)

        for individual in range(len(individual_matrices)):
            fitness_of_individual = calculate_backup_fitness(individual_matrices[individual],
                                                             nodes, service_num,
                                                             ms_num_per_service, ms_list,
                                                             allocated_matrix)

            created_individual = Individual(individual_matrices[individual], fitness_of_individual)
            individuals.append(created_individual)

        for individual in range(len(individuals)):

            if individuals[individual].fitness < best_individual.fitness:
                best_individual = copy.deepcopy(individuals[individual])
            else:
                p = math.exp(-(individuals[individual].fitness - best_individual.fitness) / (T))
                if random.uniform(0, 1) <= p:
                    best_individual = copy.deepcopy(individuals[individual])

    return best_individual