# [Trayectorias de Kepler y corrección relativista](/01-EDOs/)

Las trayectorias que trazan los planetas de nuestro sistema solar están dados por elipses, con el Sol en uno de sus focos. Dada la ecuación diferencial que modela estos recorridos, se nos presentaron dos situaciones:

## Modelo de Kepler

Las únicas fuerzas involucradas son las puntuales del planeta y del Sol. En este apartado la ecuación resultaba lineal y pudimos dar solución analítica en nuestro [informe](/01-EDOs/informe.pdf).

Hicimos uso de nuestra solución para graficar nuestras trayectorias bajo distintas [excentricidades](/01-EDOs/graficos/orbita_cerrada_ej2_8pi.pdf) (órbitas abiertas y cerradas) y proporciones.


## Corrección relativista de Einstein

En las traslaciones de los planetas se ven involucradas más fuerzas que sólo la de ellas y el Sol, para reflejar esta situación se añade una pequeña perturbación al modelo lo cual nos lleva a tener una EDO no lineal que resolvimos usando ```odeint``` de la biblioteca Scipy de Python. Con nuestro [código](/01-EDOs/main.py) pudimos explorar el impacto de la perturbación hecha al modelo de Kepler: el corrimiento del *perihelio*.

![Comparación de modelos](/01-EDOs/graficos/orbitas.png)

# [Identificación del número telefónico](/02-Fourier/)

Cuando marcamos un número telefónico, inevitablemente generaremos silencios intermedios que separan nuestros dígitos discados.

En este trabajo se nos facilitaron dos audios: uno [limpio](/02-Fourier/tlfn-a.wav) y otro [ruidoso](/02-Fourier/tlfn-b.wav). Dado que el sistema de marcación por tonos usa dos sinusoidales de frecuencias distintas para distinguir dígitos, nuestra tarea era la de lograr tomar muestras de las marcaciones de cada número, para así descubrir a quién se llamó en cada caso.


 * **Audio sin ruido:** Trabajamos con un [algoritmo de umbralización](/02-Fourier/main.py) para distinguir las marcaciones de dígitos.

 * **Audio con ruido:** Para lograr usar el mismo algoritmo, realizamos unos pasos previos:

      * Utilizamos la función ```fft``` del módulo ```scipy.fft``` de Python para obtener el [espectro frecuencias](/02-Fourier/graficos/freqs.png) de nuestro audio y analizarlo.
      * Diseñamos un [filtro](/02-Fourier/main.py) con el módulo ```signal``` de la biblioteca Scipy, que nos permitió separar las marcaciones de números del ruido.

      ![filtro](/02-Fourier/graficos/filtro%20pasa%20banda%20650%20a%201500.png)

      * Utilizamos el mismo algoritmo de umbralización para distinguir las marcaciones de los dígitos

# [Resolución numérica de una ecuación de Poisson unidimensional](/03-EDPs/)

Una ecuación en derivadas parciales, EDP, es aquella en la que la incógnita es una función de al menos dos variables independientes, y que en esta ecuación aparecen involucradas tanto la función como sus derivadas parciales
respecto de sus variables.
En el presente trabajo se nos presentó un sistema compuesto por una ecuación diferencial y dos condiciones de contorno. Resolver este sistema implica dar a conocer la función u que satisface la ecuación dada, u_xx(x) = f(x), que corresponde a una EDP de Poisson puesto que f no es la función cero (en tal caso sería de Laplace). Resolver también implica que nuestra solución cumple con las condiciones de contorno dadas: una de Dirichlet que nos indica el valor de u en la frontera de su dominio, y otra de Neumann que nos aporta información sobre la pendiente o derivada de nuestra función u también en la frontera.
Para dar respuesta al trabajo usamos las herramientas vistas en clase, y trabajamos con métodos de diferencias finitas que resuelven EDPs a partir la definición de una grilla de finitos nodos o puntos, que usamos para aproximar las derivadas de nuestra función y con ello construir un sistema de ecuaciones lineales en la que la incógnita resultaba ser la función buscada.
