# Hala Backtracking/Sequence Reconstruction
from typing import List


def reconstruct_lcs(X: str, Y: str, dp_table: List[List[int]]) -> str:
    i = len(X)
    j = len(Y)
    lcs_chars = []

    # Backtrack through the DP table
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            # Characters match - part of LCS
            lcs_chars.append(X[i - 1])
            i -= 1
            j -= 1
        else:
            # Characters don't match - move to larger value
            if dp_table[i - 1][j] >= dp_table[i][j - 1]:
                i -= 1
            else:
                j -= 1

    # We built the LCS backwards, so reverse it
    lcs_chars.reverse()
    return "".join(lcs_chars)


def solve_backtrack(X: str, Y: str) -> tuple[int, str]:
    m = len(X)
    n = len(Y)

    # Build the DP table (same as standard DP)
    dp_table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp_table[i][j] = dp_table[i - 1][j - 1] + 1
            else:
                dp_table[i][j] = max(dp_table[i - 1][j], dp_table[i][j - 1])

    # Get the LCS length
    length = dp_table[m][n]

    # Reconstruct the actual LCS string
    lcs_string = reconstruct_lcs(X, Y, dp_table)

    return length, lcs_string


# Testing code
if __name__ == "__main__":
    # Test case 1
    X = "ABCBDAB"
    Y = "BDCABA"

    length, lcs_sequence = solve_backtrack(X, Y)
    print(f"Input X: {X}")
    print(f"Input Y: {Y}")
    print(f"LCS Length: {length}")
    print(f"LCS Sequence: {lcs_sequence}")
    print()

    # Test case 2 (from documentation example)
    X2 = "ABCDGH"
    Y2 = "AEDFHR"

    length2, lcs_sequence2 = solve_backtrack(X2, Y2)
    print(f"Input X: {X2}")
    print(f"Input Y: {Y2}")
    print(f"LCS Length: {length2}")
    print(f"LCS Sequence: {lcs_sequence2}")
