import numpy as np
import pandas as pd

# Example data: User-Movie rating matrix
ratings_data = {
    'User': [1, 2, 3, 4, 5, 6, 7],
    'The Matrix': [5, 4, 0, 0, 3, 0, 2],
    'Inception': [4, 0, 0, 2, 4, 0, 3],
    'Toy Story': [0, 0, 5, 4, 0, 2, 0],
    'The Godfather': [0, 3, 4, 0, 5, 0, 5],
    'Finding Nemo': [2, 3, 4, 0, 0, 3, 4],
    'Interstellar': [0, 0, 0, 5, 2, 4, 0]
}

# Create a DataFrame for user-movie ratings
df_ratings = pd.DataFrame(ratings_data)
df_ratings.set_index('User', inplace=True)
print("Here's the User-Movie Ratings Matrix:")
print(df_ratings)

# Example movie metadata: (genres represented as binary features)
movie_features = {
    'Movie': ['The Matrix', 'Inception', 'Toy Story', 'The Godfather', 'Finding Nemo', 'Interstellar'],
    'Action': [1, 1, 0, 0, 0, 1],
    'Sci-Fi': [1, 1, 0, 0, 0, 1],
    'Animation': [0, 0, 1, 0, 1, 0],
    'Drama': [0, 1, 0, 1, 0, 1],
    'Family': [0, 0, 1, 0, 1, 0]
}

df_movies = pd.DataFrame(movie_features)
df_movies.set_index('Movie', inplace=True)
print("\nHere's some information about movie genres:")
print(df_movies)


def recommend_similar_movies(movie_name, df_movies, num_recommendations=2):
    if movie_name not in df_movies.index:
        return f"Oops! It looks like '{movie_name}' isn't in our movie list. Could you please enter a valid movie name?"

    # Get features of the chosen movie
    movie_features = df_movies.loc[movie_name]

    # Compute similarity scores
    movie_similarity = df_movies.dot(movie_features)

    # Get top recommendations
    recommendations = movie_similarity.drop(movie_name).nlargest(num_recommendations)

    if recommendations.empty:
        return f"Looks like we don't have any other movies similar to '{movie_name}' at the moment."

    return recommendations


def recommend_movies(movie_name, df_movies, num_recommendations=2):
    return recommend_similar_movies(movie_name, df_movies, num_recommendations)


# Interactions
try:
    movie_name = input("Hey there! Which movie would you like recommendations for? ").strip()
    num_recommendations = int(input("How many movie recommendations are you interested in? "))

    # Get recommendations based on the chosen movie
    recommended_movies = recommend_movies(movie_name, df_movies, num_recommendations)

    print(f"\nSearching for the top {num_recommendations} movies similar to '{movie_name}':")
    print(recommended_movies)

except ValueError:
    print("Oops! It seems like you entered an invalid name. Please try again with a valid movie for recommendations.")
