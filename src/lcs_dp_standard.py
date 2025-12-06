# Rawan Standard DP (2D Table)
def solve_dp_standard(X: str, Y: str) -> tuple[int, list[list[int]]]:
    n = len(X)
    m = len(Y)

    dp_table = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            if X[i - 1] == Y[j - 1]:
                dp_table[i][j] = dp_table[i - 1][j - 1] + 1

            else:
                dp_table[i][j] = max(dp_table[i][j - 1], dp_table[i - 1][j])

    max_length = dp_table[n][m]

    return max_length, dp_table


if __name__ == "__main__":

    X = "ABCBDAB"
    Y = "BDCABA"

    print(" Running LCS Standard DP Solver ")
    print(f"Input String X: {X}")
    print(f"Input String Y: {Y}")

    length, dp_table = solve_dp_standard(X, Y)

    print("\n" + "=" * 40)
    print(f"Calculated Max Length: {length}")
    print(f"Expected Max Length: 4")
    print(f"Expected Table Size: ({len(X) + 1}) x ({len(Y) + 1}) = {len(dp_table)} x {len(dp_table[0])}")
    print("=" * 40)

    print("\nDP Table (LCS Lengths):")

    header = [" "] + list(Y)
    print("    " + " ".join(f"{h:^3}" for h in header))
    print("  " + " ".join("  " for _ in range(len(header) + 1)))


    for i in range(len(dp_table)):
        row = dp_table[i]

        row_label = X[i - 1] if i > 0 else " "

        row_output = " ".join(f"{val:^3}" for val in row)
        print(f"{row_label}| {row_output}")

    if length == 4 and dp_table[len(X)][len(Y)] == 4:
        print("\n VERIFICATION SUCCESSFUL: Max length and final cell value are correct.")
    else:
        print("\n VERIFICATION FAILED: Check your recurrence logic or indexing.")