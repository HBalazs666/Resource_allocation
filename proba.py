from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_matrice
from init_simulation import init_nodes
from init_simulation import init_ms_list


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
cloud_total_MIPS = []  # 0
cloud_total_RAM = []  # 1
VMs_per_cloud = 100  # 2
fog_total_MIPS = []  # 3
fog_total_RAM = []  # 4
VMs_per_fog = 8  # 5
edge_total_MIPS = []  # 6
edge_total_RAM = []  # 7
VMs_per_edge = 4  # 8
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
matrice = init_matrice(nodes, ms_list)

