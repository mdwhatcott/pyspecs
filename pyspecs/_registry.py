class Registry(object):
    _instance = None
    _current_step = None
    root_steps = []
    total_steps = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registry, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def reset(self):
        self._current_step = None
        self.root_steps = []
        self.total_steps = 0
        return self

    def push(self, step):
        self.total_steps += 1
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
