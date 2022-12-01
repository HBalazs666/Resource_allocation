from graph_gen import graph_gen
from graph_gen import dijkstra
from genetic import calculate_backup_fitness
from genetic import calculate_fitness
from genetic import cost_calculator
from init_simulation import init_nodes
from init_simulation import init_ms_list
from init_simulation import init_matrix
from simulated_annealing import simulated_annealing
from simulated_annealing import backup_simulated_annealing


fog_num = 3
starting_point = 3  # ehhez a ponthoz csatlakozik a service

# itt generáljuk a mintahálózatot
graph = graph_gen(fog_num)
graph.print_adj_list()

# meghatározzuk a legrövidebb utakat
network_latencies = dijkstra(graph, fog_num, starting_point)
print(network_latencies)

# inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
service_quantity = 4  # hány darab legyen
ms_per_service = 3  # servicenként mennyi ms legyen TODO: lehetne ez is változó
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
VMs_per_cloud = 8  # 2
fog_total_MIPS = [10000, 10000]  # 3
fog_total_RAM = [6000, 6000]  # 4
VMs_per_fog = 3  # 5
edge_total_MIPS = [1000, 1000]  # 6
edge_total_RAM = [10000, 10000]  # 7
VMs_per_edge = 3  # 8
cloud_cost_multiplier = 1  # 9
fog_cost_multiplier = 4  # 10
edge_cost_multiplier = 8  # 11
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
parameters.append(cloud_cost_multiplier)
parameters.append(fog_cost_multiplier)
parameters.append(edge_cost_multiplier)

nodes = init_nodes(fog_num, network_latencies, parameters)

# létrehozzuk a genetikus algoritmus kezdeti mátrixát
# csak a méretekhez kell
matrix = init_matrix(nodes, ms_list)

# szimulációs paraméterek
states_per_iteration = 100  # generált példányok iterációnként
T_0 = 1000  # kezdeti hőmérséklet
alpha = 0.95  # hűlési együttható
k_max = 1000  # iterációk száma

VM_num = 2*VMs_per_cloud + VMs_per_fog*fog_num + VMs_per_edge*fog_num*2
ms_num = len(ms_list)


# a szimuláció kimenete (Individual)
best_individual = simulated_annealing(nodes, ms_list, states_per_iteration,
                               VM_num, ms_num, service_quantity, ms_per_service,
                               T_0, alpha, k_max)

cost_of_best = cost_calculator(best_individual.matrix, nodes)

print("Best individual: ",best_individual.matrix)
print("Cost: ", cost_of_best)

# print("Best individual: ",best_individual.matrix)  # hibás értéket mutat
print("Fitness: ",best_individual.fitness)
#print("Backup matrix: ", backup_individual.matrix)

backup_individual = backup_simulated_annealing(nodes, ms_list,
                                               states_per_iteration,
                                               VM_num, ms_num, service_quantity,
                                               ms_per_service,
                                               T_0, alpha, k_max, best_individual.matrix)

print("Backup matrix: ", backup_individual.matrix)
print("Backup cost: ", backup_individual.fitness)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# A mátrix hibás, a fitness érték minden esetben helyes.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# latency_of_backup = calculate_fitness(backup_individual.matrix, nodes,
#                                      service_quantity,
#                                      ms_per_service, ms_list)

# print("Backup fitness: ", latency_of_backup)
