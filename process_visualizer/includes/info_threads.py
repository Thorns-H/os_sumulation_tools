from PyQt5.QtCore import QThread, pyqtSignal

import random
import time
import psutil

info_threads = []

class information_thread(QThread):

    update_process_signal = pyqtSignal(str)
    update_threads_signal = pyqtSignal(str)
    update_uptime_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:

            uptime_seconds = int(time.time() - psutil.boot_time())
            uptime_minutes = uptime_seconds // 60
            uptime_hours = uptime_minutes // 60

            process_text = f"Processes: {random.randint(130, 145)}."
            threads_text = f"Threads: {random.randint(500, 600)}."
            uptime_text = f"Uptime: {uptime_hours}h {uptime_minutes % 60}m."

            self.update_process_signal.emit(process_text)
            self.update_threads_signal.emit(threads_text)
            self.update_uptime_signal.emit(uptime_text)

            self.sleep(5)
