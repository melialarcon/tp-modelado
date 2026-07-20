############################################################
#TRABAJO PRÁCTICO 2 : Identificación del número telefónico #
############################################################

"""
Alumnos:
    *Alarcón, Melina
    *Belbrun, Axel
    *Dominguez, Rocio
"""

#%%
#Importamos las librerias que vamos a utilizar

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fft import fft, ifft, fftfreq, rfft, irfft # librerías para la fft

#%%
############################################################
#EJERCICIO 1
############################################################
######################
# cargamos el audio A
######################

fs1, data_a = wavfile.read("tlfn-a.wav") # fs1: la frecuencia de sampleo

#Vemos como se esperaba, dos canales de audio
print(data_a)

#Nos quedamos con el canal de audio izquierdo.
data_a_izq = data_a[:,0 ]
print(data_a_izq)

#Ahora procedemos a graficar para observar las amplitudes de las muestras

plt.plot(data_a_izq, 'b') # batata
plt.title('Gráfico archivo a')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid('True')
plt.show()

#Notemos que graficamos el numero de muestras
# para obtener un sentido fisico real, usamos la frecuencia de muestreo para graficar en funcion del tiempo
tiempo_a = np.arange(len(data_a_izq)) / fs1

plt.plot(tiempo_a, data_a_izq, 'b') # batata
plt.title('Gráfico archivo a (en segundos)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid('true')
plt.show()

#buscamos los intervalos de tiempo (ventanitas de marcado telefonico)
#usando segundos

# Para esquivar la Trampa de sube y baja por el cero, calculamos la "envolvente" (la silueta del bloque azul)
# Esto une todos los cruces por cero para que el bloque sea macizo
envolvente = np.abs(data_a_izq)

for i in range(1, len(envolvente)-1):
    envolvente[i] = max(envolvente[i-1]*0.99, envolvente[i]) # Mantiene arriba el valor

# algoritmo para detectar bloques de tiempo

inicios_muestras_a = []
fines_muestras_a = []
dentro_del_digito = False
UMBRAL_CERO = 5000 # Nuestro "cero" para esquivar la Trampa 1

for i in range(len(envolvente)):
    # Si encontrás un número distinto de "cero" (supera el umbral)
    if envolvente[i] > UMBRAL_CERO and not dentro_del_digito:
        inicios_muestras_a.append(i)
        dentro_del_digito = True

    # Si volvés a llegar a "cero" (cae por debajo del umbral)
    elif envolvente[i] < UMBRAL_CERO and dentro_del_digito:
        fines_muestras_a.append(i - 1)  # Guardás el anterior como fin
        dentro_del_digito = False

# INTERVALOS A SEGUNDOS
print("=== INTERVALOS ENCONTRADOS (audio A) ===")
for j in range(len(inicios_muestras_a)):
    t_inicio = inicios_muestras_a[j] / fs1
    t_fin = fines_muestras_a[j] / fs1
    print(f"Dígito {j+1}: de {t_inicio:.3f}s a {t_fin:.3f}s")

# calcular_ventanas_seguras nos permite, dado dados nuestros bloques de tiempo
# y un ancho para las ventanas, armar un subintervalo que capture mejor el tono de la señal
def calcular_ventanas_seguras(bloques, ancho_ventana=0.04): # Tomo 0.04s de ancho total para dejar un margen seguro antes del límite de 0.035s a cada lado
    ventanas = []
    for inicio, fin in bloques:
        # Calculamos el punto medio promediando inicio y fin
        punto_medio = (inicio + fin) / 2

        # Restamos y sumamos la mitad del ancho de la ventana (0.02 s)
        v_inicio = punto_medio - (ancho_ventana / 2)
        v_fin = punto_medio + (ancho_ventana / 2)

        ventanas.append([v_inicio, v_fin])
    return np.array(ventanas)

inicios_segundos = np.array(inicios_muestras_a) / fs1
fines_segundos = np.array(fines_muestras_a) / fs1
intervalos_bloques = np.array(list(zip(inicios_segundos, fines_segundos)))
ventanas_seguras_a = calcular_ventanas_seguras(intervalos_bloques)

print('Ventanas seguras para el audio A:')
for ventana in ventanas_seguras_a:
    print(f"Inicio: {ventana[0]:.3f}s, Fin: {ventana[1]:.3f}s")


#%%
#######################
# cargamos el audio B
######################
fs2, data_b = wavfile.read("tlfn-b.wav") # fs2: la frecuencia de sampleo

#Nos quedamos con el canal de audio izquierdo.
data_b_izq = data_b[:,0 ]
print(data_b_izq)

# Graficamos
plt.plot(data_b_izq, 'm') # membrillo
plt.title('Gráfico archivo b')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid('True')
plt.show()

# Usamos la frecuencia de muestreo para graficar en funcion del tiempo
tiempo_b = np.arange(len(data_b_izq)) / fs2

plt.plot(tiempo_b, data_b_izq, 'm') # membrillo
plt.title('Gráfico archivo b (en segundos)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid('true')

plt.show()

# Graficamos el espectro de frecuencias

Ck= fft(data_b_izq.copy())
N = len(data_b_izq)
frecuencias = fftfreq(N, 1/fs2)

# Tomamos la magnitud de la transformada y nos quedamos con la mitad positiva
magnitudesCk = np.abs(Ck[:N//2])
freqs_positivas = frecuencias[:N//2]

plt.figure(figsize=(12, 6))
plt.plot(freqs_positivas, magnitudesCk, '.', color = 'darkviolet')
plt.title('Espectro de Frecuencias del audio B')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid(ls = ':')
#plt.xlim(0, fs2 / 2) # Limitamos el eje x a la frecuencia de Nyquist (fs/2)
plt.xlim([40,1960]) # aquí están los primeros picos
plt.show()

# Buscamos la frecuencia del discado de números (la base, no el ruido)
# 1ra idea: El segundo pico podría ser la frecuencia base (la de los tonos)

Ck= fft(data_b_izq.copy())
plt.plot(range(1, 18001), np.abs(Ck[:18000]), 'o:', color = 'darkviolet') # vemos varios picos o frecuencias que intervienen
plt.xlim([1940,1960]) # voy a tomar el segundo pico como la freq_base
plt.title('Segundo Pico en el Espectro de Frecuencias del audio B')
plt.xlabel('Índice (Ck)')
plt.ylabel('Magnitud')
plt.grid(ls = ':')
plt.show()

freq_base=0
for i in range(1940,1960):
    if np.abs(Ck[i]) > freq_base:
        freq_base = np.abs(Ck[i])
#    print(f'{i} -> {np.abs(Ck[i]):.3f}')
print(f'La magnitud de la frecuencia base resulta: {freq_base}') # está en la posición 1946
N = len(data_b_izq)
fs = fs2
freq_base = 1946 * fs / N
print(f'La frecuencia base es {freq_base} Hz')

# Si el segundo pico es la frecuencia base, filtramos desde allí
x = data_b_izq.copy()
frec_corte = 500 # Parece que el discado de números ocurre a 440 Hz aproxi, cortamos en 500 por las dudas
sos = signal.butter(10, frec_corte, 'lowpass', fs = fs1, output = 'sos')

filtrado_inicial = signal.sosfilt(sos, x)

plt.plot(tiempo_b, filtrado_inicial, 'm')
plt.title('Gráfico archivo b con filtro pasa bajos a 500 Hz')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(ls=':')
plt.show()

# PROBLEMA: al parecer detectamos la frecuencia del ruido
x = data_b_izq.copy()
frec_corte = 500 # vemos qué ocurre si descartamos los primeros picos con un filtro pasa altos
sos2 = signal.butter(10, frec_corte, 'highpass', fs = fs1, output = 'sos')

filtrado_inicial2 = signal.sosfilt(sos2, x)

plt.plot(tiempo_b, filtrado_inicial2, 'm')
plt.title('Gráfico archivo b con filtro pasa altos a 500 Hz')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(ls=':')
plt.show()

# Graficamos las frecuencias originales vs. las contempladas por el primer filtro (pasa bajos a 500Hz)

N_filtered = len(filtrado_inicial)
Ck_filtered = fft(filtrado_inicial) # el de pasa bajos
frecuencias_filtered = fftfreq(N_filtered, 1/fs2)

magnitud_espectro_filtered = np.abs(Ck_filtered[:N_filtered//2])
frecuencias_positivas_filtered = frecuencias_filtered[:N_filtered//2]

plt.figure(figsize=(12, 6))
plt.plot(freqs_positivas, magnitudesCk, color = 'darkviolet', label='Original (audio B)', alpha=0.5)
plt.plot(frecuencias_positivas_filtered, magnitud_espectro_filtered, color = 'g', label='Filtrado (pasa bajos a 500 Hz)', alpha=0.7)
plt.title('Comparación del Espectro de Frecuencias (Original vs. Filtrado)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid('True')
plt.xlim(100, 1500)
#plt.xlim(650, 1500)
plt.legend()
plt.show()

# Usamos un filtro pasa banda para capturar estas frecuencias finales
x = data_b_izq.copy()

freq_corte_baja = 650
freq_corte_alta = 1500
sos = signal.butter(5, [freq_corte_baja, freq_corte_alta], btype='bandpass', fs=fs2, output='sos')

filtrado_final = signal.sosfilt(sos, x)

plt.plot(tiempo_b, filtrado_final, color='m')
#plt.xlim([10000,20000])
plt.title('Gráfico archivo b con filtro pasa banda de 650 a 1500 Hz')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(ls=':')
plt.show()

# Graficamos la señal original junto con la filtrada
plt.plot(tiempo_b, data_b_izq, 'm', label = 'Original')

plt.plot(tiempo_b, filtrado_final, color='k', label='Filtrada')
plt.title('Audio B antes y después del filtro pasa banda de 650 a 1500 Hz')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(ls=':')
plt.legend()
plt.show()

#buscamos los intervalos de tiempo (ventanitas de marcado telefonico)
#usando segundos

# Para esquivar la Trampa de sube y baja por el cero, calculamos la "envolvente" (la silueta del bloque azul)
# Esto une todos los cruces por cero para que el bloque sea macizo
envolvente = np.abs(filtrado_final) # usamos la señal ya filtrada
for i in range(1, len(envolvente)-1):
    envolvente[i] = max(envolvente[i-1]*0.99, envolvente[i]) # Mantiene arriba el valor

# algoritmo para detectar bloques de tiempo

inicios_muestras_b = []
fines_muestras_b = []
dentro_del_digito = False
UMBRAL_CERO = 1100  # Nuestro "cero" para esquivar la Trampa 1

for i in range(len(envolvente)):
    # Si encontrás un número distinto de "cero" (supera el umbral)
    if envolvente[i] > UMBRAL_CERO and not dentro_del_digito:
        inicios_muestras_b.append(i)
        dentro_del_digito = True

    # Si volvés a llegar a "cero" (cae por debajo del umbral)
    elif envolvente[i] < UMBRAL_CERO and dentro_del_digito:
        fines_muestras_b.append(i - 1)  # Guardás el anterior como fin
        dentro_del_digito = False

# INTERVALOS A SEGUNDOS
print("=== INTERVALOS ENCONTRADOS (audio B) ===")
for j in range(len(inicios_muestras_b)):
    t_inicio = inicios_muestras_b[j] / fs2
    t_fin = fines_muestras_b[j] / fs2
    print(f"Dígito {j+1}: de {t_inicio:.3f}s a {t_fin:.3f}s")

# calculamos las ventanas seguras
inicios_segundos = np.array(inicios_muestras_b) / fs2
fines_segundos = np.array(fines_muestras_b) / fs2
intervalos_bloques = np.array(list(zip(inicios_segundos, fines_segundos)))
ventanas_seguras_b = calcular_ventanas_seguras(intervalos_bloques)

print('Ventanas seguras para el audio B:')
for ventana in ventanas_seguras_b:
    print(f"Inicio: {ventana[0]:.3f}s, Fin: {ventana[1]:.3f}s")

# gráfico de la envolvente para el audio B filtrado
# esto nos ayudó a definir UMBRAL_CERO, pues donde la señal cortaba UMBRAL_CERO se definía un nuevo dítgito
# y a veces por cómo es la señal se cortaba antes de tiempo. 1100 fue el umbral óptimo
plt.figure(figsize=(15, 6))
plt.plot(tiempo_b, envolvente, 'darkviolet', alpha = 0.5, label='Envolvente de la señal filtrada')
plt.axhline(y=UMBRAL_CERO, color='r', linestyle='--', label=f'UMBRAL_CERO = {UMBRAL_CERO}')
plt.title('Envolvente de la Señal Filtrada con UMBRAL_CERO')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud de la Envolvente')

for inicio in inicios_muestras_b:
    plt.axvline(x=inicio / fs2, color='g', linestyle=':', linewidth=0.8)
for fin in fines_muestras_b:
    plt.axvline(x=fin / fs2, color='r', linestyle=':', linewidth=0.8)

plt.legend()
plt.grid('True')
plt.show()

#%%
############################################################
#EJERCICIO 2
############################################################

############
# ARCHIVO A
############
# detectamos las frecuencias de cada dígito
for idx, (t_ini,t_fin) in enumerate(ventanas_seguras_a,start =1):
  n_inicio = int(t_ini*fs1)
  n_fin = int(t_fin*fs1)

  muestra_tono = data_a_izq[n_inicio:n_fin]

  N=len(muestra_tono)

  transformada=fft(muestra_tono)
  frecuencias = fftfreq(N, 1/fs1)

  magnitud = np.abs(transformada) #medimos intensidad/amplitud de cada frec

  mascara_baja = (frecuencias >= 650) & (frecuencias <= 1000)
  mascara_alta = (frecuencias >= 1100) & (frecuencias <= 1600)

  frecuencias_bajas = frecuencias[mascara_baja]
  magnitudes_bajas = magnitud[mascara_baja]

  frecuencias_altas = frecuencias[mascara_alta]
  magnitudes_altas = magnitud[mascara_alta]

  #Buscamos el índice del máximo absoluto dentro de cada banda
  indice_pico_bajo = np.argmax(magnitudes_bajas)
  indice_pico_alto = np.argmax(magnitudes_altas)

  #Recuperamos las frecuencias exactas asociadas a esos picos
  frec_baja_detectada = frecuencias_bajas[indice_pico_bajo]
  frec_alta_detectada = frecuencias_altas[indice_pico_alto]

  print(f"\nDígito {idx}")
  print(f"Frecuencias componentes:")
  print(f"Baja: {frec_baja_detectada:.1f} Hz")
  print(f"Alta: {frec_alta_detectada:.1f} Hz")
  
#%%
############################################################
#EJERCICIO 2
############################################################

############
# ARCHIVO B
###########

# detectamos las frecuencias de cada dígito
for idx, (t_ini,t_fin) in enumerate(ventanas_seguras_b,start =1):
  n_inicio = int(t_ini*fs2)
  n_fin = int(t_fin*fs2)

  muestra_tono = filtrado_final[n_inicio:n_fin]

  N=len(muestra_tono)

  transformada=fft(muestra_tono)
  frecuencias = fftfreq(N, 1/fs2)

  magnitud = np.abs(transformada) #medimos intensidad/amplitud de cada frec

  mascara_baja = (frecuencias >= 650) & (frecuencias <= 1000)
  mascara_alta = (frecuencias >= 1100) & (frecuencias <= 1600)

  frecuencias_bajas = frecuencias[mascara_baja]
  magnitudes_bajas = magnitud[mascara_baja]

  frecuencias_altas = frecuencias[mascara_alta]
  magnitudes_altas = magnitud[mascara_alta]

  #Buscamos el índice del máximo absoluto dentro de cada banda
  indice_pico_bajo = np.argmax(magnitudes_bajas)
  indice_pico_alto = np.argmax(magnitudes_altas)

  #Recuperamos las frecuencias exactas asociadas a esos picos
  frec_baja_detectada = frecuencias_bajas[indice_pico_bajo]
  frec_alta_detectada = frecuencias_altas[indice_pico_alto]

  print(f"\nDígito {idx}")
  print(f"Frecuencias componentes:")
  print(f"Baja: {frec_baja_detectada:.1f} Hz")
  print(f"Alta: {frec_alta_detectada:.1f} Hz")
