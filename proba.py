from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_matrix
from init_simulation import init_nodes
from init_simulation import init_ms_list
from genetic import genetic_algorithm


fog_num=2
starting_point = 2  # ehhez a ponthoz csatlakozik a service

# itt generáljuk a mintahálózatot
graph = graph_gen(fog_num)

# meghatározzuk a legrövidebb utakat
network_latencies = dijkstra(graph, fog_num, starting_point)

# inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
service_quantity = 1  # hány darab legyen
ms_per_service = 4  # servicenként mennyi ms legyen TODO: lehetne ez is változó
MIPS_ms_min = 100  # minimum MIPS
MIPS_ms_max = 2000  # maximum MIPS
RAM_ms_min = 500
RAM_ms_max = 2000

ms_list = init_ms_list(service_quantity, ms_per_service, MIPS_ms_max, MIPS_ms_min, RAM_ms_max, RAM_ms_min)

# inicializáljuk a csomópontokat
parameters = []
# -------------------------------------------
cloud_total_MIPS = [600, 600]  # 0
cloud_total_RAM = [10, 10]  # 1
VMs_per_cloud = 2  # 2
fog_total_MIPS = [300, 300]  # 3
fog_total_RAM = [5, 5]  # 4
VMs_per_fog = 1  # 5
edge_total_MIPS = [100, 100]  # 6
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
matrix = init_matrix(nodes, ms_list)
print(matrix)

# genetic_solution = genetic_algorithm(matrix, nodes, ms_list)

# kasd