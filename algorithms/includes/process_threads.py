from PyQt5.QtCore import QThread, pyqtSignal

import random
import time

threads = []

class process_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_process_signal = pyqtSignal(int, str, int)

    pause_signal = pyqtSignal()
    resume_signal = pyqtSignal()

    # Constructor de la clase.

    def __init__(self, index: int, process: tuple) -> None:
        super().__init__()
        self.index = index
        self.id = process[0]
        self.user = process[1]
        self.state = process[2]
        self.progress_bar = process[3]
        self.process_time = process[4]

        self.paused = False

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    # Getters para verificaciones con los comandos.

    def get_id(self) -> int:
        return int(self.id.text())
    
    def get_state(self) -> str:
        return self.state.text()
    
    # Setter para el estado del proceso con el comando.
    
    def set_state(self, text: str) -> None:
        if text == 'Initializing...':
            self.state.setStyleSheet('color: orange;')
        elif text == 'Ready!':
            self.state.setStyleSheet('color: yellow;')
        elif text == 'Running...' or text == 'Paused':
            self.state.setStyleSheet('color: lime;')
        elif text == 'Finished' or text == 'Terminated':
            self.state.setStyleSheet('color: red;')

        self.state.setText(text)

    def set_value(self, value: int) -> None:
        self.progress_bar.setValue(value)

    def run(self) -> None:
        for i in range(1, 101):
            if self.paused:
                while self.paused:
                    time.sleep(0.1) 

            if 1 <= i < 20:
                state = 'Initializing...'
            elif 20 <= i < 30:
                state = 'Ready!'
            elif i == 100:
                state = 'Finished'
            else:
                state = 'Running...'

            self.update_process_signal.emit(self.index, state, i)
            time.sleep(random.uniform(0.0, 0.5))