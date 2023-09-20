from PyQt5.QtCore import QThread, pyqtSignal

import time

threads = []

class fcfs_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int)

    # Constructor de la clase.

    def __init__(self, processes: tuple) -> None:
        super().__init__()
        self.processes = processes

    def run(self) -> None:
        for index, process in enumerate(self.processes):

            state = process[2]

            for i in range (1, 101):

                if 1 <= i < 20:
                    state.setText('Initializing...')
                    state.setStyleSheet('color: orange;')
                elif 20 <= i < 30:
                    state.setText('Ready!')
                    state.setStyleSheet('color: yellow;')
                elif i == 100:
                    state.setText('Finished')
                    state.setStyleSheet('color: red;')
                else:
                    state.setText('Running...')
                    state.setStyleSheet('color: lime;')

                self.update_signal.emit(index, i)
                time.sleep(0.009)