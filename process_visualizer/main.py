"""
Seminario de Solución de Problemas de Sistemas Operativos - D05 - 28/09/2023
Actividad #8 - Concurrencia, el problema de los lectores y escritores.
Abraham Magaña Hernández - 220791217
"""

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

from includes.core_progress_bars_threads import *
from includes.info_threads import *
from includes.process_threads import *

from includes.fcfs_thread import *
from includes.rr_thread import *
from includes.priority_thread import *
from includes.queue_thread import *

from includes.pc_thread import *
from includes.rw_thread import *

from includes.real_memory_thread import *

import random
import sys
import os

"""
Esta es la clase principal de la ventana donde se muestran los procesos, a lo largo del codigo se va a documentar esta
misma clase pero en secciones, para entenderse mejor.
"""

class process_manager(QMainWindow):

    # Constructor de la clase principal.

    def __init__(self) -> None:

        super(process_manager, self).__init__()
        uic.loadUi('graphics/window_updated.ui', self) # Cargamos la interfaz hecha en QtDesigner.
        self.setWindowTitle('Process Manager - Abraham Magaña Hernández')

        self.setFixedSize(self.size())

        # Tupla con las barras de procesos de los núcleos.

        self.cpu_process_bars = (self.first_core_progressbar, self.second_core_progressbar, self.third_core_progressbar, self.fourth_core_progressbar)

        # Tupla con las labels de id, usuario, estado y barra de procesos.

        self.processes = [
            [self.token_0, self.user_0, self.state_0, self.progress_0, self.time_0, self.priority_0, self.located_0],
            [self.token_1, self.user_1, self.state_1, self.progress_1, self.time_1, self.priority_1, self.located_1],
            [self.token_2, self.user_2, self.state_2, self.progress_2, self.time_2, self.priority_2, self.located_2],
            [self.token_3, self.user_3, self.state_3, self.progress_3, self.time_3, self.priority_3, self.located_3],
            [self.token_4, self.user_4, self.state_4, self.progress_4, self.time_4, self.priority_4, self.located_4],
            [self.token_5, self.user_5, self.state_5, self.progress_5, self.time_5, self.priority_5, self.located_5],
            [self.token_6, self.user_6, self.state_6, self.progress_6, self.time_6, self.priority_6, self.located_6],
            [self.token_7, self.user_7, self.state_7, self.progress_7, self.time_7, self.priority_7, self.located_7]
        ]

        self.numbers: list = [int]
        self.times: list = [int]
            
        # Inicializamos los procesos.

        for process in self.processes:

            number = random.randint(30, 120)
            time = random.randint(0, 20)
            priority = random.randint(0,2)

            while number in self.numbers:
                number = random.randint(30, 120)

            while time in self.times:
                time = random.randint(0, 20)

            process[0].setText(str(number))
            process[2].setText('Not in CPU...')
            process[4].setText(str(time))
            process[5].setText(str(priority))

            self.times.append(time)
            self.numbers.append(number)

        # Conexiones con las teclas para el prompt de comandos.

        self.prompt.returnPressed.connect(self.get_command)

    def initialize_bars(self) -> None:
        for process in self.processes:
            process[3].setValue(0)

    """
    Este apartado es para los métodos encargados del primer frame de la interfaz gráfica, es decir, el frame que contiene,
    la información de los núcleos del procesador y las barras correspondientes.

    Uso QThreads en una clase implementada en 'includes/core_progress_bars_threads', que sirve para generar números aleatorios
    en un cierto rango para simular el uso de cada núcleo en el procesador.
    """

    # Este método se encarga de inicializar los threads y mantenerlos corriendo.

    def load_cpu_bars(self) -> None:

        # Este ciclo for funciona para inicializar todas las barras a cero.

        for progress_bar in self.cpu_process_bars:
            progress_bar.setValue(0)

        # Este segundo ciclo for toma de retorno en un for each, el lugar de la barra en la tupla y la barra.

        for index, progress_bar in enumerate(self.cpu_process_bars):
            thread = core_progress_bar_thread(index, progress_bar) # Luego les asigna un thread.
            thread.update_signal.connect(self.update_core_progress_bar) # Luego los conecta al método que actualiza el thread.
            core_threads.append(thread)
            thread.start()

    # Método repetitivo que actualiza el valor de las barras, este método es llamado desde el thread.

    def update_core_progress_bar(self, index: int, usage: int) -> None:
        self.cpu_process_bars[index].setValue(usage)

    """
    Este apartado es para los métodos encargados del segundo frame de la interfaz gráfica, es decir, el frame que contiene
    la información de cuantos procesos, hilos y tiempo lleva activo el sistema operativo.

    Uso QThreads en una clase implementada en 'includes/info_threads', que sirve para generar números aleatorios
    en un cierto rango para simular la cantidad de procesos y hilos que se usan actualmente en el sistema operativo.

    También obtiene el tiempo que el equipo lleva encendido y lo muestra, todo esto se hace en un solo thread.
    """

    # Este método se encarga de inicializar el thread.

    def load_information(self) -> None:

        # Creamos un solo hilo para mantener la información actualizada.

        info_thread = information_thread()

        # Conectamos todas las señales a sus labels correspondientes.

        info_thread.update_process_signal.connect(self.update_process_label)
        info_thread.update_threads_signal.connect(self.update_threads_label)
        info_thread.update_uptime_signal.connect(self.update_uptime_label)

        info_threads.append(info_thread) # Añadimos el thread a una lista para no perderlo.

        info_thread.start() # Corremos el thread.

    # Métodos conectados a las señales del thread de información del sistema.

    def update_process_label(self, text: str) -> None:
        self.processes_label.setText(text)

    def update_threads_label(self, text: str) -> None:
        self.threads_label.setText(text)

    def update_uptime_label(self, text: str) -> None:
        self.uptime_label.setText(text)

    """
    Este apartado es para los métodos encargados del tercer frame de la interfaz gráfica, es decir, el frame que contiene
    los procesos, sus estados y sus id's.

    Uso QThreads en una clase implementada en 'includes/process_threads', que sirve para tomar una tupla de todos los elementos
    de cada proceso (id, usuario, estado y progreso) y interactuar con el.

    Además implemento un terminal prompt donde podemos usar comandos para terminar, pausar y reanudar los procesos (kill, stop,
    start).
    """

    # Este método se encarga de inicializar los threads de procesos.

    def simulate_processes(self) -> None:

        for thread in threads:
            thread.terminate()

        for index, process in enumerate(self.processes):
            thread = process_thread(index, process) # Creamos el thread.
            thread.update_process_signal.connect(self.update_process_thread) # Conectamos el thread.
            threads.append(thread) # Añadimos el thread a una lista para no perder donde esta.

            thread.start() # Iniciamos el thread.

    # Método encargado de actualizar el estado del thread, segun los comandos o el progreso en la barra.

    def update_process_thread(self, index: int, state: str, value: int) -> None:
        threads[index].set_state(state)
        threads[index].set_value(value)

    # Este método se llama cuando queremos ejemplificar la planeacion first come first served.

    def simulate_processes_fcfs(self) -> None:

        for thread in threads:
            thread.terminate()

        # Ordenamos por el tiempo de llegada al proceso.

        self.processes = sorted(self.processes, key = lambda time: int(time[4].text()))

        # Creamos el hilo que se encarga de los procesos.

        thread = fcfs_thread(self.processes)
        thread.update_signal.connect(self.update_process_thread_fcfs)
        threads.append(thread)
        thread.start()

    # Método encargado de actualizar las barras.

    def update_process_thread_fcfs(self, index: int, value: int) -> None:
        self.processes[index][3].setValue(value)

    # Método encargado de hacer la planificacion por el método round robin.

    def simulate_processes_rr(self, quantum: int) -> None:
        for thread in threads:
            thread.terminate()

        for progress in self.processes:
            progress[3].setMaximum(random.randint(50, 101))
        
        # Creamos el hilo que se encarga de los procesos.

        thread = rr_thread(self.processes, quantum)
        thread.update_signal.connect(self.update_process_thread_rr)
        threads.append(thread)
        thread.start()
        
    # Método encargado de actualizar las barras.

    def update_process_thread_rr(self, index: int, value: int) -> None:
        self.processes[index][3].setValue(value)

    # Este método se llama cuando queremos ejemplificar la ejecucion de procesos por prioridad.

    def simulate_processes_priority(self) -> None:

        for thread in threads:
            thread.terminate()

        # Ordenamos por la prioridad y por el tiempo de llegada.

        self.processes = sorted(self.processes, key = lambda process: (int(process[5].text()), int(process[4].text())))

        # Creamos el hilo que se encarga de los procesos.

        thread = priority_thread(self.processes)
        thread.update_signal.connect(self.update_process_thread_priority)
        threads.append(thread)
        thread.start()
        
    def update_process_thread_priority(self, index: int, value: int) -> None:
        self.processes[index][3].setValue(value)

    # Este método se llama cuando queremos ejemplificar la planeacion usando colas multiples.

    def simulate_processes_queues(self) -> None:

        for thread in threads:
            thread.terminate()

        self.low_priority = []
        self.medium_priority = []
        self.high_priority = []

        # Ordenamos los procesos en colas:

        for process in self.processes:
            if process[5].text() == '0':
                self.high_priority.append(process)
            elif process[5].text() == '1':
                self.medium_priority.append(process)
            elif process[5].text() == '2':
                self.low_priority.append(process)

        self.low_priority = sorted(self.low_priority, key = lambda process: int(process[4].text()))
        self.medium_priority = sorted(self.medium_priority, key = lambda process: int(process[4].text()))
        self.high_priority = sorted(self.high_priority, key = lambda process: int(process[4].text()))

        # Creamos el hilo que se encarga de los procesos.

        thread = queue_thread(self.high_priority, self.medium_priority, self.low_priority)
        thread.update_signal.connect(self.update_process_queues)
        threads.append(thread)
        thread.start()
        
    def update_process_queues(self, index: int, value: int, priority: int) -> None:
        if priority == 0:
            self.high_priority[index][3].setValue(value)
        elif priority == 1:
            self.medium_priority[index][3].setValue(value)
        elif priority == 2:
            self.low_priority[index][3].setValue(value)

    # Este método se encarga de simular el problema del productor/consumidor.

    def simulate_pc(self) -> None:

        for thread in threads:
            thread.terminate()

        self.processes = sorted(self.processes, key = lambda time: int(time[4].text()))

        thread = pc_thread(self.processes)
        thread.update_signal.connect(self.update_process_thread_fcfs)
        threads.append(thread)
        thread.start()

    def simulate_rw(self) -> None:

        for thread in threads:
            thread.terminate()

        self.processes = sorted(self.processes, key = lambda time: int(time[4].text()))

        thread = rw_thread(self.processes)
        thread.update_signal.connect(self.update_process_thread_fcfs)
        threads.append(thread)
        thread.start()

    def simulate_real_memory(self) -> None:

        for thread in threads:
            thread.terminate()

        self.processes = sorted(self.processes, key = lambda time: int(time[4].text()))

        thread = real_memory_thread(self.processes)
        thread.update_signal.connect(self.update_process_thread_fcfs) 
        threads.append(thread)

        thread.start()

    """
    Este apartado es para el funcionamiento del prompt, donde ingresamos los comandos para interactuar con los procesos,
    por ende, es donde estan los métodos encargados de terminar, pausar y reanudar los threads.
    """

    # Método encargado de obtener el comando escrito por el usuario.

    def get_command(self) -> None:
        tokens = self.prompt.text().split() 

        integer_value = False

        if tokens[0] in ('normal', 'fcfs', 'rr', 'priority', 'queues', 'pc', 'rw', 'rmemory', 'restart', 'exit'):

            mode = tokens[0]

            if mode == 'normal':
                self.simulate_processes()
            elif mode == 'fcfs':
                self.simulate_processes_fcfs()
            elif mode == 'rr':
                self.simulate_processes_rr(int(tokens[1]))
            elif mode == 'priority':
                self.simulate_processes_priority()
            elif mode == 'queues':
                self.simulate_processes_queues()
            elif mode == 'pc':
                self.simulate_pc()
            elif mode == 'rw':
                self.simulate_rw()
            elif mode == 'rmemory':
                self.simulate_real_memory()
            elif mode == 'restart':
                restart_application()
            elif mode == 'exit':
                self.close()

            self.prompt.clear()
            return

        # Comprobamos que el comando sea válido.

        if len(tokens) != 2 and tokens[0].lower() in ('kill', 'stop', 'start', 'wait', 'resume'):
            self.prompt.clear()
            return
        
        command = tokens[0].lower()
        parameter = tokens[1].lower()
    
        try:
            id = int(parameter) # Casteamos el número de token a entero.
            integer_value = True
        except ValueError:
            if parameter == 'all':
                for thread in threads: # Pausamos o reanudamos los procesos.
                    if command == 'wait':
                        thread.set_state('Paused')
                        thread.pause()
                    elif command == 'resume' and thread.get_state() != 'Terminated':
                        thread.set_state('Initializing...')
                        thread.resume() 

        # Iteramos todos los threads en busca del token.

        for thread in threads: 
            if integer_value:
                if command == 'kill' and thread.get_id() == id:
                    thread.set_state('Terminated')
                    thread.terminate() # Finalizamos el thread.
                elif command == 'stop' and thread.get_id() == id:
                    thread.set_state('Paused')
                    thread.pause() # Pausamos el thread.
                elif command == 'start' and thread.get_id() == id:
                    thread.set_state('Running...')
                    thread.resume() # Reanudamos el thread.
                        
        self.prompt.clear() # Limpiamos la prompt de comandos.

    # Encargado de terminar los threads de Qt.

    def clear_threads(self) -> None:
        for thread in core_threads + info_threads + threads:
            thread.terminate()

# Método encargado de reiniciar la aplicacion para hacer pruebas.

def restart_application() -> None:
    app.quit()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main() -> None:

    global app 

    app = QApplication([])

    window = process_manager()

    # Cargamos todos los inicializadores de los threads.

    window.load_cpu_bars()
    window.load_information()

    # Obtenemos el tamaño de la pantalla.

    screen_geometry = app.desktop().availableGeometry()

    # Centramos la ventana.

    window.setGeometry((screen_geometry.width() - window.width()) // 2, (screen_geometry.height() - window.height()) // 2, window.width(), window.height())

    window.show()
    app.exec_()

    # Limpiamos los threads.

    window.clear_threads()

if __name__ == '__main__':
    main()