import asyncio
from augmentoolkit.generation_functions.engine_wrapper_class import EngineWrapper
import os
import inspect


def setup_semaphore_and_engines(
    concurrency_limit: int,
    small_model: str,
    small_api_key: str,
    small_base_url: str,
    small_mode: str,
    large_model: str,
    large_api_key: str,
    large_base_url: str,
    large_mode: str,
    engine_input_observers=[],
    engine_output_observers=[],
    large_engine_input_observers=[],
    large_engine_output_observers=[],
):
    semaphore = asyncio.Semaphore(concurrency_limit)

    async def run_task_with_limit(task, timeout=60):
        async with semaphore:
            try:
                return await asyncio.wait_for(task, timeout=timeout)
            except asyncio.TimeoutError:
                print("[Timeout] A task exceeded the timeout limit.")
                return None
            except Exception as e:
                print(f"[Error] Exception in task: {e}")
                return None

    engine_wrapper = EngineWrapper(
        model=small_model,
        api_key=small_api_key,
        base_url=small_base_url,
        mode=small_mode,
        input_observers=engine_input_observers,
        output_observers=engine_output_observers,
    )

    engine_wrapper_large = EngineWrapper(
        model=large_model,
        api_key=large_api_key,
        base_url=large_base_url,
        mode=large_mode,
        input_observers=large_engine_input_observers,
        output_observers=large_engine_output_observers,
    )

    return run_task_with_limit, engine_wrapper, engine_wrapper_large, semaphore


def make_relative_to_self(path):
    """Make paths relative to the calling script's location"""
    # Get the caller's frame info
    caller_frame = inspect.stack()[1]
    caller_filepath = caller_frame.filename

    # Get directory of the script that called this function
    caller_dir = os.path.dirname(os.path.abspath(caller_filepath))

    return os.path.join(caller_dir, path)
