from PyQt5.QtCore import QThread, pyqtSignal
import threading

import time

threads = []
normal_threads = []

class pc_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int)

    # Constructor de la clase.

    def __init__(self, processes: tuple) -> None:
        super().__init__()
        self.processes = processes

    def run(self) -> None:
        for index, process in enumerate(self.processes):

            state, progress_bar = process[2], process[3]

            state.setText('Producing...')
            state.setStyleSheet('color: lime;')

            for i in range (1, 101):
                self.update_signal.emit(index, i)
                time.sleep(0.009)

            state.setText('Consuming...')
            progress_bar.setStyleSheet('QProgressBar::chunk {background: #B1351F;}')
            state.setStyleSheet('color: red;')

            for i in range (101, -1, -1):
                self.update_signal.emit(index, i)
                time.sleep(0.009)

            state.setText('Not in CPU...')
            state.setStyleSheet('color: white;')