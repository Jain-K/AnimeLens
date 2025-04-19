import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit config
st.set_page_config(layout="wide")
st.title("📅 Seasonal Release Patterns of Anime")
st.markdown("Analyze anime release trends, scores, and popularity based on seasons.")


df = pd.read_csv("./data/anime_cleaned.csv")

# Clean and preprocess
df = df.dropna(subset=['premiered'])
df[['season', 'season_year']] = df['premiered'].str.split(' ', expand=True)
df = df.dropna(subset=['season_year'])
df['season_year'] = df['season_year'].astype(int)

# Sidebar filters
min_year = int(df['season_year'].min())
max_year = int(df['season_year'].max())

year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
seasons = ['Winter', 'Spring', 'Summer', 'Fall']
selected_seasons = st.sidebar.multiselect("Select Seasons", seasons, default=seasons)

# Filter dataset
filtered_df = df[
    (df['season_year'] >= year_range[0]) &
    (df['season_year'] <= year_range[1]) &
    (df['season'].isin(selected_seasons))
]

# Group data for plotting
release_trend = (
    filtered_df.groupby(['season_year', 'season'])['title']
    .count()
    .reset_index()
    .rename(columns={'title': 'anime_count'})
)

avg_score = (
    filtered_df.groupby('season')['score']
    .mean()
    .reset_index()
    .sort_values(by='score', ascending=False)
)

avg_popularity = (
    filtered_df.groupby('season')['popularity']
    .mean()
    .reset_index()
    .sort_values(by='popularity')
)

# Plotting release trend
st.subheader("Anime Releases by Season Over Time")
fig1, ax1 = plt.subplots(figsize=(14, 6))
sns.lineplot(data=release_trend, x='season_year', y='anime_count', hue='season', marker='o', ax=ax1)
ax1.set_title("Number of Anime Released Per Season")
ax1.set_xlabel("Year")
ax1.set_ylabel("Anime Count")
ax1.grid(True)
st.pyplot(fig1)

# Plotting average rating
st.subheader("⭐ Average Anime Score by Season")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_score, x='season', y='score', palette='viridis', ax=ax2)
ax2.set_title("Average Anime Score (Filtered)")
ax2.set_ylabel("Average Score")
st.pyplot(fig2)

# Plotting average popularity
st.subheader("Average Popularity Rank by Season (Lower is Better)")
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_popularity, x='season', y='popularity', palette='magma', ax=ax3)
ax3.set_title("Average Popularity Rank (Filtered)")
ax3.set_ylabel("Popularity Rank")
st.pyplot(fig3)

# Show table
with st.expander("🔍 View Filtered Data"):
    st.dataframe(filtered_df[['title', 'season', 'season_year', 'score', 'popularity']])