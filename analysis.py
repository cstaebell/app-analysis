# -*- coding: utf-8 -*-
"""
App Analysis

Adapted from Dataquest Guided Project: Profitable App Profiles for the App Store and Google Play Markets

"""

#%% Import packages and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

apple = pd.read_csv("AppleStore.csv")
google = pd.read_csv("googleplaystore.csv")

#%% Explore data
apple.info()
apple.iloc[0,:]
apple.isna().sum()

google.info()
google.iloc[0,:]
google.isna().sum()

#%% Clean data
# Remove rows from google with NaN values (except for Rating)
google = google.dropna(subset = ["Type", "Content Rating", "Current Ver", "Android Ver"])

# Identify duplicate app entries
apple_dups_mask = apple.duplicated(subset=["track_name"], keep=False)
google_dups_mask = google.duplicated(subset=["App"], keep=False)

# Find entries with highest number of ratings to keep
apple_dups = apple[apple_dups_mask].loc[:,["track_name", "rating_count_tot"]]
apple_retain = apple_dups.groupby("track_name")["rating_count_tot"].idxmax()
apple_dups_mask[apple_retain] = False

google_dups = google[google_dups_mask].loc[:, ["App", "Reviews"]]
google_retain = google_dups.groupby("App")["Reviews"].idxmax()
google_dups_mask[google_retain] = False

# Remove duplicates
apple = apple[~apple_dups_mask]
google = google[~google_dups_mask]

#%% Identify and remove non-English apps
def check_english(string):
    counter = 0
    for char in string:
        if ord(char) > 127:
            counter += 1
        if counter > 3:    
            return False
    return True

apple_english_mask = apple["track_name"].apply(check_english)
google_english_mask = google["App"].apply(check_english)

apple = apple[apple_english_mask]
google = google[google_english_mask]

#%% Keep only free apps
apple.columns # price
google.columns # Price

apple_free = apple[apple["price"] == 0]
google_free = google[google["Price"] == '0']

#%% Find most common apps by genre for both datasets

# apple: rating_count_tot, user_rating, prime_genre
# google: Ratings, Reviews, Installs, Genres

apple_genre_counts = apple_free.groupby("prime_genre")["id"].count().sort_values(ascending=False)
google_genre_counts = google_free.groupby("Genres")["App"].count().sort_values(ascending=False)
google_category_counts = google_free.groupby("Category")["App"].count().sort_values(ascending=False)

apple_genre_counts.plot.bar()
plt.title("Apple Genre Counts")
plt.show()

google_category_counts.plot.bar()
plt.title("Google Play Category Counts")
plt.show()

