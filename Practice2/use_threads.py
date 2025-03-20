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
        last_notes_count = 0
        while not self.stop_thread:
            time.sleep(5)  
            notes = users.get_notes(username)
            current_notes_count = len(notes)
            
            if current_notes_count != last_notes_count:
                print(f"\n(Автосохранение)")
                last_notes_count = current_notes_count