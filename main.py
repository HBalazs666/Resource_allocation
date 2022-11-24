from classes import Node
import random

# 70-es cikkből lehet értékeket venni ezekhez
POPULATION = 50  # Ennyi db node legyen
GENERATIONS = 50  # Ennyi iteráció legyen

def init_network():
    pass



def ga(services):

    nodes = init_nodes(population)

    for generation in range(GENERATIONS):

        print('Generation: ' + str(generation))

        nodes = fitness(nodes)
        nodes = selection(nodes)
        nodes = crossover(nodes)
        nodes = mutation(nodes)


# Létrehozzuk a Node-okat
def init_individuals(population):

    # Erőforrásokat adunk minden node-nak.
    CPU =
    RAM =

    # Itt történik a létrehozás a paraméterekkel; a node-okat
    # listába fűzzűk
    return [Node(CPU, RAM) for node in range(population)]


def fitness(nodes):

    # minden node-hoz kiszámoljuk, hogy mennyi a fitness értéke
    for node in nodes:

        node.fitness = 

    return nodes


def selection(nodes):

    # sorbarendezzük a listát
    nodes = sorted(nodes, key=lambda node: node.fitness, reverse=True)
    print('\n'.join(map(str, nodes)))

    # vesszük a legjobb 20%-át a node-oknak
    nodes = nodes[:int(0.2 * len(nodes))]


def crossover(nodes):

    offspring = []

    for i in range((POPULATION - len(nodes)) / 2):

        parent1 = random.choice(nodes)
        parent2 = random.choice(nodes)  # lehet két egyforma (!!!)
        child1 = Node()
