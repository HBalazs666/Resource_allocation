from SA_main import SA_simulation
from GA_main import GA_simulation


def GA():

    generation_num_max = 200
    #population_size = 100
    mutation_coefficient = 1

    cost_max = 99999999

    param = [100]

    obj_per_param = []

    for p in range(len(param)):

        obj_per_param.append([])
        population_size = param[p]

        for i in range(int(generation_num_max/10)):

            #generation_num = (i+1)*10
            generation_num = 400

            fitness = GA_simulation(generation_num, population_size,
                                    cost_max, mutation_coefficient)

            obj_per_param[p].append(fitness)

    print(obj_per_param)

    return obj_per_param

def SA():

    # első ábra dolgai
    # alfa a paraméter, k a változó, f(x) a függvényérték

    # mik legyenek a paraméterértékek? (alfa)
    alpha_values = [0.99]

    # maximális iterációszám
    k_max = 1600

    # egyéb fix paraméterek
    states_per_iteration = 50
    T_0 = 50
    cost_max = 99999999999

    #kimeneti értékek egy paraméterre (célfüggvény értékek egy paraméterre)
    obj_per_param = []

    for a in range(len(alpha_values)):

        obj_per_param.append([])

        for k in range(int(k_max)):
            k_act = (k+1)

            act_fitness = SA_simulation(states_per_iteration, T_0, alpha_values[a], k_max, cost_max)
            obj_per_param[a].append(act_fitness)

    print(obj_per_param)


GA()