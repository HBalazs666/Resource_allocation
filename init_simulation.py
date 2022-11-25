from classes import Microservice
from classes import Node
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

    node_num = fog_num+1+fog_num*2

    # ezek a fog és edge szerverek sorszámai:
    cloud_server = 0
    fog_servers = []
    edge_servers = []
    for fog_node in range(fog_num):
        fog = 1 + 3*fog_node
        fog_servers.append(fog)

        edge_servers.append(fog+1)
        edge_servers.append(fog+2)


    for node in range(node_num):

        if node == 0:
            MIPS = random.randint(parameters[0][0], parameters[0][1])
            RAM = random.randint(parameters[1][0], parameters[1][1])
            VM_quantity = parameters[2]
            cloud_server = Node(MIPS, RAM, VM_quantity, network_latencies[node], node)

            nodes.append(cloud_server)

        elif node in fog_servers:
            MIPS = random.randint(parameters[3][0], parameters[3][1])
            RAM = random.randint(parameters[4][0], parameters[4][1])
            VM_quantity = parameters[5]
            fog_server = Node(MIPS, RAM, VM_quantity, network_latencies[node], node)

            nodes.append(fog_server)

        elif node in edge_servers:
            MIPS = random.randint(parameters[6][0], parameters[6][1])
            RAM = random.randint(parameters[7][0], parameters[7][1])
            VM_quantity = parameters[8]
            edge_server = Node(MIPS, RAM, VM_quantity, network_latencies[node], node)

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
    for i in range(VM_sum): #total row is 3 (VM-ek)
        row=[] 
        for j in range(MS_sum): #total column is 3 (MS-ek//gének)
            row.append(0) #adding 0 value for each column for this row
        matrix.append(row) #add fully defined column into the row

    return matrix