# [Trayectorias de Kepler y corrección relativista](/01-EDOs/)

Las trayectorias que trazan los planetas de nuestro sistema solar están dados por elipses, con el Sol en uno de sus focos. Dada la ecuación diferencial que modela estos recorridos, se nos presentaron dos situaciones:

## Modelo de Kepler

Las únicas fuerzas involucradas son las puntuales del planeta y del Sol. En este apartado la ecuación resultaba lineal y pudimos dar solución analítica en nuestro [informe](/01-EDOs/informe.pdf).

Hicimos uso de nuestra solución para graficar nuestras trayectorias bajo distintas [excentricidades](/01-EDOs/graficos/orbita_cerrada_ej2_8pi.pdf) (órbitas abiertas y cerradas) y proporciones.


## Corrección relativista de Einstein

En las traslaciones de los planetas se ven involucradas más fuerzas que sólo la de ellas y el Sol, para reflejar esta situación se añade una pequeña perturbación al modelo lo cual nos lleva a tener una EDO no lineal que resolvimos numéricamente usando ```odeint``` de la biblioteca Scipy de Python. Con nuestro [código](/01-EDOs/main.py) pudimos explorar el impacto de la perturbación hecha al modelo de Kepler: el corrimiento del *perihelio*.

![Comparación de modelos](/01-EDOs/graficos/orbitas.png)

# [Identificación del número telefónico](/02-Fourier/)

Cuando marcamos un número telefónico, inevitablemente generaremos silencios intermedios que separan nuestros dígitos discados.

En este trabajo se nos facilitaron dos audios: uno [limpio](/02-Fourier/graficos/grafico_a_seg.png) y otro [ruidoso](/02-Fourier/graficos/grafico_b_seg.png). Dado que el sistema de marcación por tonos usa dos sinusoidales de frecuencias distintas para distinguir dígitos, nuestra tarea era la de lograr tomar muestras de las marcaciones de cada número, para así descubrir a quién se llamó en cada caso.

 * **Audio sin ruido:** Trabajamos con un [algoritmo de umbralización](/02-Fourier/main.py) para distinguir las marcaciones de dígitos.

 * **Audio con ruido:** Requerimos del siguiente tratamiento:

      * Utilizamos la función ```fft``` del módulo ```scipy.fft``` de Python para obtener el [espectro frecuencias](/02-Fourier/graficos/freqs.png) de nuestro audio y analizarlo.
      * Diseñamos un [filtro](/02-Fourier/graficos/filtro%20pasa%20banda%20650%20a%201500.png) con el módulo ```signal``` de la biblioteca Scipy, que nos permitió separar las marcaciones de números del ruido.
      * Utilizamos el mismo algoritmo de umbralización para distinguir las marcaciones de los dígitos sobre la señal filtrada.
  
Hicimos uso de la función ```fft``` del módulo ```scipy.fft``` para hallar las frecuencias altas y bajas con mayor presencia en cada marcación hallada y así descifrar a quién se llamó.

# [Resolución numérica de una ecuación de Poisson unidimensional](/03-EDPs/)

En el contexto de una EDP, dar una solución numérica implica discretizar el dominio mediante una malla. Refinar la malla para dar una respuesta más exacta nos cuesta poder de cómputo, puesto que se utilizan matrices que aumentan exponencialmente su tamaño.

En este trabajo se nos presentó una EDP que resolvimos numéricamente:
 - Usamos métodos de diferencias finitas que desarrollamos en nuestro [informe](/03-EDPs/informe.pdf).
 - Usamos matrices ralas y densas usando el módulo ```scipy.sparse``` y la biblioteca ```numpy``` respectivamente.
 - [Programamos](/03-EDPs/main.py) nuestros sistemas lineales que resolvimos usando ```spsolve``` y ```solve``` según el tipo de matriz usada.

Nos pareció interesante [comparar](/03-EDPs/graficos/tiempos.png) la eficiencia de las matrices ralas y densas para distintos refinamientos de la malla, y observamos que el orden de convergencia de nuestro método se podía estimar con una [regresión lineal](/03-EDPs/graficos/ajuste.png) sobre nuestros errores de aproximación.

Por último, realizamos pruebas de estrés para encontrar el refinamiento máximo que soportaba nuestra computadora y graficamos su resultado.

![Máximo k](/03-EDPs/graficos/k_mas_alto.png)
