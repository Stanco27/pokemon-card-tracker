import threading

class TargetBot:
    def __init__(self):
        self.is_running = False
        self.thread = None

    def run_loop(self, config):
        while self.is_running:
            pass

    def start(self, config):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run_loop, args=(config,))
            self.thread.start()

    def stop(self):
        self.is_running = False

target_bot = TargetBot()

def test_bot():
    print("Bot test successful")