from PyQt5.QtCore import QThread, pyqtSignal

import time

threads = []

class queue_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int, int)

    # Constructor de la clase.

    def __init__(self, high: tuple, medium: tuple, low: tuple) -> None:
        super().__init__()
        self.high_priority = high
        self.medium_priority = medium
        self.low_priority = low

    # Método encargado de llevar la actualizacion de las colas.

    def progress_bar_for(self, queue: tuple) -> None:

        for index, process in enumerate(queue):

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

                self.update_signal.emit(index, i, int(process[5].text()))
                time.sleep(0.009)

    # Método encargado de arrancar el hilo.

    def run(self) -> None:

        for process in self.high_priority:
            process[2].setText(f'High Queue...')
            process[2].setStyleSheet('color: yellow;')
            time.sleep(0.5)

        self.progress_bar_for(self.high_priority)

        for process in self.medium_priority:
            process[2].setText(f'Medium Queue...')
            process[2].setStyleSheet('color: yellow;')
            time.sleep(0.5)

        self.progress_bar_for(self.medium_priority)

        for process in self.low_priority:
            process[2].setText(f'Low Queue...')
            process[2].setStyleSheet('color: yellow;')
            time.sleep(0.5)

        self.progress_bar_for(self.low_priority)
