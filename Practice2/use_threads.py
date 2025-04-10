import threading
import time

class UseThreads:
    def __init__(self):
        self.saving_thread = None
        self.stop_thread = False

    def start_saving_thread(self, username, users):
        self.stop_thread = False
        self.saving_thread = threading.Thread(target=self.save_notes, args=(username, users), daemon=True)
        self.saving_thread.start()

    def stop_saving_thread(self):
        self.stop_thread = True
        if self.saving_thread:
            self.saving_thread.join()

    def save_notes(self, username, users):
        last_notes = None
        while not self.stop_thread:
            time.sleep(5)
            notes = users.get_notes(username)

            if notes != last_notes:
                print(f"\n(Автосохранение)")
                users._save_data(users._load_data())
                last_notes = notes.copy()