import random


# inicializáljuk a kezdeti populációt
def init_first(matrix, population_size):
    
    init_population = []

    for individual in range(population_size):

        for VM in range(len(matrix)):
            for MS in range(len(matrix[VM])):
                matrix[VM][MS] = random.randint(0, 1)
        
        init_population.append(matrix)

    return init_population


# VM sorszáma alapján kideríti, hogy melyik node-hoz tartozik
def node_finder(VM, nodes):
    
    first_VM_of_node = 0

    for node in nodes:

        if VM - first_VM_of_node < node.VM_quantity:

            return node
        
        first_VM_of_node = node.VM_quantity

    return -1


def latency_calculator(ms, containing_node):

    latency = containing_node.network_latency + ((ms.CPU_req / containing_node.MIPS_per_VM) / 1000)

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
            if sum > 0:
                if sum != sum(matrix_of_individual[VM]):

                    return 99999
    
    # az egyes node-ok kapacitásait nem lehet meghaladni
    actual_VM = 0
    for node in nodes:

        for VM in range(node.VM_quantity):

            VM_MIPS_assumed = 0
            VM_RAM_assumed = 0

            for ms in range(len(matrix_of_individual[actual_VM])):
                if matrix_of_individual[actual_VM][ms] == 1:

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
    latencies_by_ms = []

    # a service_latencies számításához minden ms késleltetését
    # ismerni kell servicekhez rendelve
    for service in range(service_num):

        latencies_by_ms.append([])

    for VM in range(len(matrix_of_individual)):

        for ms in range(len(ms_list)):

            # ha az ms az adott VM-en van
            if matrix_of_individual[VM][ms] == 1:

                # kikeressük az ms-ek listájából
                actual_ms = ms_list[ms]

                # kiderítjük melyik service-hez tartozik
                service_number = int(ms/ms_num_per_service)

                # kiderítjük melyik node-hoz tartozik
                containing_node = node_finder(VM)

                # a paraméterek alapján kiszámoljuk
                # a késleltetést
                latency = latency_calculator(actual_ms, containing_node)

                # hozzáfűzzük a megfelelő listához
                latencies_by_ms[service_number].append(latency)

                # ezek alapján a késleltetés servicenként a legnagyobb
                # késleltetésű ms-nek felel meg
                for service in range(service_num):
                    service_latencies.append(max(latencies_by_ms[service]))

    return sum(service_latencies)
                    



# kiválasztjuk a legjobb egyedeket az implementált szabály alapján
def select(ordered_fitness_list):
    pass


# keresztezzük a legjobbakat
def crossover(selected_individuals, population_size):
    pass


# a lokális optimum elkerülése miatt mutációt végzünk az új populáción
# TODO: ezt is parametrizáljuk
def mutation(new_population):
    pass


def genetic_algorithm(matrix, nodes, ms_list, population_size,
                      generation_quantity, service_num, ms_num):
    
    init_first_population = init_first(matrix, population_size)