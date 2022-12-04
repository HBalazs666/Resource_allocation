from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_matrix
from init_simulation import init_nodes
from init_simulation import init_ms_list
from genetic import genetic_algorithm
from genetic import backup_genetic_algorithm
from genetic import cost_calculator
from genetic import calculate_fitness


def GA_simulation(generation_num, population_size, cost_max, mutation_coefficient,
                  with_backup=False):
# szimulációs paraméterek
# ------------------------------------------------------------

    # költségkorlát
    cost_max = 9999999999 

    # hálózat mérete és csatlakozási pont
    fog_num = 5
    starting_point = 3

    # inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
    service_quantity = 10  # hány darab legyen
    ms_per_service = 10  # servicenként mennyi ms legyen
    MIPS_ms_min = 150  # minimum MIPS
    MIPS_ms_max = 150  # maximum MIPS
    RAM_ms_min = 512
    RAM_ms_max = 1024

    # inicializáljuk a csomópontokat
    cloud_total_MIPS = [30000, 30000]  # 0
    cloud_total_RAM = [40960, 40960]  # 1
    VMs_per_cloud = 5  # 2
    fog_total_MIPS = [15000, 15000]  # 3
    fog_total_RAM = [8192, 8192]  # 4
    VMs_per_fog = 5  # 5
    edge_total_MIPS = [7500, 7500]  # 6
    edge_total_RAM = [6144, 6144]  # 7
    VMs_per_edge = 5  # 8
    cloud_cost_multiplier = 1  # 9
    fog_cost_multiplier = 4  # 10
    edge_cost_multiplier = 8  # 11
    # ------------------------------------------------------------

    # itt generáljuk a mintahálózatot
    graph = graph_gen(fog_num)
    graph.print_adj_list()

    # meghatározzuk a legrövidebb utakat
    network_latencies = dijkstra(graph, fog_num, starting_point)
    print(network_latencies)

    ms_list = init_ms_list(service_quantity, ms_per_service,
                        MIPS_ms_max, MIPS_ms_min, RAM_ms_max,
                        RAM_ms_min)

    parameters = []
    parameters.append(cloud_total_MIPS)
    parameters.append(cloud_total_RAM)
    parameters.append(VMs_per_cloud)
    parameters.append(fog_total_MIPS)
    parameters.append(fog_total_RAM)
    parameters.append(VMs_per_fog)
    parameters.append(edge_total_MIPS)
    parameters.append(edge_total_RAM)
    parameters.append(VMs_per_edge)
    parameters.append(cloud_cost_multiplier)
    parameters.append(fog_cost_multiplier)
    parameters.append(edge_cost_multiplier)

    nodes = init_nodes(fog_num, network_latencies, parameters)

    # létrehozzuk a genetikus algoritmus kezdeti mátrixát
    # csak a méretekhez kell
    matrix = init_matrix(nodes, ms_list)

    # a legjobb eredmény a megadott paraméterek mellett
    best_individual = genetic_algorithm(matrix, nodes, ms_list,
                                        generation_num,
                                        population_size, service_quantity,
                                        ms_per_service, cost_max,
                                        mutation_coefficient)

    cost_of_best = cost_calculator(best_individual.matrix, nodes)

    print("Best individual: ",best_individual.matrix)
    print("Fitness (latency): ",best_individual.fitness)
    print("Cost: ", cost_of_best)

    return best_individual.fitness

    if with_backup == True:
        backup_individual = backup_genetic_algorithm(matrix,
                                                    nodes, ms_list,
                                                    generation_num,
                                                    population_size,
                                                    service_quantity,
                                                    ms_per_service,
                                                    best_individual.matrix)

        print("Backup matrix: ", backup_individual.matrix)
        print("Backup fitness (cost): ", backup_individual.fitness)

        cost_max_backup = 9999999
        latency_of_backup = calculate_fitness(backup_individual.matrix, nodes, service_quantity,
                                            ms_per_service, ms_list, cost_max_backup)

        print("Backup latency: ", latency_of_backup)