import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# === Configuration ===
delay = 0.1                      # Seconds between each click (adjust as needed)
button = Button.left             # Mouse button to click
start_stop_key = KeyCode(char='a')  # Press 'a' to start/stop clicking
exit_key = KeyCode(char='b')         # Press 'b' to exit the program


# === AutoClicker Class ===
class AutoClicker(threading.Thread):
    def __init__(self, delay, button):
        super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_active = True
        self.mouse = Controller()

    def start_clicking(self):
        self.running = True
        print("[INFO] Auto-clicking started.")

    def stop_clicking(self):
        self.running = False
        print("[INFO] Auto-clicking stopped.")

    def exit(self):
        self.stop_clicking()
        self.program_active = False
        print("[INFO] Exiting program...")

    def run(self):
        print("[INFO] AutoClicker thread running.")
        while self.program_active:
            if self.running:
                print("[DEBUG] Click.")
                self.mouse.click(self.button)
                time.sleep(self.delay)
            else:
                time.sleep(0.1)


# === Hotkey Event Handling ===
def on_press(key):
    print(f"[KEY] Pressed: {key}")
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        return False  # Stop the listener


# === Start AutoClicker Thread ===
click_thread = AutoClicker(delay, button)
click_thread.start()

# === Start Keyboard Listener ===
print("[INFO] Press 'a' to start/stop clicking. Press 'b' to exit.")
with Listener(on_press=on_press) as listener:
    listener.join()

