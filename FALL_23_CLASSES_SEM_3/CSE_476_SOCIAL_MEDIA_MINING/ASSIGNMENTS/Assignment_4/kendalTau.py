def kendall_tau_coefficient(arr1, arr2):
    """
    Calculate Kendall Tau coefficient, concordant pairs (c), and discordant pairs (d).

    Parameters:
    - arr1, arr2: Lists representing the paired observations.

    Returns:
    - Kendall Tau coefficient, c, d
    """
    n = len(arr1)
    c = 0
    d = 0
    concordant = []
    disconcordantPairs = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            # Check for concordant and discordant pairs
            if (arr1[i] - arr1[j]) * (arr2[i] - arr2[j]) > 0:
                c += 1
                concordant.append((arr1[i], arr1[j]))
            elif (arr1[i] - arr1[j]) * (arr2[i] - arr2[j]) < 0:
                d += 1
                disconcordantPairs.append((arr1[i], arr1[j]))

    # Calculate Kendall Tau coefficient
    tau = (c - d) / (c + d)

    return tau, c, d, concordant, disconcordantPairs

# Example usage:
predicted = [1, 2, 3, 4, 5 ,6]
true = [1, 4, 3, 6, 2, 5]

tau_coefficient, concordant_pairs, discordant_pairs, concordant, disconcordantPairs = kendall_tau_coefficient(predicted, true)

print(f"Kendall Tau Coefficient: {tau_coefficient}")

print(f"Number of Concordant Pairs (c): {concordant_pairs}")
print(f"Concordant Pairs: {concordant}")

print(f"Number of Discordant Pairs (d): {discordant_pairs}")
print(f"Discordant Pairs: {disconcordantPairs}")
