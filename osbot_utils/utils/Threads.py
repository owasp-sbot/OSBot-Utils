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

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, TypeVar, Tuple, Optional, Dict

T = TypeVar('T')  # Type of items in the list
R = TypeVar('R')  # Return type of the function

def execute_in_thread_pool(target_function   : Callable                     ,
                           calls             : List[Tuple[Tuple, Dict]]     ,  # List of (args, kwargs) pairs
                           max_workers       : Optional[int] = None         ,
                           return_exceptions : bool          = False        ):
    """Execute a function for each item in parallel using ThreadPoolExecutor."""

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = []
        for args, kwargs in calls:
            future = executor.submit(target_function, *args, **kwargs)
            futures.append(future)                                              # Submit all tasks to the executor

        for future in futures:                                                  # Wait for all to complete and collect results
            try:
                results.append(future.result())
            except Exception as e:
                if return_exceptions:
                    results.append(e)
                else:
                    raise
    return results

# in the use cases when I tried to use this, it hanged
# def invoke_in_current_loop(target: typing.Coroutine):
#     try:
#         current_loop = asyncio.get_running_loop()   # Get the current running loop, if any
#     except RuntimeError:                            # There is no running event loop
#         current_loop = None
#
#     if current_loop and current_loop.is_running():  # If there's an event loop currently running, we can use asyncio.run_coroutine_threadsafe to run it
#         future = asyncio.run_coroutine_threadsafe(target, current_loop)
#         return future.result()
#     else:
#         return asyncio.run(target)                  # If there's no event loop running, we create a new one and use run_until_complete

async_invoke_in_new_loop = invoke_in_new_event_loop
invoke_async             = invoke_async_function                    # todo: see if this is best use of this function name