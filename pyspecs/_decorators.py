import logging
log = logging.getLogger(__name__)


def wait_keyboard_interrupt(method):
    def inner(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except KeyboardInterrupt:
            log.debug('keyboard interruption')
            pass
    return inner
