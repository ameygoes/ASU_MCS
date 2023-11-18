from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ratings = np.array([
    [3, 2, 5, 4],
    [2, np.nan, 4, 3],
    [1, 4, 2, 3],
    [3, 4, 3, 5]
])


def fill_missing_ratings(ratings):
    # Transpose the ratings matrix for item-based collaborative filtering
    ratings_transposed = ratings.T

    # Replace NaN values with zeros
    ratings_transposed = np.nan_to_num(ratings_transposed)

    for i in range(ratings.shape[0]):
        for j in range(ratings.shape[1]):
            if np.isnan(ratings[i, j]):
                # Calculate average rating for the target item
                avg_rating_i = np.nanmean(ratings_transposed[i])

                # Calculate cosine similarity between the target item and other items
                similarities = cosine_similarity([ratings_transposed[i]], ratings_transposed)[0]

                # Use item-based collaborative filtering formula to fill the missing value
                numerator = np.sum(similarities * (ratings[:, j] - np.nanmean(ratings, axis=0)[j]))
                denominator = np.sum(np.abs(similarities))

                # Fill the missing value
                ratings[i, j] = avg_rating_i + numerator / denominator

    return ratings

# Fill missing values
filled_ratings = fill_missing_ratings(ratings)

print("Original Ratings:")
print(ratings)

print("\nFilled Ratings:")
print(filled_ratings)
