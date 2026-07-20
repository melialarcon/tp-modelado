# -*- coding: utf-8 -*-
"""
TRÁBAJO PRÁCTICO N°3

Alumnos:
ALarcón, Melina
Belbrum, Axel
Dominguez, Rocio Julieta

"""

#%%
#IMPORTAMOS LIBRERIAS
import numpy as np
from matplotlib import pyplot as plt
from scipy.linalg import solve # para matrices sin aprovechar esparcidad
from scipy.sparse import diags_array # para matrices esparzas (ralas)
from scipy.sparse.linalg import spsolve # métodos para matrices esparzas
import time as time # para medir tiempos de ejecución

#%%########################
#        EJERCICIO 1      #
###########################

# El interior del dominio (filas 0 a nx-2) aproxima el operador u_xx mediante
# el esquema clásico de diferencias finitas centradas de orden 2:
# (u_{j-1} - 2u_j + u_{j+1}) / h^2 = f(x_j).
# Al estar multiplicado por 1/h^2, la diagonal principal almacena -2/h^2, y las
# diagonales adyacentes almacenan 1/h^2.
# La última fila (índice nx-1) se limpia por completo porque allí no aplica la
# ecuación diferencial, sino la condición de Neumann de orden 2 en el borde derecho:
# u_x(1)  (3u_N - 4u_{N-1} + u_{N-2}) / 2h = beta. Sus coeficientes ocupan las
# últimas tres posiciones de la fila, divididos por 2h.
def construir_matriz_densa(nx, h):
    A = np.zeros((nx, nx))
    for i in range(nx - 1):
        A[i, i] = -2.0
        if i > 0:
            A[i, i - 1] = 1.0
        A[i, i + 1] = 1.0
    A /= h * h

    # Condición de Neumann backward de orden 2
    A[nx - 1, :] = 0.0
    A[nx - 1, nx - 3] = 1.0 / (2.0 * h)
    A[nx - 1, nx - 2] = -4.0 / (2.0 * h)
    A[nx - 1, nx - 1] = 3.0 / (2.0 * h)
    return A

# se definen los vectores que representan las diagonales:
# principal, superior e inferior
# Para acoplar la condición de Neumann backward, se agrega una segunda diagonal
# inferior para el coeficiente del nodo u_{N-2}, y se pisan
# las últimas posiciones de cada vector diagonal para que coincidan
# exactamente con los coeficientes del borde (3/2h, -4/2h y 1/2h).
def construir_matriz_esparza(nx, h):
    diag_princ = -2.0 * np.ones(nx) / (h * h)
    diag_sup = 1.0 * np.ones(nx - 1) / (h * h)
    diag_inf = 1.0 * np.ones(nx - 1) / (h * h)
    diag_inf_2 = np.zeros(nx - 2)

    diag_princ[-1] = 3.0 / (2.0 * h)
    diag_inf[-1] = -4.0 / (2.0 * h)
    diag_inf_2[-1] = 1.0 / (2.0 * h)

    return diags_array([diag_princ, diag_sup, diag_inf, diag_inf_2], offsets=[0, 1, -1, -2]).tocsc()

# como Dirichlet fija u(0) = alfa,u_0 ya no es una incógnita. El sistema empieza resolviendo desde u_1. Por eso,la primera ecuación (b[0]) debe igualarse a f(x_1), lo que exige evaluar f en x[i + 1] a lo largo del bucle para no arrastrar el nodo x_0.
#Para el nodo x_1, la ecuación diferencial expandida es (1/h^2)*u_0 - (2/h^2)*u_1 + (1/h^2)*u_2 = f(x_1). Al ser u_0 conocido, modificamos el primer casillero como  b[0] -= alfa / h^2.
#  la ultima fila del sistema no responde a u_xx = f(x) sino al flujo del contorno (dirichlet). Por ello pisamos el bucle y se asignamos directamente la constante del flujo 'beta'.
def construir_vector_b(nx, h, x, alfa, beta, funcion_f):
    b = np.zeros(nx)
    for i in range(nx):
        b[i] = funcion_f(x[i + 1])

    b[0] -= alfa / (h * h)
    b[-1] = beta
    return b

