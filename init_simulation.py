from classes import Microservice
from classes import Node
from classes import Individual
from genetic import calculate_fitness
import random


def init_ms_list(service_quantity, ms_per_service, MIPS_ms_max, MIPS_ms_min, RAM_ms_max, RAM_ms_min):
    
    ms_list = []

    # létrehozunk ms-eket, amikből a servicek felépülnek
    for index in range(service_quantity*ms_per_service):

        MIPS_ms = random.randint(MIPS_ms_min, MIPS_ms_max)
        RAM_ms = random.randint(RAM_ms_min, RAM_ms_max)
        ms = Microservice(MIPS_ms, RAM_ms, index)

        ms_list.append(ms)

    return ms_list


def init_nodes(fog_num, network_latencies, parameters):

    nodes = []

    node_num = fog_num+2+fog_num*2

    # ezek a fog és edge szerverek sorszámai:
    cloud_server = [0, 1]
    fog_servers = []
    edge_servers = []
    for fog_node in range(fog_num):
        fog = 2 + 3*fog_node
        fog_servers.append(fog)

        edge_servers.append(fog+1)
        edge_servers.append(fog+2)


    for node in range(node_num):

        if node == 0 or node == 1:
            MIPS = random.randint(parameters[0][0], parameters[0][1])
            RAM = random.randint(parameters[1][0], parameters[1][1])
            VM_quantity = parameters[2]
            cost_multiplier = parameters[9]
            cloud_server = Node(MIPS, RAM, VM_quantity, network_latencies[node], node,
                                cost_multiplier)

            nodes.append(cloud_server)

        elif node in fog_servers:
            MIPS = random.randint(parameters[3][0], parameters[3][1])
            RAM = random.randint(parameters[4][0], parameters[4][1])
            VM_quantity = parameters[5]
            cost_multiplier = parameters[10]
            fog_server = Node(MIPS, RAM, VM_quantity, network_latencies[node], node,
                              cost_multiplier)

            nodes.append(fog_server)

        elif node in edge_servers:
            MIPS = random.randint(parameters[6][0], parameters[6][1])
            RAM = random.randint(parameters[7][0], parameters[7][1])
            VM_quantity = parameters[8]
            cost_multiplier = parameters[11]
            edge_server = Node(MIPS, RAM, VM_quantity, network_latencies[node], node,
                               cost_multiplier)

            nodes.append(edge_server)

        else:
            print("BAD NUMBER OF NODES IN init_nodes()")


    return nodes


def init_matrix(nodes, ms_list):
    
    VM_sum = 0
    MS_sum = len(ms_list)

    for node in range(len(nodes)):
        VM_sum = VM_sum + nodes[node].VM_quantity

    matrix=[] #define empty matrix
    for i in range(VM_sum): #(VM-ek)
        row=[] 
        for j in range(MS_sum): #(MS-ek//gének)
            row.append(0) #adding 0 value for each column for this row
        matrix.append(row) #add fully defined column into the row

    return matrix


# SA algoritmus függvényei ------------------------------------------------------


def init_sa(VM_num, ms_num, nodes, service_num, ms_num_per_service, ms_list,
            cost_max):

    # kezdeti állapot létrehozása

    matrix_of_individual = []

    for VM in range(VM_num):
        matrix_of_individual.append([])
        for MS in range(ms_num):
            matrix_of_individual[VM].append(0)

    for MS in range(ms_num):
        # melyik VM-re rakja az ms-t?
        ms_placement = random.randint(0, VM_num-1)
        matrix_of_individual[ms_placement][MS] = 1

    init_fitness = calculate_fitness(matrix_of_individual, nodes, service_num,
                                     ms_num_per_service, ms_list, cost_max)

    init_individual = Individual(matrix_of_individual, init_fitness)

    return init_individual
