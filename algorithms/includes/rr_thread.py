from PyQt5.QtCore import QThread, pyqtSignal

import time

threads = []

class rr_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int)

    # Constructor de la clase.

    def __init__(self, processes: tuple, quantum: int) -> None:
        super().__init__()
        self.processes = processes
        self.last = [0]
        self.quantum = quantum

    def rr(self) -> None:

        for index in range(len(self.processes)):

            state = self.processes[index][2]

            for i in range(self.last[0] + 1, self.last[0] + self.quantum + 1):

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

        self.last[0] += self.quantum

    def run(self) -> None:
        while self.last[0] < 100:
            if self.last[0] >= 90:
                self.quantum = 100 - self.last[0]
                self.rr()
            else:
                self.rr()