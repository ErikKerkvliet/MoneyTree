class ThreadManager:

    def __init__(self, glv):
        self.glv = glv
        self.threads = []

    def add(self, thread):
        print(f'Starting new {type(thread).__name__}')
        thread.start()

        self.threads.append(thread)
