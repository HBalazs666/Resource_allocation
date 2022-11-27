from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_matrix
from init_simulation import init_nodes
from init_simulation import init_ms_list
from genetic import genetic_algorithm


fog_num = 2
starting_point = 2  # ehhez a ponthoz csatlakozik a service

# itt generáljuk a mintahálózatot
graph = graph_gen(fog_num)
graph.print_adj_list()

# meghatározzuk a legrövidebb utakat
network_latencies = dijkstra(graph, fog_num, starting_point)
print(network_latencies)

# inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
service_quantity = 1  # hány darab legyen
ms_per_service = 1  # servicenként mennyi ms legyen TODO: lehetne ez is változó
MIPS_ms_min = 5000  # minimum MIPS
MIPS_ms_max = 5000  # maximum MIPS
RAM_ms_min = 5000
RAM_ms_max = 5000

ms_list = init_ms_list(service_quantity, ms_per_service,
                       MIPS_ms_max, MIPS_ms_min, RAM_ms_max,
                       RAM_ms_min)

# inicializáljuk a csomópontokat
parameters = []
# -------------------------------------------
cloud_total_MIPS = [6000000, 6000000]  # 0
cloud_total_RAM = [1000000, 1000000]  # 1
VMs_per_cloud = 2  # 2
fog_total_MIPS = [6000, 6000]  # 3
fog_total_RAM = [6000, 6000]  # 4
VMs_per_fog = 1  # 5
edge_total_MIPS = [1, 1]  # 6
edge_total_RAM = [1, 1]  # 7
VMs_per_edge = 1  # 8
# -------------------------------------------
parameters.append(cloud_total_MIPS)
parameters.append(cloud_total_RAM)
parameters.append(VMs_per_cloud)
parameters.append(fog_total_MIPS)
parameters.append(fog_total_RAM)
parameters.append(VMs_per_fog)
parameters.append(edge_total_MIPS)
parameters.append(edge_total_RAM)
parameters.append(VMs_per_edge)

nodes = init_nodes(fog_num, network_latencies, parameters)

# létrehozzuk a genetikus algoritmus kezdeti mátrixát
# csak a méretekhez kell
# TODO: helyettesítés egyszerűbb függvénnyel
matrix = init_matrix(nodes, ms_list)

# -------------------------------------------
generation_num = 30
population_size = 20
# -------------------------------------------
# a legjobb eredmény a megadott paraméterek mellett
best_individual = genetic_algorithm(matrix, nodes, ms_list,
                                    generation_num,
                                    population_size, service_quantity,
                                    ms_per_service)
print(best_individual.matrix)
print(best_individual.fitness)