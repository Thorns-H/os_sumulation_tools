from PyQt5.QtCore import QThread, pyqtSignal

import time
import random
import math

threads = []
normal_threads = []

class virtual_memory_thread(QThread):

    update_signal = pyqtSignal(int, int)

    def __init__(self, processes: tuple, swap_frame: tuple) -> None:
        super().__init__()
        self.processes = processes
        self.swap_frame = swap_frame

    def run(self) -> None:

        memory_index = id(self)

        for index, process in enumerate(self.processes):

            state, progress_bar, memory_location = process[2], process[3], process[6]

            state.setText('Allocating...')
            state.setStyleSheet('color: lime;')

            random_kb = random.randint(1000, 16000)
            process_size = random_kb * 1024
            blocks = math.ceil(process_size / 8)

            memory_location.setText(f'{hex(memory_index + process_size)} [{random_kb}kb - {blocks}]')
            memory_location.setStyleSheet('color: lime;')

            for i in range (1, 101):
                self.update_signal.emit(index, i)
                time.sleep(0.009)

            state.setText('Releasing...')
            progress_bar.setStyleSheet('QProgressBar::chunk {background: #B1351F;}')
            state.setStyleSheet('color: red;')

            for i in range (101, -1, -1):
                self.update_signal.emit(index, i)
                time.sleep(0.009)

            state.setText('Not in CPU...')
            state.setStyleSheet('color: white;')

            memory_location.setText('0x000000000000 [0]')
            memory_location.setStyleSheet('color: red;')

            memory_index = memory_index + blocks