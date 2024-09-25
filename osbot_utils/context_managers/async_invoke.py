import logging
from contextlib import contextmanager
import asyncio

@contextmanager
def async_invoke():
    logger         = logging.getLogger('asyncio')
    level_original = logger.level
    logger.level   = logging.INFO                          # this will suppress the asyncio debug messages which where showing in tests
    try:
        original_loop = asyncio.get_event_loop()
    except RuntimeError:
        original_loop = None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        yield loop.run_until_complete
    finally:
        loop.close()
        if original_loop is not None:
            asyncio.set_event_loop(original_loop)
        else:
            asyncio.set_event_loop(None)

        logger.level = level_original                           # restore the original log level