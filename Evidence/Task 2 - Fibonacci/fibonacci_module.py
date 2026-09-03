"""
Task 2: Core Algorithmic Fibonacci Generation Module
Progree Internship

This module generates exact Fibonacci sequence values for integer
index bounds and benchmarks execution time using timeit.
"""

import timeit


def generate_fibonacci(start, end):
    """
    Return Fibonacci values from index 'start' through index 'end'.

    Fibonacci indexing:
        F(0) = 0
        F(1) = 1

    Example:
        generate_fibonacci(0, 5)
        -> [0, 1, 1, 2, 3, 5]
    """

    # Parameter sanitization
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("Start bound must be an integer.")

    if not isinstance(end, int) or isinstance(end, bool):
        raise TypeError("End bound must be an integer.")

    if start < 0 or end < 0:
        raise ValueError("Sequence bounds cannot be negative.")

    if start > end:
        raise ValueError("Start bound cannot be greater than end bound.")

    # Build the sequence only up to the requested end index.
    fibonacci = [0, 1]

    if end == 0:
        return [0]

    for index in range(2, end + 1):
        fibonacci.append(fibonacci[index - 1] + fibonacci[index - 2])

    # Return a structured list containing the requested values.
    return fibonacci[start:end + 1]


def benchmark_fibonacci(start, end, repetitions=1000):
    """
    Measure average execution time for generate_fibonacci()
    using Python's timeit framework.
    """

    # Validate parameters before benchmarking.
    generate_fibonacci(start, end)

    total_time = timeit.timeit(
        lambda: generate_fibonacci(start, end),
        number=repetitions
    )

    return total_time / repetitions


def run_tests():
    """Run functional and validation tests."""

    print("\n--- Functional Tests ---")

    test_cases = [
        (0, 10),
        (5, 15),
        (10, 20),
    ]

    for start, end in test_cases:
        result = generate_fibonacci(start, end)
        print(f"Range {start}-{end}: {result}")

    print("\n--- Validation Tests ---")

    invalid_cases = [
        (-1, 10),
        (10, 5),
        (1.5, 10),
        (0, "10"),
    ]

    for start, end in invalid_cases:
        try:
            generate_fibonacci(start, end)
        except (TypeError, ValueError) as error:
            print(f"Input ({start}, {end}) -> {error}")


def run_benchmarks():
    """Benchmark several sequence limits."""

    print("\n--- Execution-Time Benchmarks ---")

    limits = [10, 20, 30, 50]
    repetitions = 1000

    results = []

    for end in limits:
        average_time = benchmark_fibonacci(0, end, repetitions)
        results.append((end, average_time))
        print(
            f"Range 0-{end}: "
            f"{average_time:.10f} seconds per execution"
        )

    return results


def main():
    """Run the complete demonstration."""

    print("=" * 55)
    print("TASK 2 - FIBONACCI GENERATION MODULE")
    print("=" * 55)

    run_tests()
    run_benchmarks()


if __name__ == "__main__":
    main()
