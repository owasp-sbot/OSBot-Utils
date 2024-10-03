import asyncio
import logging
import typing

def invoke_async_function(target: typing.Coroutine):
    """Run an asynchronous coroutine in a new event loop."""
    logger         = logging.getLogger('asyncio')
    level_original = logger.level
    logger.level   = logging.INFO  # this will suppress the asyncio debug messages which where showing in tests
    try:
        original_loop = asyncio.get_event_loop()
    except RuntimeError:
        original_loop = None  # No event loop was set

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(target)
    finally:
        loop.close()
        # Restore the original event loop
        if original_loop is not None:
            asyncio.set_event_loop(original_loop)
        else:
            asyncio.set_event_loop(None)

        logger.level = level_original  # restore the original log level


def invoke_in_new_event_loop(target: typing.Coroutine):
    def run_in_new_loop():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(target)
        finally:
            new_loop.close()

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as pool:
        future = pool.submit(run_in_new_loop)
        result = future.result()
        return result