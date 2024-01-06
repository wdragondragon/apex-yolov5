class Counter:
    def __init__(self):
        self.count = 0

    def increase(self):
        self.count += 1
        return self.get_count()

    def reset(self):
        self.count = 0

    def get_count(self):
        return self.count


no_lock_counter = Counter()


def sure_no_aim(num):
    return no_lock_counter.increase() >= num


def reset_counter():
    no_lock_counter.reset()
