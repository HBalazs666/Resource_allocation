from classes import Graph, Node
import random

def graph_gen(fog_num):

    node_counter = 0
    node_num = fog_num+1+fog_num*2

    graph = Graph(node_num)

    # ha a fog_num 1:
    # cloud csatlakozása
    graph.add_edge(1, 0, random.randint(2000, 2000))

    # edge csatlakozások
    graph.add_edge(1, 2, random.randint(2000, 2000))
    graph.add_edge(1, 3, random.randint(2000, 2000))

    node_counter = 3  # azaz 4 node van, hiszen 0-tól számol

    if fog_num > 1:
        for fog in range(fog_num-1):
            # először a fog eszköz, ami a cloud-hoz és az előző fog-hoz csatlakozik:
            graph.add_edge(node_counter+1, 0, random.randint(90000, 90000))
            graph.add_edge(node_counter+1, node_counter-2, random.randint(300, 400))

            # most a két edge csatlakozás jön:
            graph.add_edge(node_counter+1, node_counter+2, random.randint(1000, 2000))
            graph.add_edge(node_counter+1, node_counter+3, random.randint(1000, 2000))

            node_counter = node_counter+3

    # graph.print_adj_list
    
    return graph


def calculate_actual_neighbours(graph, list_of_neighbours, checked, distances):

    list_of_new_neighbours = []

    # az előző ciklus minden szomszédját bejárjuk
    for neighbour in range(len(list_of_neighbours)):

        conn = []
        latency = []
        
        act_node = list_of_neighbours[neighbour][0]
        if act_node in checked: continue

        act_latency = distances[act_node]

        # kikeressük az összes szomszédot a hozzájuk tartozó eljutási idővel
        for neighbour_node in range(len(graph.m_adj_list[act_node])):

            # kihez csatlakozik
            conn.append(graph.m_adj_list[act_node][neighbour_node][0])

            # milyen késleltetéssel
            latency.append(act_latency + graph.m_adj_list[act_node][neighbour_node][1])

            # tuple-t csinálunk a node és hozzá tartozó latencyből
            for neighbour in range(len(conn)):
                list_of_new_neighbours.append((conn[neighbour], latency[neighbour]))

        # rendezzük növekvő sorrendbe késleltetés szerint
        list_of_new_neighbours.sort(key=lambda tup: tup[1])

        # dijkstra táblázat javítása
        for neighbour_1 in range(len(list_of_new_neighbours)):

            if act_latency + list_of_new_neighbours[neighbour_1][1] < distances[list_of_new_neighbours[neighbour_1][0]]:
                distances[list_of_new_neighbours[neighbour_1][0]] = list_of_new_neighbours[neighbour_1][1]


        checked.append(act_node)

    return [list_of_new_neighbours, checked, distances]


def dijkstra(graph, fog_num, starting_point):

    node_num = fog_num+1+fog_num*2

    # inicializáció
    distances = []
    for node in range(node_num):
        distances.append(99999)
    distances[starting_point] = 0

    # aktuális pozíció és késleltetés
    act_node = starting_point
    act_latency = 0

    conn = []
    latency = []
    checked = []
    list_of_neighbours = []

    # első pont
    for neighbour_node in range(len(graph.m_adj_list[act_node])):
        # kihez csatlakozik
        conn.append(graph.m_adj_list[act_node][neighbour_node][0])

        # milyen késleltetéssel
        latency.append(act_latency + graph.m_adj_list[act_node][neighbour_node][1])

        # tuple-t csinálunk a node és hozzá tartozó latencyből
        for neighbour in range(len(conn)):
            list_of_neighbours.append((conn[neighbour], latency[neighbour]))

    # rendezzük növekvő sorrendbe késleltetés szerint
    list_of_neighbours.sort(key=lambda tup: tup[1])

    # dijkstra táblázat javítása
    for neighbour in range(len(list_of_neighbours)):

        if list_of_neighbours[neighbour][1] < distances[list_of_neighbours[neighbour][0]]:
            distances[list_of_neighbours[neighbour][0]] = list_of_neighbours[neighbour][1]

    # betesszük a bejárt node-ok listájába
    checked.append(act_node)


    # addig megy az algoritmus, amíg nincs már új node
    while len(list_of_neighbours) != 0:

        result = calculate_actual_neighbours(graph, list_of_neighbours, checked, distances)
        list_of_neighbours = result[0]
        checked = result[1]
        distances = result[2]

    return distances