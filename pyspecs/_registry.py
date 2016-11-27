class Registry(object):
    def __init__(self):
        self._current_step = None
        self.root_steps = []

    def push(self, step):
        previous = self._current_step
        self._current_step = step

        if previous is None:
            self.root_steps.append(step)
        else:
            previous.steps.append(step)
        return previous

    def pop(self):
        self._current_step = self._current_step.parent \
            if self._current_step else None
