import time
import tracemalloc
from typing import Callable, Any, Tuple


def measure_performance(
        algorithm_function: Callable[[str, str], Any],
        X: str,
        Y: str
) -> Tuple[float, float, Any]:

    # Start memory tracking
    tracemalloc.start()

    # Measure execution time
    start_time = time.perf_counter()
    result = algorithm_function(X, Y)
    end_time = time.perf_counter()

    # Get peak memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Convert to appropriate units
    time_ms = (end_time - start_time) * 1000  # Convert seconds to milliseconds
    memory_MB = peak / (1024 * 1024)  # Convert bytes to megabytes

    return time_ms, memory_MB, result


def format_time(time_ms: float) -> str:
    """Format time for display"""
    if time_ms < 1:
        return f"{time_ms * 1000:.2f} μs"
    elif time_ms < 1000:
        return f"{time_ms:.2f} ms"
    else:
        return f"{time_ms / 1000:.2f} s"


def format_memory(memory_MB: float) -> str:
    """Format memory for display"""
    if memory_MB < 1:
        return f"{memory_MB * 1024:.2f} KB"
    else:
        return f"{memory_MB:.2f} MB"


def compare_algorithms(
        algorithms: dict,
        X: str,
        Y: str,
        skip_slow: bool = True
) -> dict:
    results = {}

    for name, func in algorithms.items():
        # Skip brute force for large inputs
        if skip_slow and name == "Brute Force" and len(X) > 20:
            results[name] = {
                'time_ms': None,
                'memory_MB': None,
                'result': None,
                'status': 'SKIPPED (input too large)'
            }
            continue

        try:
            time_ms, memory_MB, result = measure_performance(func, X, Y)

            results[name] = {
                'time_ms': time_ms,
                'memory_MB': memory_MB,
                'result': result,
                'status': 'SUCCESS'
            }
        except Exception as e:
            results[name] = {
                'time_ms': None,
                'memory_MB': None,
                'result': None,
                'status': f'ERROR: {str(e)}'
            }

    return results


def run_comprehensive_analysis():
    """
    Run comprehensive analysis comparing all LCS algorithms.
    """
    from lcs_bruteforce import solve_brute_force
    from lcs_backtrack import solve_backtrack
    from lcs_dp_standard import solve_dp_standard
    from lcs_dp_optimized import solve_dp_optimized

    print("🔬 Comprehensive LCS Algorithm Analysis")
    print("=" * 70)

    # Test cases of varying sizes
    test_cases = [
        {
            'name': 'Tiny',
            'X': 'ABC',
            'Y': 'AC',
            'expected': 2
        },
        {
            'name': 'Small',
            'X': 'ABCBDAB',
            'Y': 'BDCABA',
            'expected': 4
        },
        {
            'name': 'Medium',
            'X': 'AGGTAB' * 3,
            'Y': 'GXTXAYB' * 3,
            'expected': 12
        },
        {
            'name': 'Large',
            'X': 'ABCDEFGHIJ' * 10,
            'Y': 'ACEGHJ' * 15,
            'expected': None  # We'll calculate this
        }
    ]

    algorithms = {
        'Brute Force': solve_brute_force,
        'Backtracking': solve_backtrack,
        'Standard DP': solve_dp_standard,
        'Optimized DP': solve_dp_optimized
    }

    for test in test_cases:
        print(f"\n{'=' * 70}")
        print(f"📊 Test: {test['name']}")
        print(f"   |X| = {len(test['X'])}, |Y| = {len(test['Y'])}")
        print(f"{'=' * 70}")

        results = compare_algorithms(algorithms, test['X'], test['Y'])

        # Display results in a formatted table
        print(f"\n{'Algorithm':<20} {'Length':<10} {'Time':<15} {'Memory':<12} {'Status':<15}")
        print("-" * 70)

        for algo_name, algo_result in results.items():
            if algo_result['status'] == 'SUCCESS':
                # Extract length
                result = algo_result['result']
                if isinstance(result, tuple):
                    length = result[0]
                else:
                    length = result

                print(f"{algo_name:<20} {length:<10} "
                      f"{format_time(algo_result['time_ms']):<15} "
                      f"{format_memory(algo_result['memory_MB']):<12} "
                      f"{algo_result['status']:<15}")
            else:
                print(f"{algo_name:<20} {'N/A':<10} {'N/A':<15} {'N/A':<12} {algo_result['status']:<15}")

    print(f"\n{'=' * 70}")
    print("✅ Analysis Complete!")
    print(f"{'=' * 70}\n")


# Test the measurement function
if __name__ == "__main__":
    print("🧪 Testing Performance Measurement Tools")
    print("=" * 50)


    # Simple test function
    def dummy_lcs(X: str, Y: str) -> int:
        """Dummy function for testing"""
        time.sleep(0.01)  # Simulate work
        data = [0] * 1000000  # Allocate some memory
        return min(len(X), len(Y))


    X = "ABCBDAB"
    Y = "BDCABA"

    print(f"Testing with X='{X}', Y='{Y}'")

    time_ms, memory_MB, result = measure_performance(dummy_lcs, X, Y)

    print(f"\nResults:")
    print(f"  Time: {format_time(time_ms)}")
    print(f"  Memory: {format_memory(memory_MB)}")
    print(f"  Result: {result}")
    print("\n✅ Performance measurement tools working correctly!")

    # Run comprehensive analysis
    print("\n" + "=" * 70)
    print("Running comprehensive analysis with all algorithms...")
    print("=" * 70)
    run_comprehensive_analysis()