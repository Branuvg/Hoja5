import simpy
import numpy as np
import random

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
        yield env.timeout(10)
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
                self.memoria -= 1 # gasta memoria
                self.instrucciones -= 3 # tiene menos intrucciones que hacer
                yield env.timeout(1) # realiza el proceso
                if waiting == 1:
                    yield env.process(self.rest())
                else:
                    print(f"{env.now} [Ready] {self.name} Se va directamente a listo")
            if self.memoria == 0:
                print(f"{env.now} P {self.name} pedira mas memoria.")
                # le toma un tiempo aleatorio poner gasolina.
                yield env.timeout(1)
                self.memoria = random.randint(1,10)
                print(f"{env.now} P {self.name} termina de poner memoria.")
        print(f"{env.now} [Terminated] P {self.name} ha terminado sus procesos")
        self.fin = env.now

def simular(env, cpu):
    # creamos procesos
    for i in range(100):
        name = f"Proceso_{i}"
        newCar = Process(name, env, cpu,
                     np.random.randint(1, 10),
                     np.random.randint(1, 10))
        lista_carros.append(newCar)
        env.process(newCar.run())
        yield env.timeout(1) # tiempo de creación entre procesos

lista_carros = []
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)  # Define the race cpu as a shared resource
print("Llamada a simular")
env.process(simular(env, cpu))

env.run()

for c in lista_carros:
    print(f"{c.principio} -- {c.fin}")