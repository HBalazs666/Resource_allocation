from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_matrix
from init_simulation import init_nodes
from init_simulation import init_ms_list
from genetic import genetic_algorithm
from genetic import backup_genetic_algorithm
from genetic import cost_calculator
from genetic import calculate_fitness

# szimulációs paraméterek
# ------------------------------------------------------------
# genetikus algoritmus paraméterei
generation_num = 100
population_size = 200

# költségkorlát
cost_max = 100000 

# hálózat mérete és csatlakozási pont
fog_num = 2
starting_point = 3

# inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
service_quantity = 4  # hány darab legyen
ms_per_service = 3  # servicenként mennyi ms legyen
MIPS_ms_min = 1000  # minimum MIPS
MIPS_ms_max = 1000  # maximum MIPS
RAM_ms_min = 5
RAM_ms_max = 5

# inicializáljuk a csomópontokat
cloud_total_MIPS = [50000, 50000]  # 0
cloud_total_RAM = [1000000, 1000000]  # 1
VMs_per_cloud = 4  # 2
fog_total_MIPS = [10000, 10000]  # 3
fog_total_RAM = [6000, 6000]  # 4
VMs_per_fog = 3  # 5
edge_total_MIPS = [1000, 1000]  # 6
edge_total_RAM = [10000, 10000]  # 7
VMs_per_edge = 2  # 8
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
                                    ms_per_service, cost_max)

cost_of_best = cost_calculator(best_individual.matrix, nodes)

print("Best individual: ",best_individual.matrix)
print("Fitness (latency): ",best_individual.fitness)
print("Cost: ", cost_of_best)

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