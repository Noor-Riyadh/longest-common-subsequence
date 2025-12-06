"""
Test input data for LCS algorithms comparison.
Includes small, medium, and large test cases.
"""

# Small test case - for quick verification
SMALL_TEST = {
    'name': 'Small',
    'X': "ABCBDAB",
    'Y': "BDCABA",
    'expected_length': 4,
    'description': 'Classic example from textbooks'
}

# Medium test case - moderate complexity
MEDIUM_TEST = {
    'name': 'Medium',
    'X': "AGGTABCDEFGHIJ",  # Length 14
    'Y': "GXTXAYBMNOPQRS",  # Length 14
    'expected_length': 6,  # "GTAB" or similar
    'description': 'Medium-sized strings to show performance differences'
}

# Large test case - demonstrates brute force failure
LARGE_TEST = {
    'name': 'Large',
    'X': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # Length 26
    'Y': "ACEGIKMOQSUWYABDFHJLNPRT",  # Length 24
    'expected_length': None,  # Will be calculated by DP (around 13-14)
    'description': 'Large input where brute force becomes impractical (2^26 subsequences)'
}

# Extra large test case - for extreme performance testing (optional)
EXTRA_LARGE_TEST = {
    'name': 'Extra Large',
    'X': "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2,  # Length 52
    'Y': "ACEGIKMOQSUWYABDFHJLNPRT" * 2,  # Length 48
    'expected_length': None,  # Will be calculated
    'description': 'Very large input to stress-test algorithms'
}

# All test cases in a list for easy iteration
ALL_TESTS = [SMALL_TEST, MEDIUM_TEST, LARGE_TEST]

# Test cases for specific scenarios
EDGE_CASES = {
    'empty_strings': {
        'X': "",
        'Y': "",
        'expected_length': 0
    },
    'one_empty': {
        'X': "ABCD",
        'Y': "",
        'expected_length': 0
    },
    'identical': {
        'X': "ABCDEF",
        'Y': "ABCDEF",
        'expected_length': 6
    },
    'no_common': {
        'X': "AAAA",
        'Y': "BBBB",
        'expected_length': 0
    }
}

if __name__ == "__main__":
    """Display test case information"""
    print("📊 LCS Test Cases Overview")
    print("=" * 60)

    for test in ALL_TESTS:
        print(f"\n{test['name']} Test:")
        print(f"  X length: {len(test['X'])}")
        print(f"  Y length: {len(test['Y'])}")
        print(f"  X: {test['X'][:30]}{'...' if len(test['X']) > 30 else ''}")
        print(f"  Y: {test['Y'][:30]}{'...' if len(test['Y']) > 30 else ''}")
        print(f"  Expected LCS length: {test['expected_length']}")
        print(f"  Description: {test['description']}")

        if test['name'] == 'Large':
            print(f"  ⚠️  Brute force would need to check 2^{len(test['X'])} = {2 ** len(test['X']):,} subsequences!")

    print("\n" + "=" * 60)