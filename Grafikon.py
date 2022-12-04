import matplotlib.pyplot as plt
import numpy as np

#ebbe kell beírni a fixalt parametereket a gorbeserghez
N = [10, 15, 20, 30, 50, 100]

#ezt a matrixot kell frissiteni
A_matrix = [[None, None, 6875.0, 6825.0, 5625.0, 4275.0, 5900.0, 5725.0, 4300.0, 4700.0, 3925.0, 5150.0, 3625.0, 4050.0, 3525.0, 5000.0, 3825.0, 5125.0, 3675.0, 3875.0], [9375.0, None, 5825.0, None, 3675.0, 4250.0, 3925.0, 4225.0, 3350.0, 4425.0, 3475.0, 3500.0, 3775.0, 3650.0, 3750.0, 3225.0, 3050.0, 2975.0, 2675.0, 2850.0], [7250.0, None, 6350.0, 5725.0, 3900.0, 5000.0, 8025.0, 3525.0, 3225.0, 3200.0, None, 3050.0, 3250.0, 3300.0, 2475.0, 3250.0, 2525.0, 2800.0, 2825.0, 2825.0], [5775.0, 5250.0, 4575.0, 4025.0, 4350.0, 9200.0, 3525.0, 3000.0, 3125.0, 2650.0, 3075.0, 2775.0, 2675.0, 2350.0, 2450.0, 2375.0, 2600.0, 2550.0, 1900.0, 2200.0], [None, 4200.0, 4225.0, 3975.0, 3400.0, 3275.0, 2625.0, 2850.0, 2475.0, 2275.0, 2350.0, 2375.0, 2700.0, 2500.0, 1975.0, 2600.0, 1650.0, 1875.0, 2175.0, 1575.0], [5750.0, 4600.0, 2800.0, 3075.0, 2875.0, 2450.0, 2375.0, 1975.0, 1950.0, 1650.0, 1750.0, 1650.0, 1700.0, 1775.0, 1825.0, 1650.0, 1650.0, 1675.0, 1875.0, 1675.0]]

def genetikus_gen_cel_egyedszam(N,y):
    fig, ax = plt.subplots()

    for i in range(len(N)):
        ax.plot(np.arange(10,len(y[0])*10+1,10), y[i], label = 'egyedszám: {}'.format(N[i]), linewidth = 1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(loc='upper right')

    ax.set(xlabel='Generáció szám [db]', ylabel='Késleltetés [ms]',
           title='Genetikus algoritmus: Populáció méretének hatása')

    ax.grid()

    #fig.savefig("test.png")
    plt.show()

#igy lehet meghivni a fenti fuggvenyt
genetikus_gen_cel_egyedszam(N,A_matrix)

def genetikus_two_axes(t, data1, data2):

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('iterációk')
    ax1.set_ylabel('késleltetés', color=color)
    ax1.plot(t, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('költség', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

# Igy lehet adatokat betolteni a kettos y tengelyu abrahoz. Ha az iteraciok szam anem 1-esevel no, a t helyett egy iteraciokat leiro array kell
t = np.arange(1,len(A_matrix[0])+1,1)
data1 = A_matrix[0]
data2 = A_matrix[1]
#genetikus_two_axes(t, data1, data2)