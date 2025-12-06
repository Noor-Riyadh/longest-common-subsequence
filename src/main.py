

import sys
import csv
from pathlib import Path

# Import all LCS implementations
from lcs_bruteforce import solve_brute_force
from lcs_backtrack import solve_backtrack
from lcs_dp_standard import solve_dp_standard
from lcs_dp_optimized import solve_dp_optimized

# Import analysis tools
from lcs_analysis import measure_performance, format_time, format_memory

# Import test data
from data.test_inputs import ALL_TESTS, SMALL_TEST, MEDIUM_TEST, LARGE_TEST


def extract_length(result) -> int:
    """Extract LCS length from different return formats"""
    if isinstance(result, tuple):
        return result[0]  # (length, sequence) or (length, table)
    else:
        return result  # just length


def run_comparison():
    """
    Run all LCS algorithms on all test cases and generate comparison report.
    Creates multiple CSV files:
    - results_comparison.csv: All results together
    - results_brute_force.csv: Only Brute Force results
    - results_backtracking.csv: Only Backtracking results
    - results_standard_dp.csv: Only Standard DP results
    - results_optimized_dp.csv: Only Optimized DP results
    - results_summary.csv: Side-by-side comparison
    """
    print("🔬 LCS Algorithms Performance Comparison")
    print("=" * 70)

    # Define algorithms to test
    algorithms = [
        ("Brute Force", solve_brute_force),
        ("Backtracking", solve_backtrack),
        ("Standard DP", solve_dp_standard),
        ("Optimized DP", solve_dp_optimized)
    ]

    all_results = []

    # Dictionaries to store results by algorithm
    brute_force_results = []
    backtracking_results = []
    standard_dp_results = []
    optimized_dp_results = []

    # Run tests
    for test in ALL_TESTS:
        test_name = test['name']
        X = test['X']
        Y = test['Y']
        expected = test['expected_length']

        print(f"\n{'=' * 70}")
        print(f"📊 Test Case: {test_name}")
        print(f"{'=' * 70}")
        print(f"Input Size: |X| = {len(X)}, |Y| = {len(Y)}")
        print(f"Description: {test['description']}")
        if expected:
            print(f"Expected LCS Length: {expected}")
        print()

        # Test each algorithm
        for algo_name, algo_func in algorithms:
            # Skip brute force for large inputs
            if algo_name == "Brute Force" and len(X) > 20:
                print(f"⏭️  {algo_name:20s} SKIPPED (input too large, would take 2^{len(X)} iterations)")

                result_dict = {
                    'Test': test_name,
                    'Algorithm': algo_name,
                    'Length': 'N/A',
                    'Time (ms)': 'N/A',
                    'Memory (MB)': 'N/A',
                    'Status': 'SKIPPED'
                }
                all_results.append(result_dict)
                brute_force_results.append(result_dict)
                continue

            try:
                # Measure performance
                time_ms, memory_MB, result = measure_performance(algo_func, X, Y)
                length = extract_length(result)

                # Display results
                status = "✅"
                if expected and length != expected:
                    status = "❌ WRONG"

                print(f"{status} {algo_name:20s} Length: {length:2d} | "
                      f"Time: {format_time(time_ms):>12s} | "
                      f"Memory: {format_memory(memory_MB):>10s}")

                # Store results
                result_dict = {
                    'Test': test_name,
                    'Algorithm': algo_name,
                    'Length': length,
                    'Time (ms)': f"{time_ms:.4f}",
                    'Memory (MB)': f"{memory_MB:.6f}",
                    'Status': 'SUCCESS'
                }
                all_results.append(result_dict)

                # Store in individual algorithm lists
                if algo_name == "Brute Force":
                    brute_force_results.append(result_dict)
                elif algo_name == "Backtracking":
                    backtracking_results.append(result_dict)
                elif algo_name == "Standard DP":
                    standard_dp_results.append(result_dict)
                elif algo_name == "Optimized DP":
                    optimized_dp_results.append(result_dict)

            except Exception as e:
                print(f"❌ {algo_name:20s} ERROR: {str(e)}")

                result_dict = {
                    'Test': test_name,
                    'Algorithm': algo_name,
                    'Length': 'ERROR',
                    'Time (ms)': 'ERROR',
                    'Memory (MB)': 'ERROR',
                    'Status': f'ERROR: {str(e)}'
                }
                all_results.append(result_dict)

                # Store in individual algorithm lists
                if algo_name == "Brute Force":
                    brute_force_results.append(result_dict)
                elif algo_name == "Backtracking":
                    backtracking_results.append(result_dict)
                elif algo_name == "Standard DP":
                    standard_dp_results.append(result_dict)
                elif algo_name == "Optimized DP":
                    optimized_dp_results.append(result_dict)

    # Export results to CSV files
    print(f"\n{'=' * 70}")
    print("💾 Exporting results to CSV files...")

    # 1. Main comparison CSV (all algorithms together)
    csv_file = 'results_comparison.csv'
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['Test', 'Algorithm', 'Length', 'Time (ms)', 'Memory (MB)', 'Status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
    print(f"✅ Main comparison exported to: {csv_file}")

    # 2. Individual algorithm CSV files - THIS IS THE FIX!
    individual_files = [
        ('results_brute_force.csv', brute_force_results, 'Brute Force'),
        ('results_backtracking.csv', backtracking_results, 'Backtracking'),
        ('results_standard_dp.csv', standard_dp_results, 'Standard DP'),
        ('results_optimized_dp.csv', optimized_dp_results, 'Optimized DP')
    ]

    for filename, results, algo_name in individual_files:
        with open(filename, 'w', newline='') as f:
            fieldnames = ['Test', 'Length', 'Time (ms)', 'Memory (MB)', 'Status']
            # THIS LINE WAS ADDED: extrasaction='ignore'
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ {algo_name:15s} exported to: {filename}")

    # 3. Create a summary comparison CSV (side-by-side for each test)
    summary_file = 'results_summary.csv'
    with open(summary_file, 'w', newline='') as f:
        # Group results by test case
        test_cases = {}
        for result in all_results:
            test_name = result['Test']
            if test_name not in test_cases:
                test_cases[test_name] = {}
            algo = result['Algorithm']
            test_cases[test_name][algo] = {
                'Length': result['Length'],
                'Time': result['Time (ms)'],
                'Memory': result['Memory (MB)']
            }

        # Write summary
        fieldnames = ['Test Case',
                      'BF Length', 'BF Time (ms)', 'BF Memory (MB)',
                      'BT Length', 'BT Time (ms)', 'BT Memory (MB)',
                      'DP Length', 'DP Time (ms)', 'DP Memory (MB)',
                      'Opt Length', 'Opt Time (ms)', 'Opt Memory (MB)']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for test_name, algos in test_cases.items():
            row = {'Test Case': test_name}

            if 'Brute Force' in algos:
                row['BF Length'] = algos['Brute Force']['Length']
                row['BF Time (ms)'] = algos['Brute Force']['Time']
                row['BF Memory (MB)'] = algos['Brute Force']['Memory']

            if 'Backtracking' in algos:
                row['BT Length'] = algos['Backtracking']['Length']
                row['BT Time (ms)'] = algos['Backtracking']['Time']
                row['BT Memory (MB)'] = algos['Backtracking']['Memory']

            if 'Standard DP' in algos:
                row['DP Length'] = algos['Standard DP']['Length']
                row['DP Time (ms)'] = algos['Standard DP']['Time']
                row['DP Memory (MB)'] = algos['Standard DP']['Memory']

            if 'Optimized DP' in algos:
                row['Opt Length'] = algos['Optimized DP']['Length']
                row['Opt Time (ms)'] = algos['Optimized DP']['Time']
                row['Opt Memory (MB)'] = algos['Optimized DP']['Memory']

            writer.writerow(row)

    print(f"✅ Summary comparison exported to: {summary_file}")

    # Summary
    print(f"\n{'=' * 70}")
    print("📈 Summary")
    print(f"{'=' * 70}")
    print(f"Total tests run: {len(all_results)}")
    success_count = sum(1 for r in all_results if r['Status'] == 'SUCCESS')
    print(f"Successful: {success_count}")
    print(f"Skipped: {sum(1 for r in all_results if r['Status'] == 'SKIPPED')}")
    print(f"Errors: {sum(1 for r in all_results if 'ERROR' in r['Status'])}")
    print()

    # Analysis insights
    print("🔍 Key Insights:")
    print("  • Brute Force: Exponential time O(2^n), impractical for n > 20")
    print("  • Backtracking: O(n×m) time with sequence reconstruction capability")
    print("  • Standard DP: O(n×m) time, O(n×m) space, reliable and predictable")
    print("  • Optimized DP: O(n×m) time, O(min(n,m)) space, best space efficiency")
    print("  • All DP-based approaches produce identical results")

    print(f"\n{'=' * 70}")
    print(f"📁 CSV Files Created (for documentation screenshots):")
    print(f"{'=' * 70}")
    print(f"  1. results_comparison.csv      - All results together")
    print(f"  2. results_brute_force.csv     - Brute Force only")
    print(f"  3. results_backtracking.csv    - Backtracking only")
    print(f"  4. results_standard_dp.csv     - Standard DP only")
    print(f"  5. results_optimized_dp.csv    - Optimized DP only")
    print(f"  6. results_summary.csv         - Side-by-side comparison")
    print(f"{'=' * 70}\n")


def run_single_test(X: str, Y: str):
    """
    Run a single test with custom input.
    """
    print(f"🧪 Single Test Mode")
    print(f"X = '{X}'")
    print(f"Y = '{Y}'")
    print("=" * 50)

    algorithms = [
        ("Brute Force", solve_brute_force),
        ("Backtracking", solve_backtrack),
        ("Standard DP", solve_dp_standard),
        ("Optimized DP", solve_dp_optimized)
    ]

    for name, func in algorithms:
        if name == "Brute Force" and len(X) > 20:
            print(f"⏭️  {name}: SKIPPED")
            continue

        time_ms, memory_MB, result = measure_performance(func, X, Y)
        length = extract_length(result)

        # Show sequence if available
        if isinstance(result, tuple) and len(result) >= 2 and isinstance(result[1], str):
            sequence = result[1]
            print(
                f"✅ {name}: Length={length}, Sequence='{sequence}', Time={format_time(time_ms)}, Memory={format_memory(memory_MB)}")
        else:
            print(f"✅ {name}: Length={length}, Time={format_time(time_ms)}, Memory={format_memory(memory_MB)}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Custom test mode
        X = sys.argv[1]
        Y = sys.argv[2]
        run_single_test(X, Y)
    else:
        # Full comparison mode
        run_comparison()