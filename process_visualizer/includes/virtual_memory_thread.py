from PyQt5.QtCore import QThread, pyqtSignal

import time
import random
import math

threads = []
normal_threads = []

class virtual_memory_thread(QThread):

    update_signal = pyqtSignal(int, int)
    update_memory = pyqtSignal(int)
    update_vmemory = pyqtSignal(int)

    def __init__(self, processes: tuple, memory_frame: tuple, swap_frame: tuple) -> None:
        super().__init__()
        self.processes = processes
        self.total_memory = memory_frame[1]
        self.total_blocks = memory_frame[2]
        self.total_size = memory_frame[3]

        self.total_vmemory = swap_frame[1]
        self.total_pages = swap_frame[2]
        self.total_vsize = swap_frame[3]

    def run(self) -> None:

        memory_index = id(self)

        for index, process in enumerate(self.processes):

            state, progress_bar, memory_location = process[2], process[3], process[6]

            state.setText('Allocating...')
            state.setStyleSheet('color: lime;')

            random_gb = random.randint(8, 11)
            diff = random_gb - 7
            blocks = math.ceil(7168 / 8)

            process_size = diff * 1024
            pages = math.ceil(process_size / 4)

            percentage = (7 / 8) * 100
            percentage = math.ceil(percentage)

            vpercentage = (diff / 4) * 100
            vpercentage = math.ceil(vpercentage)

            memory_location.setText(f'{hex(memory_index + random_gb)}')
            memory_location.setStyleSheet('color: lime;')

            for i in range (1, 101):
                self.update_signal.emit(index, i)
                time.sleep(0.009)

            for i in range(1, percentage + 1):
                self.update_memory.emit(i)
                time.sleep(0.002)

            self.total_memory.setText(f'Total Space: 1GB')
            self.total_blocks.setText(f'Blocks (8MB c/u): {blocks}')
            self.total_size.setText(f'Process Size: {random_gb}GB')

            for i in range(1, vpercentage + 1):
                self.update_vmemory.emit(i)
                time.sleep(0.002)

            self.total_vmemory.setText(f'Total Space: {4 - diff}GB')
            self.total_pages.setText(f'Pages (4MB c/u): {pages}')
            self.total_vsize.setText(f'Usage: {diff}GB')

            state.setText('Releasing...')
            progress_bar.setStyleSheet('QProgressBar::chunk {background: #B1351F;}')
            state.setStyleSheet('color: red;')

            for i in range (101, -1, -1):
                self.update_signal.emit(index, i)
                time.sleep(0.009)

            state.setText('Not in CPU...')
            state.setStyleSheet('color: white;')

            self.total_memory.setText(f'Total Space: 8GB')
            self.total_blocks.setText(f'Blocks (8MB c/u): 0')
            self.total_size.setText(f'Process Size: 0GB')
            self.update_memory.emit(0)

            self.total_vmemory.setText(f'Total Space: 4GB')
            self.total_pages.setText(f'Pages (4MB c/u): 0')
            self.total_vsize.setText(f'Usage: 0GB')
            self.update_vmemory.emit(0)

            memory_location.setText('0x000000000000')
            memory_location.setStyleSheet('color: red;')

            memory_index = memory_index + blocks