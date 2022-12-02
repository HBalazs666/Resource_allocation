from docplex.mp.model import Model
from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_ms_list
from init_simulation import init_matrix
from init_simulation import init_nodes
from classes import Graph
from genetic import node_finder
from genetic import cost_calculator

# szimulációs paraméterek
# ------------------------------------------------------------
# költségkorlát
cost_max = 50000 

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

# constraint no.4: A költségkorlátot is tartani kell
# VM-ek cost-ja:
cost_per_VM = []
for VM in range(len(matrix)):
    containing = node_finder(VM, nodes)
    cost_per_VM.append(containing.MIPS_per_VM * containing.cost_multiplier)

# jönnek a constraintek
opt_model.add_constraint(sum(sum(services[VM, service] for service in range(service_quantity)) * cost_per_VM[VM] for VM in range(len(matrix))) <= cost_max)

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

best_individual = []

for VM in range(len(matrix)):

    best_individual.append([])

    for MS in range(len(matrix[0])):
        best_individual[VM].append(int(x_ijk[(VM,MS)].solution_value))

print(best_individual)

cost = cost_calculator(best_individual, nodes)
print("Cost: ", cost)

# Innentől a backup dolgai
# --------------------------------------------------------
# modell példányosítása
opt_model_backup = Model(name = "Opt_backup")

# döntési változók (egyed mátrixa)
xx_ijk = opt_model_backup.binary_var_matrix(len(matrix), len(matrix[0]), name='xx_ijk')  # (VM, ms)
services = opt_model_backup.binary_var_matrix(len(matrix), service_quantity, name='services')  # (VM, service)

# constraint no.1.1: Minden backupot is ki kell szolgálni
c1 = opt_model_backup.add_constraints((sum([xx_ijk[VM, MS] for VM in range(len(matrix))]) == 1
                            for MS in range(len(matrix[0]))),
                            names='Task_completion')

# constraint no.2.2: A virtuális gép memória kapacitáshatárának eleget kell tenni
for VM in range(len(matrix)):
    
    node = node_finder(VM, nodes)

    c2 = opt_model_backup.add_constraint(sum(ms_list[MS].RAM_req*xx_ijk[VM, MS] for MS in range(len(matrix[0]))) <= nodes[node.index].RAM_per_VM)

# constraint no.3.3: Egy VM-en csak egy service backup ms-ei lehetnek
for VM in range(len(matrix)):
    for service in range(service_quantity):
        for ms in range(ms_per_service):

            c3 = opt_model_backup.add_constraint(xx_ijk[VM, ms + service*ms_per_service] <= services[VM, service])

    c32 = opt_model_backup.add_constraint(sum(services[VM, service] for service in range(service_quantity)) <= 1)

# constraint no.4: Egy ms backupját nem lehet ugyanarra a node-ra tenni, mint ahol
# az eredeti is van.

# Először meg kell tudni melyik node-on milyen ms-ek futnak
node_states = []
for nodey in range(2+fog_num+fog_num*2):
    node_states.append([])
    for MS in range(ms_per_service*service_quantity):
        node_states[nodey].append(0)

for VM in range(len(matrix)):

    act_node = node_finder(VM, nodes)

    for MS in range(len(matrix[VM])):

        if best_individual[VM][MS] == 1:
            node_states[act_node.index][MS] = 1

for nodex in range(len(node_states)):
    for MS in range(len(node_states[nodex])):

        if node_states[nodex][MS] == 1:

            # ekkor ezekre a VM-ekre nem kerülhet az MS backupja
            for VM in range(len(matrix)):
                containing_node = node_finder(VM, nodes)
                if containing_node.index == nodex:

                    opt_model_backup.add_constraint(xx_ijk[VM, MS] <= 0)

# VM-ek költségei
VM_costs = []
for VM in range(len(matrix)):

    act_node = node_finder(VM, nodes)
    VM_costs.append(act_node.MIPS_per_VM*act_node.cost_multiplier)

# Célfüggvény
obj_fn_backup = sum(VM_costs[VM] * sum(services[VM, service] for service in range(service_quantity)) for VM in range(len(matrix)))

opt_model_backup.set_objective('min', obj_fn_backup)

opt_model_backup.print_information()

opt_model_backup.solve()
opt_model_backup.print_solution()

best_individual_backup = []

for VM in range(len(matrix)):

    best_individual_backup.append([])

    for MS in range(len(matrix[0])):
        best_individual_backup[VM].append(int(xx_ijk[(VM,MS)].solution_value))

print(best_individual_backup)

cost = cost_calculator(best_individual_backup, nodes)
print("Cost of backup: ", cost)