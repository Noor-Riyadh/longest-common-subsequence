# Manar  - Brute Force
def solve_brute_force(X: str, Y: str) -> tuple[int, str]:
    def is_subsequence(sub: str, text: str) -> bool:
        it = iter(text)
        return all(ch in it for ch in sub)

    n = len(X)
    longest_length = 0
    longest_sequence = ""

    for mask in range(1 << n):
        subsequence = ''.join(X[i] for i in range(n) if (mask >> i) & 1)

        if is_subsequence(subsequence, Y):
            if len(subsequence) > longest_length:
                longest_length = len(subsequence)
                longest_sequence = subsequence

    return longest_length, longest_sequence


# Test code
if __name__ == "__main__":
    X = "ABCBDAB"
    Y = "BDCABA"

    print("🔍 Running LCS Brute Force Solver")
    print(f"Input String X: {X}")
    print(f"Input String Y: {Y}")
    print("=" * 40)

    length, sequence = solve_brute_force(X, Y)

    print(f"LCS Length: {length}")
    print(f"LCS Sequence: '{sequence}'")
    print(f"Expected Length: 4")
    print("=" * 40)

    if length == 4:
        print("VERIFICATION SUCCESSFUL")
    else:
        print("VERIFICATION FAILED")