import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit layout
st.set_page_config(layout="wide")

st.title("📈 Anime Genre Popularity Over Time")
st.markdown("Explore how different anime genres have evolved in popularity based on release years.")

# Upload dataset

df = pd.read_csv("./data/anime_cleaned.csv")

# Preprocessing
df = df.dropna(subset=['aired_from_year', 'genre'])
df['aired_from_year'] = df['aired_from_year'].astype(int)
df['genre'] = df['genre'].str.split(', ')  # Adjust if necessary

# Explode genres
df_exploded = df.explode('genre')

# Sidebar filters
min_year, max_year = int(df_exploded['aired_from_year'].min()), int(df_exploded['aired_from_year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

unique_genres = sorted(df_exploded['genre'].dropna().unique())
selected_genres = st.sidebar.multiselect("Select Genres", unique_genres, default=["Action", "Romance", "Slice of Life"])

# Filter data
filtered = df_exploded[
    (df_exploded['aired_from_year'] >= year_range[0]) &
    (df_exploded['aired_from_year'] <= year_range[1]) &
    (df_exploded['genre'].isin(selected_genres))
]

# Group and aggregate
genre_trend = (
    filtered.groupby(['aired_from_year', 'genre'])['title']
    .count()
    .reset_index()
    .rename(columns={'title': 'count'})
)

# Visualization
plt.figure(figsize=(14, 7))
sns.lineplot(data=genre_trend, x='aired_from_year', y='count', hue='genre', marker='o')
plt.title('Anime Genre Popularity Over Time', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Number of Anime Released')
plt.grid(True)
plt.legend(title='Genre')
st.pyplot(plt)

# Optional: display data
with st.expander("📊 Show Data Table"):
    st.dataframe(genre_trend)


# Extract and process
df = df.dropna(subset=['premiered', 'score', 'popularity'])
df[['season', 'season_year']] = df['premiered'].str.split(' ', expand=True)
df['season_year'] = df['season_year'].astype(int)

# Grouping
release_dist = df.groupby(['season_year', 'season'])['title'].count().reset_index().rename(columns={'title': 'anime_count'})

# Visualization
st.subheader("📅 Seasonal Anime Releases Over Years")
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(data=release_dist, x='season_year', y='anime_count', hue='season', marker='o', ax=ax)
plt.title("Number of Anime Released Per Season Over Time")
st.pyplot(fig)
    