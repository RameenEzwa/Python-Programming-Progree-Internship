# Task 2 - Core Algorithmic Fibonacci Generation Module

## Internship
Progree Internship

## Objective
Build a Python module that calculates exact Fibonacci sequence values
under varying parameter limits.

## Requirements Covered
- Clean Python function for integer sequence bounds
- Negative-input parameter sanitization
- Structured list output
- Exact Fibonacci values
- Runtime benchmarking with the `timeit` framework
- Functional and invalid-input testing

## How to Run

1. Make sure Python 3 is installed.
2. Open a terminal in this folder.
3. Run:

```bash
python fibonacci_module.py
```

## Function Usage

```python
from fibonacci_module import generate_fibonacci

print(generate_fibonacci(0, 10))
```

Expected sequence:

```text
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

## Validation
The module rejects:
- Negative bounds
- Non-integer bounds
- A start bound greater than the end bound

## Benchmarking
The program uses `timeit.timeit()` and reports the average execution
time for 1,000 repetitions at several sequence limits.
