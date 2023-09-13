"""
Este código proporciona la documentación a la actividad, hecha en Python usando Qt5,
como utilizamos QtDesigner, el archivo .ui estará docuentado en el vídeo adjunto a 
esta actividad.
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic

import time
import random

random_times = (0.009, 0.011, 0.02, 0.005)

# Definición de la clase que actua como nuestro thread personalizado para las barras.

class progress_bar_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int)

    # Constructor de la clase.

    def __init__(self, index: int, process: QProgressBar) -> None:
        super().__init__()
        self.index = index
        self.process = process

    # Método que se encarga de actualizar la barra relacionada al thread.

    def run(self) -> None:

        if self.process.text() != '':
            for i in range(1, 101):
                self.update_signal.emit(self.index, i)
                time.sleep(random.choice(random_times))

# Definición de la clase que actua como handler de nuestra ventana de gráficos de Qt5. 

class multiprocessing_simulator(QMainWindow):

    # Constructor de la clase.

    def __init__(self) -> None:
        super(multiprocessing_simulator, self).__init__()
        uic.loadUi('graphics/window.ui', self) # Cargamos la interfaz hecha en QtDesigner.
        self.setWindowTitle('Processing Simulator')

        # Por cada QLineEdit, ordenamos los tabs para movernos más rápidamente.

        self.setTabOrder(self.A, self.B)
        self.setTabOrder(self.B, self.C)
        self.setTabOrder(self.C, self.D)
        self.setTabOrder(self.D, self.E)
        self.setTabOrder(self.E, self.F)
        self.setTabOrder(self.F, self.batch_button)

        # Creamos tuplas con los objetos que vamos a necesitar, separando dos lotes de procesos
        # y sus respectivas barras.

        self.first_batch = (self.A, self.B, self.C)
        self.second_batch = (self.D, self.E, self.F)
        self.first_batch_bars = (self.first_bar, self.second_bar, self.third_bar)
        self.second_batch_bars = (self.fourth_bar, self.fifth_bar, self.sixth_bar)

        # Vinculamos los botones con los métodos de procesamiento correspondientes.

        self.batch_button.clicked.connect(self.batch_processing)
        self.multi_processing_button.clicked.connect(self.multiprocessing)

    # Función handler de procesamiento de lotes.

    def batch_processing(self) -> None:

        # Limpiamos los procesos anteriores.

        for progress_bar in self.first_batch_bars + self.second_batch_bars:
            progress_bar.setValue(0)

        # Iteramos por cada proceso en los lotes, comprobamos si existen y simulamos la barra del proceso correspondiente.

        for index, process in enumerate(self.first_batch):
            if process.text() != '':
                for i in range(1, 101):
                    self.first_batch_bars[index].setValue(i)
                    time.sleep(random.choice(random_times))

        for index, process in enumerate(self.second_batch):
            if process.text() != '':
                for i in range(1, 101):
                    self.second_batch_bars[index].setValue(i)
                    time.sleep(random.choice(random_times))

    # Función handler de multiprocesamiento.

    def multiprocessing(self) -> None:

        # Limpiamos los procesos anteriores.

        for progress_bar in self.first_batch_bars + self.second_batch_bars:
            progress_bar.setValue(0)

        # Creamos la lista que almacena las referencias de nuestros hilos.

        self.threads = []

        # Creamos un thread por cada barra en la lista y lo pasamos al método que actualiza la señal de estas.

        for index, process in enumerate(self.first_batch + self.second_batch):
            thread = progress_bar_thread(index, process)
            thread.update_signal.connect(self.update_progress)
            self.threads.append(thread)
            thread.start()

    # Método encargado de actualizar el valor en la barra.

    def update_progress(self, index: int, value: int) -> None:
        bars = self.first_batch_bars + self.second_batch_bars
        bars[index].setValue(value)

# Función principal del programa.

def main() -> None:
    app = QApplication([])
    window = multiprocessing_simulator()
    screen_geometry = app.desktop().availableGeometry()
    window.setGeometry((screen_geometry.width() - window.width()) // 2, (screen_geometry.height() - window.height()) // 2, window.width(), window.height())
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()