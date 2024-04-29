"""
tools.py

Utility module providing decorators for performance measurement and other common tools 
used throughout the codebase. The module aims to enhance debugging and performance optimization 
by allowing easy integration of time measurement across functions.

Available Decorators:
- `duration`: Measures the execution time of any callable (function or method) and prints it.

Usage:
------
This module is intended to be imported and its decorators applied to various functions
throughout a project where performance measurement is necessary.

Example:
--------
from tools import duration

@duration
def example_function():
    import time
    time.sleep(2)  # Simulates a delay
    return "Function has completed."

When executed, this decorates `example_function()` such that its execution time is automatically
measured and printed to stdout, along with returning its original result.

Dependencies:
-------------
- Python 3.10+ due to the use of type hints and other modern Python features.

Authors:
- Your Name <your.email@example.com>

License:
- MIT License
"""

import time

def duration(func):
    """
    Decorator that measures the execution time of a function.

    This decorator wraps any callable, and when the callable is executed,
    it measures the time taken from start to finish and prints out the duration
    in seconds.

    Parameters:
    - func (callable): The function to measure. This can be any function or method
                       that is callable.

    Returns:
    - callable: A wrapper function that adds timing logic to the original function.

    Example:
    --------
    @duration
    def my_function():
        time.sleep(2)
        return "Completed"

    Running `my_function()` will output:
    `my_function took 2.0023 seconds to execute.` and returns "Completed"
    """
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds to execute.")
        return result

    return wrapper
