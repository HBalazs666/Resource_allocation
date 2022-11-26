import random
from classes import Individual


# inicializáljuk a kezdeti populációt
# ha a matrix_of_individual = matrix operációt alkalmazzuk,
# az hibás működést eredményez, mert megváltoztatja a matrix-ot is
def init_first(matrix, population_size, nodes, service_num,
               ms_num_per_service, ms_list):

    init_population = []

    for individual in range(population_size):

        matrix_of_individual = []

        for VM in range(len(matrix)):
            matrix_of_individual.append([])
            for MS in range(len(matrix[VM])):
                matrix_of_individual[VM].append(0)

        for MS in range(len(matrix_of_individual[0])):
            # melyik VM-re rakja az ms-t?
            ms_placement = random.randint(0, len(matrix_of_individual)-1)
            matrix_of_individual[ms_placement][MS] = 1

        latency_of_individual = calculate_fitness(matrix_of_individual,
                                                  nodes, service_num,
                                                  ms_num_per_service, ms_list)

        generated_individual = Individual(matrix_of_individual, latency_of_individual)

        init_population.append(generated_individual)

    return init_population


# VM sorszáma alapján kideríti, hogy melyik node-hoz tartozik
def node_finder(VM, nodes):
    
    first_VM_of_node = 0

    for node in nodes:

        if VM - first_VM_of_node < node.VM_quantity:

            return node
        
        first_VM_of_node = first_VM_of_node + node.VM_quantity

    return -1


def latency_calculator(ms, containing_node):

    # milliszekundumban
    latency = ((ms.CPU_req / containing_node.MIPS_per_VM) * 1000)

    return latency


# kiszámoljuk egy egyed fittségét
def calculate_fitness(matrix_of_individual, nodes, service_num,
                      ms_num_per_service, ms_list):

    # egy VM-en különböző servicekhez tartozó
    # MS-ek nem lehetnek
    for VM in range(len(matrix_of_individual)):

        for service in range(service_num):
            sum = 0
            
            for ms in range(ms_num_per_service):
                sum = sum + matrix_of_individual[VM][ms_num_per_service*service + ms]

            # ha ez igaz, akkor egyazon VM-en több service MS-e is fut,
            # ami nem megengedett
            if sum > 0 and sum != sum(matrix_of_individual[VM]):
                return 99999
    
    # az egyes VM-ek kapacitásait nem lehet meghaladni
    for VM in range(len(matrix_of_individual)):

        VM_MIPS_assumed = 0
        VM_RAM_assumed = 0

        node = node_finder(VM, nodes)

        for ms in range(len(matrix_of_individual[VM])):
            if matrix_of_individual[VM][ms] == 1:

                VM_MIPS_assumed = VM_MIPS_assumed + ms_list[ms].CPU_req
                VM_RAM_assumed = VM_RAM_assumed + ms_list[ms].RAM_req

        if VM_MIPS_assumed > node.MIPS_per_VM or VM_RAM_assumed > node.RAM_per_VM:

            return 99999

    # egy ms csak egy VM-en lehet egyszerre
    for ms in range(len(ms_list)):

        sum = 0

        for VM in range(matrix_of_individual):
            sum = sum + matrix_of_individual[VM][ms]

        if sum == 0 or sum > 1:
            return 99999


    # ha nincs ütközés a kikötések mentén, akkor normál módon
    # számolandó a késleltetés, ami megegyezik a fitness-értékkel is
    service_latencies = []
    latencies_by_VMs = []

    # a service_latencies számításához minden ms késleltetését
    # ismerni kell servicekhez rendelve
    for service in range(service_num):

        latencies_by_VMs.append([])

    for VM in range(len(matrix_of_individual)):

        latency_of_VM = 0
        latency_of_network = 0
        service_number = -1

        for ms in range(len(ms_list)):

            # ha az ms az adott VM-en van
            if matrix_of_individual[VM][ms] == 1:

                # kikeressük az ms-ek listájából
                actual_ms = ms_list[ms]

                # kiderítjük melyik service-hez tartozik
                service_number = int(ms/ms_num_per_service)

                # kiderítjük melyik node-hoz tartozik
                containing_node = node_finder(VM)
                latency_of_network = containing_node.network_latency

                # a paraméterek alapján kiszámoljuk a késleltetést a csomóponton
                # minden ms a VM-en additív tag
                latency_of_VM = latency_of_VM + latency_calculator(actual_ms, containing_node)

        # ezek alapján egy service késleltetése az általa használt
        # legnagyobb késleltetésű VM késleltetésének felel meg
        if latency_of_VM != 0:

            total_latency = latency_of_network + latency_of_VM
            latencies_by_VMs[service_number].append(total_latency)

    for service in range(service_num):

        service_latencies.append(max(latencies_by_VMs[service]))

    return sum(service_latencies)
                    

# kiválasztjuk a legjobb egyedeket az implementált szabály alapján
def select(generation):

    # latency szerint növekvő sorrendbe rakjuk az egyedeket
    generation.sort(key=lambda x: x.fitness, reverse=False)

    # a felső 20%-ot választjuk ki keresztezésre
    selected_individuals = generation[:int(0.2*len(generation))]

    return selected_individuals


# keresztezzük a legjobbakat
def crossover(selected_individuals, population_size):
    pass


# a lokális optimum elkerülése miatt mutációt végzünk az új populáción
# TODO: ezt is parametrizáljuk
def mutation(new_population):
    pass


def genetic_algorithm(matrix, nodes, ms_list, generation_num, population_size,
                      service_num, ms_num_per_service):

    first_generation = init_first(matrix, population_size, nodes, service_num,
                                  ms_num_per_service, ms_list)

    best_individuals = select(first_generation)