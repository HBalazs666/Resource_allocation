import random


# inicializáljuk a kezdeti populációt
def init_first(matrix, population_size):
    pass


# kiszámoljuk az egyes egyedek fittségét és
# növekvő sorrendben visszaadjuk az indexüket
def calculate_fitness(matrix_list):
    pass


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


def genetic_algorithm(matrix, nodes, ms_list, population_size):
    
    init_first_population = init_first(matrix, population_size)