#%%########################
#        EJERCICIO 2      #
###########################
def f(x):
    return np.sin(128 * np.pi * x)

def ue(x):
    return (-np.sin(128 * np.pi * x) / ((128 * np.pi)**2)) + ((1 + 1 / (128 * np.pi)) * x) + 2

# Parámetros y condiciones de contorno fijas del enunciado
alfa = 2.0
beta = 1.0

k_s = list(range(3, 15))

h_s = []
error_s = []

# para graficar la comparativa de tiempos de ejecución
tiempos_denso = []
tiempos_esparzo = []

#######################
# bucle de K para medir errores
###########################
for k in k_s:
    nx = 2**k + 1  # Cantidad de incógnitas
    h = 1.0 / nx   # Paso de la malla
    h_s.append(h)
    x = np.array([i * h for i in range(nx + 1)])  # Malla de puntos

    A = construir_matriz_densa(nx, h)
    Asp = construir_matriz_esparza(nx, h)
    b = construir_vector_b(nx, h, x, alfa, beta, f)

    t0 = time.time()
    u_aux = solve(A, b)
    t1 = time.time()
    tiempo_denso = t1 - t0
    tiempos_denso.append(tiempo_denso)

    t0sp = time.time()
    usp_aux = spsolve(Asp, b)
    t1sp = time.time()
    tiempo_esparzo = t1sp - t0sp
    tiempos_esparzo.append(tiempo_esparzo)

    u = np.concatenate(([alfa], u_aux))      # Reconstrucción con Dirichlet
    usp = np.concatenate(([alfa], usp_aux))  # Reconstrucción esparza
    uex = ue(x)                              # Solución exacta analítica

    if k==7: # para graficar la comparativa entre la solución real y la aproximada
        x_k7 = x
        u_k7 = u
        usp_k7 = usp

    # Error global en norma infinito (máximo error puntual)
    error = np.max(np.abs(uex - u))
    error_s.append(error)
    errorsp = np.max(np.abs(uex - usp))

    # Error de truncado residual en norma infinito
    e_d_t = np.max(np.abs(A @ u_aux - b))
    e_d_tsp = np.max(np.abs(Asp @ usp_aux - b))

    # Impresión de métricas en consola solicitadas
    print(f"--- Nivel k = {k} ---")
    print(f"Con matriz densa   -> Error: {error:.2e} | Truncado: {e_d_t:.2e} | Tiempo: {tiempo_denso:.6f}s")
    print(f"Con matriz esparza -> Error: {errorsp:.2e} | Truncado: {e_d_tsp:.2e} | Tiempo: {tiempo_esparzo:.6f}s\n")

    # --- GRÁFICO DE LOG(ERROR) VS LOG(H) ---
    if k == 3:  # Etiquetamos solo una vez en la leyenda
        plt.plot(np.log(h), np.log(error), 'or', label='Densa')
        plt.plot(np.log(h), np.log(errorsp), '*k', label='Esparza')
    else:
        plt.plot(np.log(h), np.log(error), 'or')
        plt.plot(np.log(h), np.log(errorsp), '*k')

    plt.annotate(f'k = {k}', (np.log(h), np.log(error)), xytext=None)

# Formateo del gráfico de errores acumulados
plt.legend()
plt.title('Error de aproximación')
plt.xlabel('log(h)')
plt.ylabel('log(error)')
plt.grid(ls=':', color='lavender')
plt.savefig('k_s.png', dpi = 300)
plt.show()

#%%###########################
# Regresion Lineal - Estimacion del orden
###########################

# Tomamos desde k=7 en adelante (índice 4 del vector) para evitar efectos de borde
log_h = np.log(np.array(h_s[4:]))
log_error = np.log(np.array(error_s[4:]))

ajuste = np.polyfit(log_h, log_error, 1)
print("=============================================================================")
print(f"La pendiente del ajuste resulta: {ajuste[0]:.4f}")
print("Este valor representa el orden de convergencia experimental del método (O(h²))")
print("=============================================================================")

