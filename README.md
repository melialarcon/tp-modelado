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

 * **Audio con ruido:** Requerimos del siguiente tratamiento:

      * Utilizamos la función ```fft``` del módulo ```scipy.fft``` de Python para obtener el [espectro frecuencias](/02-Fourier/graficos/freqs.png) de nuestro audio y analizarlo.
      * Diseñamos un [filtro](/02-Fourier/graficos/filtro%20pasa%20banda%20650%20a%201500.png) con el módulo ```signal``` de la biblioteca Scipy, que nos permitió separar las marcaciones de números del ruido.
      * Utilizamos el mismo algoritmo de umbralización para distinguir las marcaciones de los dígitos sobre la señal filtrada.
  
Hicimos uso de la función ```fft``` del módulo ```scipy.fft``` para hallar las frecuencias altas y bajas con mayor presencia en cada marcación hallada y así descifrar a quién se llamó.

# [Resolución numérica de una ecuación de Poisson unidimensional](/03-EDPs/)

En el contexto de una EDP, poder dar una solución mediante aproximaciones implica una discretización del dominio usando una malla. Refinar nuestra malla para dar una respuesta más fiel, nos cuesta poder de cómputo puesto que se utilizan matrices que aumentan exponencialmente de tamaño.

En el presente trabajo se nos presentó una EDP que quisimos resolver aproximadamente:
 - Usamos métodos de diferencias finitas para armar sistemas lineales cuya incógnita era la solución de nuestra EDP.
 - Armamos los sistemas tanto con matrices ralas como densas usando el módulo ```scipy.sparse``` y la biblioteca ```numpy``` respectivamente.
 - Resolvimos los sistemas con distintos solves según el tipo de matrices involucradas: ```spsolve``` para ralas y ```solve``` para densas.

[Comparamos](/03-EDPs/graficos/tiempos.png) la eficiencia de los distintos tipos de matrices para distintos refinamientos de la malla, y observamos que el orden de convergencia de nuestro método se podía estimar con una [regresión lineal](/03-EDPs/graficos/ajuste.png) sobre nuestros errores de aproximación.
