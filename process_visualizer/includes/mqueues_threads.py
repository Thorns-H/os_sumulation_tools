from PyQt5.QtCore import QThread, pyqtSignal

import time
import random

threads = []

class InvalidTypeException(Exception):
    def __init__(self, invalid_type):
        self.message = f"Invalid type: {invalid_type}. Type must be one of 'fcfs', 'rr', or 'srt'."
        super().__init__(self.message)

class mqueue_thread(QThread):

    # Constructor de la clase.

    def __init__(self, processes: tuple, type: str) -> None:
        super().__init__()
        self.processes = processes
        self.last = [0]
        self.times = {}

        if type not in ('fcfs', 'rr', 'srt'):
            raise InvalidTypeException(type)
    
        self.type = type

    def fcfs_type(self) -> None:

        self.processes = sorted(self.processes, key = lambda time: int(time[4].text()))

        for process in self.processes:
            process[3].setStyleSheet("QProgressBar { background: transparent; border: 2px solid #FF5733; } QProgressBar::chunk { background: #FF5733; }")

        for index, process in enumerate(self.processes):

            state = process[2]
            progress_bar = process[3]

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

                progress_bar.setValue(i)
                time.sleep(0.009)

    def rr_type(self) -> None:

        for process in self.processes:
            process[3].setStyleSheet("QProgressBar { background: transparent; border: 2px solid #33FF57; } QProgressBar::chunk { background: #33FF57; }")

        while self.last[0] < 100:
            if self.last[0] >= 90:
                self.quantum = 100 - self.last[0]
                self.rr()
            else:
                self.rr()

    def rr(self) -> None:

        for index in range(len(self.processes)):

            state = self.processes[index][2]
            progress_bar = self.processes[index][3]

            for i in range(self.last[0] + 1, self.last[0] + 30 + 1):

                if 1 <= i < 20:
                    state.setText('Initializing...')
                    state.setStyleSheet('color: orange;')
                elif 20 <= i < 30:
                    state.setText('Ready!')
                    state.setStyleSheet('color: yellow;')
                elif progress_bar.value() == progress_bar.maximum():
                    state.setText('Finished')
                    state.setStyleSheet('color: red;')
                else:
                    state.setText('Running...')
                    state.setStyleSheet('color: lime;')

                progress_bar.setValue(i)
                time.sleep(0.009)

        self.last[0] += 30

    def init_srt_type(self) -> None:
        
        for process in self.processes:
            process[3].setStyleSheet("QProgressBar { background: transparent; border: 2px solid #5733FF; } QProgressBar::chunk { background: #5733FF; }")
        
        self.processes = sorted(self.processes, key = lambda x: int(x[4].text()))

        for index, process in enumerate(self.processes):

            state = process[2]
            progress_bar = process[3]
            progress = random.randint(10, 16)

            state.setText('Using STR...')
            time.sleep(1)

            for i in range (1, progress):

                if 1 <= i < 20:
                    state.setText('Initializing...')
                    state.setStyleSheet('color: orange;')

                progress_bar.setValue(i)
                time.sleep(0.009)

            self.times[progress_bar] = 101 - progress

        self.srt_type()

    def srt_type(self) -> None:
        time.sleep(2)

        self.processes = sorted(self.processes, key = lambda x: int(x[5].text()))

        for index, process in enumerate(self.processes):

            state = process[2]
            progress_bar = process[3]

            for i in range(100 - self.times.get(progress_bar), 101):

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

                progress_bar.setValue(i)
                time.sleep(0.009)

    def run(self) -> None:
        if self.type == 'fcfs':
            self.fcfs_type()
        elif self.type == 'rr':
            for progress in self.processes:
                progress[3].setMaximum(random.randint(65, 101))
            self.rr_type()
        elif self.type == 'srt':
            self.init_srt_type()
