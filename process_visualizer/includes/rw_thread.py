from PyQt5.QtCore import QThread, pyqtSignal
import threading
import random

import time

threads = []
normal_threads = []

class rw_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int)

    # Constructor de la clase.

    def __init__(self, processes: tuple) -> None:
        super().__init__()
        self.processes = processes
        self.read_times = [random.randint(25, 33), random.randint(55, 66), 101]

    def target_reader(self, process) -> None:
        state = process[2]
        progress_bar = process[3]
        
        for process in self.processes:
            if process[2].text() not in ['Reading...', 'Writting...', 'Readable']:
                process[2].setText('Reading...')
                process[2].setStyleSheet('color: yellow;')

        progress_bar.setStyleSheet('QProgressBar::chunk {background: #FFD966;}')
        state.setStyleSheet('color: yellow;')

        time.sleep(2)

        state.setText('Writting...')
        state.setStyleSheet('color: lime;')

        for process in self.processes:
            if process[2].text() not in ['Writting...', 'Readable']:
                process[2].setText('Waiting...')
                process[2].setStyleSheet('color: white;')

    def run(self) -> None:

        for process in self.processes:
            process[2].setText('Waiting...')

        for index, process in enumerate(self.processes):

            state = process[2]
            progress_bar = process[3]

            state.setText('Writting...')
            state.setStyleSheet('color: lime;')

            for i in range (1, 101):
                if i in self.read_times:
                    state.setText('Saving...')
                    state.setStyleSheet('color: lime;')
                    time.sleep(0.5)

                    normal_thread = threading.Thread(target = self.target_reader, args = (process,))
                    normal_threads.append(normal_thread)
                    normal_thread.start()
                    normal_thread.join()

                    progress_bar.setStyleSheet('QProgressBar::chunk {background: #3D85C6;}')

                self.update_signal.emit(index, i)
                time.sleep(0.009)

            state.setText('Readable')
            state.setStyleSheet('color: red;')
            progress_bar.setStyleSheet('QProgressBar::chunk {background: #B1351F;}')
            