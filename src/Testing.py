"""
Comprehensive testing suite for all LCS algorithm implementations.
Verifies correctness of all approaches on various test cases.
"""

from lcs_bruteforce import solve_brute_force
from lcs_backtrack import solve_backtrack
from lcs_dp_standard import solve_dp_standard
from lcs_dp_optimized import solve_dp_optimized


def extract_length(result):
    """Extract LCS length from different return formats"""
    if isinstance(result, tuple):
        return result[0]
    return result


def extract_sequence(result):
    """Extract LCS sequence if available"""
    if isinstance(result, tuple) and len(result) >= 2 and isinstance(result[1], str):
        return result[1]
    return None


class TestCase:
    """Represents a test case for LCS algorithms"""

    def __init__(self, name, X, Y, expected_length, expected_sequences=None):
        self.name = name
        self.X = X
        self.Y = Y
        self.expected_length = expected_length
        self.expected_sequences = expected_sequences or []

    def __str__(self):
        return f"{self.name}: X='{self.X}', Y='{self.Y}', Expected Length={self.expected_length}"


# Define comprehensive test cases
TEST_CASES = [
    TestCase(
        name="Empty Strings",
        X="",
        Y="",
        expected_length=0,
        expected_sequences=[""]
    ),
    TestCase(
        name="One Empty String",
        X="ABC",
        Y="",
        expected_length=0,
        expected_sequences=[""]
    ),
    TestCase(
        name="No Common Subsequence",
        X="ABC",
        Y="DEF",
        expected_length=0,
        expected_sequences=[""]
    ),
    TestCase(
        name="Single Character Match",
        X="A",
        Y="A",
        expected_length=1,
        expected_sequences=["A"]
    ),
    TestCase(
        name="Identical Strings",
        X="HELLO",
        Y="HELLO",
        expected_length=5,
        expected_sequences=["HELLO"]
    ),
    TestCase(
        name="Simple Case",
        X="ABC",
        Y="AC",
        expected_length=2,
        expected_sequences=["AC"]
    ),
    TestCase(
        name="Classic Example 1",
        X="ABCBDAB",
        Y="BDCABA",
        expected_length=4,
        expected_sequences=["BCBA", "BDAB", "BCAB"]  # Multiple valid LCS
    ),
    TestCase(
        name="Classic Example 2",
        X="ABCDGH",
        Y="AEDFHR",
        expected_length=3,
        expected_sequences=["ADH"]
    ),
    TestCase(
        name="All Different",
        X="AAAA",
        Y="BBBB",
        expected_length=0,
        expected_sequences=[""]
    ),
    TestCase(
        name="Substring",
        X="ABCDEF",
        Y="ACE",
        expected_length=3,
        expected_sequences=["ACE"]
    ),
    TestCase(
        name="Reversed",
        X="ABC",
        Y="CBA",
        expected_length=1,
        expected_sequences=["A", "B", "C"]  # Multiple valid single-char LCS
    ),
    TestCase(
        name="Repeated Characters",
        X="AAABBB",
        Y="AABB",
        expected_length=4,
        expected_sequences=["AABB"]
    ),
    TestCase(
        name="Long Common Prefix",
        X="ABCXYZ",
        Y="ABCPQR",
        expected_length=3,
        expected_sequences=["ABC"]
    ),
    TestCase(
        name="Long Common Suffix",
        X="XYZABC",
        Y="PQRABC",
        expected_length=3,
        expected_sequences=["ABC"]
    ),
    TestCase(
        name="Interleaved",
        X="AGGTAB",
        Y="GXTXAYB",
        expected_length=4,
        expected_sequences=["GTAB"]
    )
]


def test_algorithm(algo_name, algo_func, test_case, verbose=False):
    """
    Test a single algorithm on a single test case.

    Returns:
        bool: True if test passed, False otherwise
    """
    try:
        result = algo_func(test_case.X, test_case.Y)
        length = extract_length(result)
        sequence = extract_sequence(result)

        # Check length
        if length != test_case.expected_length:
            print(f"  ❌ {algo_name}: FAILED")
            print(f"     Expected length: {test_case.expected_length}")
            print(f"     Got length: {length}")
            if sequence:
                print(f"     Sequence: '{sequence}'")
            return False

        # If sequence is available, verify it's valid
        if sequence is not None and test_case.expected_sequences:
            if sequence not in test_case.expected_sequences:
                print(f"  ⚠️  {algo_name}: Length correct but unexpected sequence")
                print(f"     Expected one of: {test_case.expected_sequences}")
                print(f"     Got: '{sequence}'")
                # This is a warning, not a failure (could be another valid LCS)

        if verbose:
            status = "✅"
            msg = f"{status} {algo_name}: PASSED (Length={length}"
            if sequence:
                msg += f", Sequence='{sequence}'"
            msg += ")"
            print(f"  {msg}")
        else:
            print(f"  ✅ {algo_name}: PASSED")

        return True

    except Exception as e:
        print(f"  ❌ {algo_name}: ERROR - {str(e)}")
        return False


