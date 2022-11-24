from classes import Microservice
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


def init_nodes(fog_num, network_latencies):

    node_num = fog_num+1+fog_num*2




def init_matrice():
    pass