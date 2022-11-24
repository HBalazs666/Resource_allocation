import random


class Graph:

    def __init__(self, num_of_nodes, directed=False):
        self.m_num_of_nodes = num_of_nodes
        self.m_nodes = range(self.m_num_of_nodes)

        # Define the type of a graph
        self.m_directed = directed

        self.m_adj_list = {node: [] for node in self.m_nodes}

    def print_adj_list(self):
        for key in self.m_adj_list.keys():
            print("node", key, ": ", self.m_adj_list[key])

    def add_edge(self, node1, node2, weight=1):
        self.m_adj_list[node1].append((node2, weight))
        
        if not self.m_directed:
            self.m_adj_list[node2].append((node1, weight))


class Individual:

    def __init__(self, node_length, service_length):
        # mátrix létrehozása
        offload =[]


    def __str__(self):

        return 'Fitness: ' + str(self.fitness)


class Node:

    def __init__(self, MIPS, RAM, VM_quantity, network_latency):
        self.MIPS = MIPS
        self.RAM = RAM
        self.network_latency = network_latency
        self.VM_quantity = VM_quantity
        self.MIPS_per_VM = int(MIPS/VM_quantity)
        self.RAM_per_VM = int(MIPS/RAM)


class Microservice:

    def __init__(self, MIPS_ms, RAM_ms, index):
        self.CPU_req = MIPS_ms
        self.RAM_req = RAM_ms
        self.index = index
        

class Service:
    
    def __init__(self, ms_list):
        self.ms_list = ms_list