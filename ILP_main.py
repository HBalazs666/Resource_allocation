from docplex.mp.model import Model
from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_ms_list
from init_simulation import init_matrix
from init_simulation import init_nodes
from classes import Graph
from genetic import node_finder


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

# létrehozzuk a genetikus algoritmus kezdeti mátrixát
# csak a méretekhez kell
matrix = init_matrix(nodes, ms_list)

# Innentől ILP -------------------------------------------------------

# modell példányosítása
opt_model = Model(name = "Opt")

# döntési változók (egyed mátrixa)
x_ijk = opt_model.binary_var_matrix(len(matrix), len(matrix[0]), name='x_ijk')  # (VM, ms)
services = opt_model.binary_var_matrix(len(matrix), service_quantity, name='services')  # (VM, service)

# constraint no.1: Minden microservicet ki kell szolgálni, azaz minden microservice pontosan 1 gépen fut
c1 = opt_model.add_constraints((sum([x_ijk[VM, MS] for VM in range(len(matrix))]) == 1
                            for MS in range(len(matrix[0]))),
                            names='Task_completion')

# constraint no.2: A virtuális gép memória kapacitáshatárának eleget kell tenni
for VM in range(len(matrix)):
    
    node = node_finder(VM, nodes)

    c2 = opt_model.add_constraint(sum(ms_list[MS].RAM_req*x_ijk[VM, MS] for MS in range(len(matrix[0]))) <= nodes[node.index].RAM_per_VM)

# constraint no.3: Egy VM-en csak egy service ms-ei lehetnek
for VM in range(len(matrix)):
    for service in range(service_quantity):
        for ms in range(ms_per_service):

            c3 = opt_model.add_constraint(x_ijk[VM, ms + service*ms_per_service] <= services[VM, service])

    c32 = opt_model.add_constraint(sum(services[VM, service] for service in range(service_quantity)) <= 1)

# célfüggvény
# VM-ek késleltetésösszegének minimalizálása
VM_network_latencies = []
VM_MIPS = []
for VM in range(len(matrix)):
    act_VM = node_finder(VM, nodes)
    VM_network_latencies.append(act_VM.network_latency)
    VM_MIPS.append(act_VM.MIPS_per_VM)

# c_i = (sum(x_ijk[VM, MS] * (ms_list[MS].CPU_req) for MS in range(len(ms_list))) + VM_network_latencies[VM])
#obj_fn = sum((sum(x_ijk[VM, MS] * (ms_list[MS].CPU_req / VM_MIPS[VM] * 1000) for MS in range(len(ms_list))) + VM_network_latencies[VM]) * \
#         sum(services[VM, service] for service in range(service_quantity)) for VM in range(len(matrix)) )

obj_fn = sum(sum(x_ijk[VM, MS] * (ms_list[MS].CPU_req / VM_MIPS[VM] * 1000) for MS in range(len(ms_list))) + sum(services[VM, service] for service in range(service_quantity))*VM_network_latencies[VM] for VM in range(len(matrix)))

opt_model.set_objective('min', obj_fn)

opt_model.print_information()

opt_model.solve()
opt_model.print_solution()