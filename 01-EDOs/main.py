######################################################################
#TRABAJO PRÁCTICO 1 : Trayectorias de Kepler y Corrección relativista#
######################################################################

"""
Alumnos:
    *Alarcón, Melina
    *Belbrun, Axel
    *Dominguez, Rocio
"""

#%%
#Importamos las librerias que vamos a utilizar

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#%%####################################################################
#EJERCICIO 2 - Gráficos
#######################################################################

alpha = 1

#Usamos la definición de r en función del resto de parámetros.
def r(theta, epsilon):
    return alpha / (1 + epsilon * np.cos(theta))



#%%
#################################
# CASO ORBITAS CERRADAS 
#################################


#Graficamos para orbitas cerradas, es decir cuando 0<= ε <1
epsilons = [0, 0.2, 0.4, 0.6, 0.8, 0.9]
#%%
##############
# CASO < 2pi
##############
#Definimos el espacio dónde se va a mover nuestro argumento theta en el caso < 2pi.

theta = np.linspace(0, 2*np.pi, 1000)

plt.figure()

for epsilon in epsilons:
    rs = r(theta, epsilon)   #pasamos a coordenadas cartesianas
    x = rs * np.cos(theta)
    y = rs * np.sin(theta)

    plt.plot(x, y, label=f"ε = {epsilon}")

plt.scatter(0, 0, label="Sol")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Órbitas cerradas con δ = 0")
plt.legend()

plt.grid(ls = ':')
plt.savefig("orbita_cerrada_ej2_2pi.pdf", format="pdf", bbox_inches="tight")
plt.show()


#%%
#################
# CASO θ >= 6pi
#################
#Órbitas cerradas para el caso θ >= 6pi (3 o 4 vueltas)
theta = np.linspace(0, 8*np.pi, 1000)

plt.figure()

for epsilon in epsilons:
    rs = r(theta, epsilon)

    x = rs * np.cos(theta)
    y = rs * np.sin(theta)

    plt.plot(x, y, label=f"ε = {epsilon:.1f}")

plt.scatter(0, 0, label="Sol")
plt.xlabel("x")
plt.ylabel("y")

plt.title("Órbitas cerradas con δ = 0")
plt.legend()
plt.savefig("orbita_cerrada_ej2_8pi.pdf", format="pdf", bbox_inches="tight")

plt.grid(ls = ':')
plt.show()

#%%
#################################
# CASO ORBITAS ABIERTAS 
#################################


#%%
##############
# CASO < 2pi
##############
#Órbitas abiertas para el caso θ <= 2pi:

theta = np.linspace(0, 2*np.pi, 2000)

epsilons = [1, 1.2, 1.4, 1.6, 1.8, 1.9]

plt.figure()


for epsilon in epsilons:
    rs = r(theta, epsilon)

    x = rs * np.cos(theta)
    y = rs * np.sin(theta)

    plt.plot(x, y, label=f"ε = {epsilon:.1f}")

plt.scatter(0, 0, label="Sol")
plt.xlabel("x")
plt.ylabel("y")

#Límitamos los valores a los que pueden extenderse los ejes porque para ciertos valores la función tiene valores muy grandes
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title("Órbitas abiertas con δ = 0")
plt.legend()
plt.savefig("orbita_abierta_ej2_8pi.pdf", format="pdf", bbox_inches="tight")

plt.show()


#%%
#################
# CASO θ >= 6pi
#################

#Órbitas abiertas para el caso θ >= 6pi (3 o 4 vueltas):

theta = np.linspace(0, 8*np.pi, 2000)

plt.figure()


for epsilon in epsilons:
    rs = r(theta, epsilon)

    x = rs * np.cos(theta)
    y = rs * np.sin(theta)

    plt.plot(x, y, label=f"ε = {epsilon:.1f}")

plt.scatter(0, 0, label="Sol", color = 'k')
plt.xlabel("x")
plt.ylabel("y")

#Límitamos los valores a los que pueden extenderse los ejes porque para ciertos valores la función tiene valores muy grandes
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title("Órbitas abiertas con δ = 0")
plt.legend()
plt.savefig("orbita_abierta_ej2_8pi.pdf", format="pdf", bbox_inches="tight")
plt.grid(ls = ':')

plt.show()

#%%######################################################################
#Ejercicio 3 - Gráficos
#########################################################################

#################################
# CASO ORBITAS CERRADAS 
#################################

#%%
##############
# CASO < 2pi
##############
#Órbitas cerradas con δ = 0.05 y θ <= 2pi:
#Como los parámetros de la EDO quedan fijos para este ejercicio, los hard-codeamos.

def campo_f(u, theta, alfa):
    x, y = u
    dx_dt = y
    dy_dt = -x + 1/alfa + 0.05*(x**2)

    return dx_dt, dy_dt


lt = np.linspace(0, 8*np.pi, 1000)

alfas = [0.5, 1.0, 2.0]
epsilons = [0, 0.2, 0.6, 0.9]

