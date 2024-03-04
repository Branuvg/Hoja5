import simpy
import numpy as np
import random
import statistics
import matplotlib.pyplot as plt

np.random.seed(10)
cant = 200

class Process:
    def __init__(self, name, env, cpu, memoria, instrucciones):
        self.env = env
        self.name = name
        self.cpu = cpu
        self.memoria = memoria
        self.instrucciones = instrucciones
        self.principio = -1
        self.fin = -2
        #print(f"{env.now} P {self.name} creado, memoria: {self.memoria}, instrucciones: {self.instrucciones}.")

    def rest(self):
        print(f"{env.now} [Waiting] P {self.name} hace envento I/O.")
        yield env.timeout(5)
        print(f"{env.now} [F Waiting] P {self.name} termino envento I/O.")

    def run(self):
        self.principio = env.now
        print(f"{env.now} P {self.name} creado, memoria: {self.memoria}, instrucciones: {self.instrucciones}.")
        while (self.instrucciones > 2):
            with self.cpu.request() as req:
                yield req # espera hasta que puede usar la pista
                print(f"{env.now} [Ready] P {self.name} a entrado al cpu.")
                waiting = random.randint(1,2)
                # hace un set de 3 instrucciones
                self.instrucciones -= 3 # tiene menos intrucciones que hacer
                yield env.timeout(1) # realiza el proceso
                if waiting == 1:
                    yield env.process(self.rest())
                else:
                    print(f"{env.now} [Ready] {self.name} Se va directamente a listo")
        print(f"{env.now} [Terminated] P {self.name} ha terminado sus procesos")
        self.fin = env.now
        tiempo_en_cpu = self.fin - self.principio
        tiempos_cpu.append(tiempo_en_cpu)

def simular(env, cpu):
    # creamos procesos
    for i in range(cant):
        name = f"Proceso_{i}"
        newprocesos = Process(name, env, cpu, np.random.randint(1,10), np.random.randint(1,10))
        lista_ejecuciones.append(newprocesos)
        env.process(newprocesos.run())
        yield env.timeout(1) # tiempo de creación entre procesos

tiempos_cpu = []
lista_ejecuciones = []
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)  # Define the race cpu as a shared resource
print("Llamada a simular")
env.process(simular(env, cpu))

env.run()

for c in lista_ejecuciones:
    print(f"{c.principio} , {c.fin}")  

# Después de env.run()
promedio = statistics.mean(tiempos_cpu)
desviacion_std = statistics.stdev(tiempos_cpu)

print("Promedio de tiempo en CPU:", promedio)
print("Desviación estándar de tiempo en CPU:", desviacion_std)

# Graficar
num_procesos = list(range(1, len(tiempos_cpu) + 1))
plt.plot(num_procesos, tiempos_cpu)
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio en CPU')
plt.title('Tiempo promedio en CPU por número de procesos')
plt.show()