# Gráfico del Ajuste de la Regresión
plt.plot(log_h, log_error, 'o:k', label='Aproximada')
plt.plot(log_h, ajuste[0] * log_h + ajuste[1], '-r', label='Ajuste Lineal')
plt.legend()
plt.grid(True, ls=':')
plt.title('Estimación del orden del método mediante regresión')
plt.xlabel('log(h)')
plt.ylabel('log(error)')
plt.savefig('ajuste.png', dpi = 300)
plt.show()

###########################
# Tiempos de ejecución
###########################

plt.plot(k_s, tiempos_denso, 'or:', label='Densa')
plt.plot(k_s, tiempos_esparzo, '*k:', label='Esparza')

plt.title('Tiempos de ejecución según k')
plt.xlabel('k')
plt.ylabel('Tiempo (s)')
plt.grid(ls=':', color='lavender')
plt.legend()

plt.savefig('tiempos.png', dpi = 300)
plt.show()

###########################
# Solución aproximada vs exacta
###########################

x_fino = np.arange(0, 1+0.001, 0.001)
uex_fino = ue(x_fino)

plt.plot(x_k7, u_k7, 'or', label='Aproximada Densa')
plt.plot(x_k7, usp_k7, '*k', label='Aproximada Esparza')
plt.plot(x_fino, uex_fino, '-b', label='Exacta')
plt.legend()
plt.grid(ls=':', color='lavender')
plt.title('Solución aproximada vs exacta para k = 7')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.savefig('solucionesk7.png', dpi = 300)
plt.show()

#%%########################
#        EJERCICIO 3      #
###########################

# Nueva función
def f_ej3(x):
    return np.exp(-x**2)

# Parámetros fijos
alfa = 2.0
beta = 1.0

###########################
#  Armamos un bucle de estres para encontrar el k maximo segun la capacidad de la maquina.
###########################

# Empezamos a probar desde k = 14 hacia arriba
k_prueba = 14
timeout = 10.0  # Límite de tiempo en segundos para considerar que tardó demasiado

print("Iniciando prueba de estrés con matrices esparzas...")
print("=====================================================")

while True:
    nx = 2**k_prueba + 1
    h = 1.0 / nx
    x = np.array([i * h for i in range(nx + 1)])

    try:
        # Intentamos armar la matriz esparza y el vector b
        Asp = construir_matriz_esparza(nx, h)
        b = construir_vector_b(nx, h, x, alfa, beta, f_ej3)

        # Medimos el tiempo que tarda el solver esparzo
        t0 = time.time()
        usp_aux = spsolve(Asp, b)
        t1 = time.time()

        tiempo_ejecucion = t1 - t0
        print(f"k = {k_prueba:2d} | N = {nx:10,d} | Tiempo: {tiempo_ejecucion:.4f}s -> K posible :) ")

        # Guardamos el último k exitoso y sus datos para graficarlo al final
        k_max_exitoso = k_prueba
        x_grafico = x
        usp_grafico = np.concatenate(([alfa], usp_aux))

        # Si tarda más de nuestro tiempo límite, cortamos por Timeout
        if tiempo_ejecucion > timeout:
            print(f"\n[TIMEOUT] Se detuvo el bucle en k = {k_prueba} porque tardó más de {timeout} segundos.")
            break

        # Pasamos al siguiente nivel de discretización
        k_prueba += 1

    except MemoryError:
        print(f"\n[MEMORY ERROR] ¡Tu RAM se agotó en k = {k_prueba} (N = {nx:,d})!")
        break
    except Exception as e:
        print(f"\n Ocurrió un error inesperado: {e}")
        break

print("=====================================================")
print(f"El mayor k que tu máquina pudo resolver eficientemente fue: k = {k_max_exitoso}")
print("=====================================================")


plt.figure()
plt.plot(x_grafico, usp_grafico, 'g-', label=f'Solución con k = {k_max_exitoso}')
plt.title(f'Solución para el N máximo alcanzable (k = {k_max_exitoso})')
plt.xlabel('Malla x')
plt.ylabel('u(x)')
plt.grid(ls=':', color='lavender')
plt.legend()
plt.show()
