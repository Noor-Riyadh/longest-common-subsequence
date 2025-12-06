def solve_dp_optimized(X: str, Y: str) -> int:

    n = len(X)
    m = len(Y)

    # Optimize: iterate over shorter string to minimize space
    if n > m:
        X, Y = Y, X
        n, m = m, n

    # Use only two 1D arrays: previous row and current row
    prev_row = [0] * (m + 1)
    curr_row = [0] * (m + 1)

    # Fill the arrays using same recurrence as standard DP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if X[i - 1] == Y[j - 1]:
                # Characters match: add 1 to diagonal value
                curr_row[j] = prev_row[j - 1] + 1
            else:
                # Characters don't match: take max of left or top
                curr_row[j] = max(curr_row[j - 1], prev_row[j])

        # Move to next row: current becomes previous
        prev_row, curr_row = curr_row, [0] * (m + 1)

    # Result is in the last cell of prev_row
    return prev_row[m]


# Test code
if __name__ == "__main__":
    X = "ABCBDAB"
    Y = "BDCABA"

    print("💾 Running LCS Space-Optimized DP Solver")
    print(f"Input String X: {X}")
    print(f"Input String Y: {Y}")
    print("=" * 40)

    length = solve_dp_optimized(X, Y)

    print(f"LCS Length: {length}")
    print(f"Expected Length: 4")
    print("=" * 40)

    # Compare space usage
    n, m = len(X), len(Y)
    standard_space = (n + 1) * (m + 1)
    optimized_space = min(n, m) + 1

    print(f"\nSpace Comparison:")
    print(f"Standard DP: {standard_space} cells ({(n + 1)} × {(m + 1)})")
    print(f"Optimized DP: {optimized_space} cells (2 rows of {min(n, m) + 1})")
    print(f"Space Saved: {standard_space - optimized_space} cells")
    print(f"Reduction: {(1 - optimized_space / standard_space) * 100:.1f}%")

    if length == 4:
        print("\n VERIFICATION SUCCESSFUL")
    else:
        print("\n VERIFICATION FAILED")