for alfa in alfas:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect(1.0)

    for epsilon in epsilons:
        estado_inicial = [(1 + epsilon) / alfa, 0]
        solucion_odeint = odeint(campo_f, estado_inicial, lt, args=(alfa,))
        xs, ys = solucion_odeint.T
        rs = 1 / xs
        xxs = rs * np.cos(lt)
        yys = rs * np.sin(lt)
        ax.plot(xxs, yys, label=f'ε = {epsilon}')

    ax.scatter(0, 0, label="Sol", color = 'k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f"Órbitas cerradas con δ = 0.05 y α = {alfa}")
    ax.grid(ls = ':')
    ax.legend()
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    ax.set_xlim(max(xmin, -10), min(xmax, 10))
    ax.set_ylim(max(ymin, -10), min(ymax, 10))

    plt.savefig(f"orbita_cerrada_ej3_8pi_alfa{alfa}.pdf", format="pdf", bbox_inches="tight")
    plt.show()


#%%
#################
# CASO θ >= 6pi
#################

#Órbitas cerradas par δ = 0.05 y  θ >= 2pi:

lt = np.linspace(0, 8*np.pi, 1000)

alfas = [0.5, 1.0, 2.0]
epsilons = [0, 0.2, 0.6, 0.9]

for alfa in alfas:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect(1.0)

    for epsilon in epsilons:
        estado_inicial = [(1 + epsilon) / alfa, 0]
        solucion_odeint = odeint(campo_f, estado_inicial, lt, args=(alfa,))
        xs, ys = solucion_odeint.T
        rs = 1 / xs
        xxs = rs * np.cos(lt)
        yys = rs * np.sin(lt)
        ax.plot(xxs, yys, label=f'ε = {epsilon}')

    ax.scatter(0, 0, label="Sol", color = 'k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f"Órbitas cerradas con δ = 0.05 y α = {alfa}")
    ax.grid(ls = ':')
    ax.legend()
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    ax.set_xlim(max(xmin, -10), min(xmax, 10))
    ax.set_ylim(max(ymin, -10), min(ymax, 10))

    plt.savefig(f"orbita_cerrada_ej3_8pi_alfa{alfa}.pdf", format="pdf", bbox_inches="tight")
    plt.show()




#%%############################################
#Comparación: órbitas cerradas para distintos  δ
##################################################
epsilon = 0.8

theta = np.linspace(0, 25*np.pi, 1000) # vemos 25 períodos de la órbita


rs = r(theta, epsilon)
x = rs * np.cos(theta) # dominio kepler
y = rs * np.sin(theta) # imagen kepler


lt = np.linspace(0, 24*np.pi, 1000) # vemos 25 períodos de la órbita

# resolución numérica
estado_inicial = [1+epsilon, 0] # para odeint
alfa = 1
solucion_odeint = odeint(campo_f, estado_inicial, lt, args=(alfa,))
xs, ys = solucion_odeint.T

# Como xs = u entonces rs = 1/u = 1/xs
rs = 1/xs

#Pasamos ahora a coordenadas cartesianas:
xxs = rs*np.cos(np.array(lt)) # dominio relativista
yys = rs*np.sin(np.array(lt)) # imagen relativista

# -------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(16, 6.5))

ax[0].set_title(fr'Trayectorias de Kepler: $\delta$ = 0', fontsize = 16) 
ax[0].plot(x, y, label = 'Órbita')
ax[0].scatter(0,0,label = "Sol", color = 'k')
ax[0].legend()
ax[0].grid(ls=':') 

ax[1].set_title(fr'Corrección relativista: $\delta$ = 0.05', fontsize = 16) 
ax[1].plot(xxs, yys, label = 'Órbita')
ax[1].scatter(0,0,label = "Sol", color = 'k')
ax[1].legend()
ax[1].grid(ls=':')

plt.suptitle(fr'Órbitas Cerradas con $\alpha$ = 1, $\epsilon$ = 0.08 y $\theta$ = 24$\pi$ > 2$\pi$', fontsize = 18)
fig.subplots_adjust(top=0.85)

plt.savefig("orbitas", dpi=300)

plt.show()



#%%
#################################
# CASO ORBITAS ABIERTAS 
#################################


#%%
##############
# CASO < 2pi
##############


lt = np.linspace(0, 2*np.pi, 1000)
epsilons = [1, 1.2, 1.4, 1.6, 1.8, 1.9]

# alfa = 1??
alfa = 1
for epsilon in epsilons:
    estado_inicial = [(1+epsilon)/alfa, 0]
    # Solución numérica del sistema usando odeint en el mismo intervalo de t
    solucion_odeint = odeint(campo_f, estado_inicial, lt, args=(alfa,))

    xs, ys = solucion_odeint.T  # Transponer porque de odeint sale [x(t), y(t)] como matriz vertical.

    #Para graficar en coordenadas cartesianas, primero adaptamos los resultados de ODE_INT para tenerlos en función de r(tita):
    rs = 1/xs

    #Pasamos ahora a coordenadas cartesianas:
    xxs = rs*np.cos(np.array(lt))
    yys = rs*np.sin(np.array(lt))

    #Graficamos
    plt.plot(xxs, yys, label='ε = ' + str(epsilon))
plt.scatter(0,0, label = "Sol", color = 'k')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title("Órbitas abiertas con δ = 0.05")
plt.grid(ls = ':')
plt.legend()
plt.savefig("orbita_abierta_ej3_2pi.pdf", format="pdf", bbox_inches="tight")

plt.show()

#%%














