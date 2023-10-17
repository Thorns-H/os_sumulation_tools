from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
import random

core_threads = []

class core_progress_bar_thread(QThread):

    # Creamos una señal que conecte al objeto QProgressBar relacionado al Thread.

    update_signal = pyqtSignal(int, int)

    # Constructor de la clase.

    def __init__(self, index: int, process: QProgressBar) -> None:
        super().__init__()
        self.index = index
        self.process = process

    def run(self) -> None:
        while True:
            random_usage = random.randint(12, 43)
            self.update_signal.emit(self.index, random_usage)
            self.sleep(1)
    