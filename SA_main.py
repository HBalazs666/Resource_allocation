from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_matrix
from init_simulation import init_nodes
from init_simulation import init_ms_list
from simulated_annealing import simulated_annealing


fog_num = 2
starting_point = 2  # ehhez a ponthoz csatlakozik a service

# itt generáljuk a mintahálózatot
graph = graph_gen(fog_num)
graph.print_adj_list()

# meghatározzuk a legrövidebb utakat
network_latencies = dijkstra(graph, fog_num, starting_point)
print(network_latencies)

# inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
service_quantity = 3  # hány darab legyen
ms_per_service = 2  # servicenként mennyi ms legyen TODO: lehetne ez is változó
MIPS_ms_min = 1000  # minimum MIPS
MIPS_ms_max = 1000  # maximum MIPS
RAM_ms_min = 5
RAM_ms_max = 5

ms_list = init_ms_list(service_quantity, ms_per_service,
                       MIPS_ms_max, MIPS_ms_min, RAM_ms_max,
                       RAM_ms_min)

# inicializáljuk a csomópontokat
parameters = []
# -------------------------------------------
cloud_total_MIPS = [50000, 50000]  # 0
cloud_total_RAM = [1000000, 1000000]  # 1
VMs_per_cloud = 2  # 2
fog_total_MIPS = [1, 1]  # 3
fog_total_RAM = [6000, 6000]  # 4
VMs_per_fog = 1  # 5
edge_total_MIPS = [1000, 1000]  # 6
edge_total_RAM = [10000, 10000]  # 7
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

# szimulációs paraméterek
states_per_iteration = 50  # generált példányok iterációnként
T_0 = 100  # kezdeti hőmérséklet
alpha = 0.99  # hűlési együttható
k_max = 2000  # iterációk száma

VM_num = VMs_per_cloud + VMs_per_fog*fog_num + VMs_per_edge*fog_num*2
ms_num = len(ms_list)

# a szimuláció kimenete (Individual)
solution = simulated_annealing(nodes, ms_list, states_per_iteration,
                               VM_num, ms_num, service_quantity, ms_per_service,
                               T_0, alpha, k_max)

print(solution.matrix)
print(solution.fitness)
