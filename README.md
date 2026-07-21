# [Trayectorias de Kepler y corrección relativista](/01-EDOs/)

Las trayectorias que trazan los planetas de nuestro sistema solar están dados por elipses, con el Sol en uno de sus focos. Dada la ecuación diferencial que modela estos recorridos, se nos presentaros dos situaciones:

## Modelo de Kepler

Las únicas fuerzas involucradas son las puntuales del planeta y del Sol. En este apartado la ecuación resultaba lineal y pudimos dar solución analítica en nuestro [informe](/01-EDOs/informe.pdf).

Hicimos uso de nuestra solución para graficar nuestras trayectorias bajo distintas [excentricidades](/01-EDOs/graficos/orbita_cerrada_ej2_8pi.pdf) (órbitas abiertas y cerradas) y proporciones.


## Corrección relativista de Einstein

En las traslaciones de los planetas se ven involucradas más fuerzas que sólo la de ellas y el Sol, para reflejar esta situación se añade una pequeña perturbación al modelo lo cual nos lleva a tener una EDO no lineal que resolvimos usando ```odeint``` de la biblioteca Scipy de Python. Con nuestro [código](/01-EDOs/main.py) pudimos explorar el impacto de la perturbación hecha al modelo de Kepler: el corrimiento del *perihelio*.

![Comparación de modelos](/01-EDOs/graficos/orbitas.png)

# [Identificación del número telefónico](/02-Fourier/)

Nos presentan dos audios: uno [limpio](/02-Fourier/tlfn-a.wav) y otro [ruidoso](/02-Fourier/tlfn-b.wav). Nuestro objetivo es, teniendo una tabla de codificación de los tonos telefónicos, descubrir a quién se llamó.

# [Resolución numérica de una ecuación de Poisson unidimensional](/03-EDPs/)
