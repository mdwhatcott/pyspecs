PYSPECS_PREFIX = '_pyspecs_'
PYSPECS_STEP = PYSPECS_PREFIX + 'step'
PYSPECS_SKIPPED = PYSPECS_PREFIX + 'skipped'
SPEC = 'spec'
GIVEN_STEP = 'given'
WHEN_STEP = 'when'
COLLECT_STEP = 'collect'
THEN_STEP = 'then'
AFTER_STEP = 'after'
ALL_STEPS = [
    GIVEN_STEP,
    WHEN_STEP,
    COLLECT_STEP,
    THEN_STEP,
    AFTER_STEP,
]
SKIPPED_STEP = 'skipped'
SKIPPED_SPEC = '(skipped spec)'


def _step(name):
    def decorator(object):
        setattr(object, PYSPECS_STEP, name)
        return object
    return decorator


def _skip(obj):
    setattr(obj, PYSPECS_SKIPPED, True)
    return obj

