import threading

class Cipher:
    def encrypt(self, text, shift, result_queue):
        def encrypt_task():
            encr_text = ""
            for char in text:
                if char.isalpha():
                    shift_amount = shift % 26
                    if char.islower():
                        encr_text += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
                    else:
                        encr_text += chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
                else:
                    encr_text += char

            result_queue.put(encr_text)

        threading.Thread(target=encrypt_task, daemon=True).start()