def run_all_tests(verbose=False):
    """
    Run all test cases on all algorithms.
    """
    print("=" * 80)
    print("🧪 COMPREHENSIVE LCS ALGORITHM TESTING SUITE")
    print("=" * 80)
    print()

    algorithms = [
        ("Brute Force", solve_brute_force),
        ("Backtracking", solve_backtrack),
        ("Standard DP", solve_dp_standard),
        ("Optimized DP", solve_dp_optimized)
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    for test_case in TEST_CASES:
        print(f"📋 Test: {test_case.name}")
        if verbose:
            print(f"   X = '{test_case.X}'")
            print(f"   Y = '{test_case.Y}'")
            print(f"   Expected Length = {test_case.expected_length}")
        print()

        for algo_name, algo_func in algorithms:
            # Skip brute force for long strings
            if algo_name == "Brute Force" and len(test_case.X) > 20:
                print(f"  ⏭️  {algo_name}: SKIPPED (input too large)")
                continue

            total_tests += 1
            if test_algorithm(algo_name, algo_func, test_case, verbose):
                passed_tests += 1
            else:
                failed_tests += 1

        print()

    # Summary
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")

    if failed_tests == 0:
        print()
        print("🎉 ALL TESTS PASSED! 🎉")
        print()
        print("All LCS algorithms are working correctly!")
    else:
        print()
        print("⚠️  Some tests failed. Please review the failures above.")

    print("=" * 80)

    return failed_tests == 0


def test_consistency():
    """
    Test that all algorithms produce the same LCS length for all test cases.
    """
    print()
    print("=" * 80)
    print("🔍 CONSISTENCY CHECK: Verifying all algorithms agree on LCS length")
    print("=" * 80)
    print()

    algorithms = [
        ("Brute Force", solve_brute_force),
        ("Backtracking", solve_backtrack),
        ("Standard DP", solve_dp_standard),
        ("Optimized DP", solve_dp_optimized)
    ]

    inconsistencies = 0

    for test_case in TEST_CASES:
        # Skip large inputs for brute force
        if len(test_case.X) > 20:
            test_algorithms = algorithms[1:]  # Skip brute force
        else:
            test_algorithms = algorithms

        results = {}
        for algo_name, algo_func in test_algorithms:
            result = algo_func(test_case.X, test_case.Y)
            length = extract_length(result)
            results[algo_name] = length

        # Check if all results are the same
        lengths = list(results.values())
        if len(set(lengths)) > 1:
            print(f"❌ INCONSISTENCY in '{test_case.name}':")
            for algo_name, length in results.items():
                print(f"   {algo_name}: {length}")
            inconsistencies += 1
        else:
            print(f"✅ {test_case.name}: All algorithms agree (Length={lengths[0]})")

    print()
    if inconsistencies == 0:
        print("🎉 PERFECT CONSISTENCY: All algorithms produce identical results!")
    else:
        print(f"⚠️  Found {inconsistencies} inconsistencies!")
    print("=" * 80)
    print()


def quick_test():
    """
    Quick smoke test on a few key cases.
    """
    print("🚀 Quick Smoke Test")
    print("=" * 50)

    test_cases = [
        ("ABC", "AC", 2),
        ("ABCBDAB", "BDCABA", 4),
        ("ABCDGH", "AEDFHR", 3)
    ]

    algorithms = [
        ("Brute Force", solve_brute_force),
        ("Backtracking", solve_backtrack),
        ("Standard DP", solve_dp_standard),
        ("Optimized DP", solve_dp_optimized)
    ]

    all_passed = True

    for X, Y, expected in test_cases:
        print(f"\nTest: X='{X}', Y='{Y}'")
        for algo_name, algo_func in algorithms:
            result = algo_func(X, Y)
            length = extract_length(result)
            if length == expected:
                print(f"  ✅ {algo_name}: {length}")
            else:
                print(f"  ❌ {algo_name}: {length} (expected {expected})")
                all_passed = False

    print()
    if all_passed:
        print("✅ Quick test PASSED!")
    else:
        print("❌ Quick test FAILED!")
    print("=" * 50)
    print()


if __name__ == "__main__":
    # Run quick test first
    quick_test()

    # Run comprehensive tests
    all_passed = run_all_tests(verbose=True)

    # Run consistency check
    test_consistency()

    # Final status
    if all_passed:
        print("\n✅ ALL TESTING COMPLETE - SYSTEM READY FOR PRODUCTION! ✅\n")
    else:
        print("\n❌ TESTING FAILED - PLEASE FIX ISSUES BEFORE DEPLOYMENT ❌\n")