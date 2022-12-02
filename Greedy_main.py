from docplex.mp.model import Model
from graph_gen import graph_gen
from graph_gen import dijkstra
from init_simulation import init_ms_list
from init_simulation import init_matrix
from init_simulation import init_nodes
from classes import Graph
from genetic import node_finder
from genetic import service_finder
from genetic import cost_calculator
from greedy import ms_order_by_RAM
import copy


# szimulációs paraméterek
# ------------------------------------------------------------
# költségkorlát
cost_max = 50000
latency_max = 100000

# hálózat mérete és csatlakozási pont
fog_num = 2
starting_point = 3

# inicializáljuk a serviceket (ms-ek létrehozásável) (nem irányított MS)
service_quantity = 1  # hány darab legyen
ms_per_service = 15  # servicenként mennyi ms legyen
MIPS_ms_min = 1000  # minimum MIPS
MIPS_ms_max = 1000  # maximum MIPS
RAM_ms_min = 10
RAM_ms_max = 10000

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

VM_num =fog_num*VMs_per_fog+2*VMs_per_cloud+2*fog_num*VMs_per_edge

# itt generáljuk a mintahálózatot
graph = graph_gen(fog_num)
graph.print_adj_list()

# meghatározzuk a legrövidebb utakat
network_latencies = dijkstra(graph, fog_num, starting_point)
print(network_latencies)

ms_list = init_ms_list(service_quantity, ms_per_service,
                       MIPS_ms_max, MIPS_ms_min, RAM_ms_max,
                       RAM_ms_min)

# rendezzük egyből csökkenő sorrendbe RAM szerint
ms_list.sort(key=lambda x: x.RAM_req, reverse=True)

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
matrix = init_matrix(nodes, ms_list)

# Innentől ILP -------------------------------------------------------

# tároljuk a más service által használt VM-eket, ezek tiltottak lesznek
is_used = []
MIPS_already_allocated = []
RAM_already_allocated = []
for VM in range(VM_num):
    is_used.append(-1)
    MIPS_already_allocated.append(0)
    RAM_already_allocated.append(0)

for ms in range(ms_per_service):
    act_ms = ms_list[ms]
    act_service = service_finder(act_ms.index, ms_per_service)

    # modell példányosítása
    opt_model = Model(name = "Opt")

    x_ijk = opt_model.binary_var_list(len(matrix), name='x_ijk')  # (VM)

    # constraint no.1: Egy microservicet ki kell szolgálni
    opt_model.add_constraint((sum(x_ijk[VM] for VM in range(len(matrix))) == 1))

    # constraint no.2: A virtuális gép memória kapacitáshatárának eleget kell tenni
    for VM in range(len(matrix)):
        
        node = node_finder(VM, nodes)

        c2 = opt_model.add_constraint((RAM_already_allocated[VM] + act_ms.RAM_req)*x_ijk[VM] <= nodes[node.index].RAM_per_VM)

    # constraint no.3: más service által használt VM-ek tiltottak
    for VM in range(VM_num):
        if is_used[VM] != -1 and is_used[VM] != act_service:
            opt_model.add_constraint(x_ijk[VM] <= 0)

    # constraint no.5: a késleltetéskorlátot tartani kell
    for VM in range(VM_num):
        act_node = node_finder(VM, nodes)
        opt_model.add_constraint(1000 * x_ijk[VM] * ((act_ms.CPU_req + MIPS_already_allocated[VM]) / act_node.MIPS_per_VM) <= latency_max)

    # VM-ek költségei
    VM_costs = []
    for VM in range(len(matrix)):

        act_node = node_finder(VM, nodes)
        VM_costs.append(act_node.MIPS_per_VM*act_node.cost_multiplier)

    # célfüggvény a költség minimalizálására
    obj_fn = sum(x_ijk[VM]*VM_costs[VM] for VM in range(VM_num))

    opt_model.set_objective('min', obj_fn)

    opt_model.print_information()

    opt_model.solve()
    opt_model.print_solution()

    # melyik VM volt a megoldás?
    VM_index = -1
    for VM_ind in range(VM_num):
        if x_ijk[VM].solution_value == 1:
            VM_index = VM_ind

    is_used[VM_ind] = act_service

    # mennyi helyet foglal (RAM)?
    RAM_already_allocated[VM_ind] = RAM_already_allocated[VM_ind] + act_ms.RAM_req

    # mennyi MIPS lett a sorban? 
    MIPS_already_allocated[VM] = MIPS_already_allocated[VM] + act_ms.CPU_req

    # tároljuk az eredményt a mátrixban
    matrix[VM_ind][act_ms.index] = 1

print(matrix)