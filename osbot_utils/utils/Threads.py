import asyncio
import logging
import typing
from concurrent.futures import ThreadPoolExecutor

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


def invoke_in_new_event_loop(target: typing.Coroutine):             # Runs a coroutine in a new event loop in a separate thread and returns the result
    def run_in_new_loop():                                          # Function to run the coroutine in a new event loop
        new_loop = asyncio.new_event_loop()                         # Create a new event loop
        asyncio.set_event_loop(new_loop)                            # Set the new event loop as the current event loop
        try:
            return new_loop.run_until_complete(target)              # Run the coroutine in the new event loop
        finally:
            new_loop.close()                                        # Close the event loop to free resources

    with ThreadPoolExecutor() as pool:                              # Create a thread pool executor
        future = pool.submit(run_in_new_loop)                       # Submit the function to run in the thread pool
        result = future.result()                                    # Wait for the result of the future
        return result                                               # Return the result from the coroutine

async_invoke_in_new_loop = invoke_in_new_event_loop