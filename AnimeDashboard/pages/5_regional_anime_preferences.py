import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="🌍 Regional Anime Preferences", layout="wide")

# Title
st.title("📊 Regional Anime Preferences Analysis")

# Load Data
@st.cache_data
def load_data():
    df_users = pd.read_csv("./data/users_cleaned.csv")
    df_anime_lists = pd.read_csv("./data/animelists_cleaned.csv")
    df_anime = pd.read_csv("./data/anime_cleaned.csv")
    return df_users, df_anime_lists, df_anime

df_users, df_anime_lists, df_anime = load_data()

# Clean 'country' column
if 'location' in df_users.columns:
    df_users['country'] = df_users['location'].str.extract(r'([A-Za-z\s]+)$')[0]
    df_users['country'] = df_users['country'].fillna('Unknown').str.strip()
else:
    df_users['country'] = 'Unknown'


# Watchtime by Country
watchtime_region = df_users.groupby('country')['user_days_spent_watching'].sum().sort_values(ascending=False).head(15)

st.subheader("📺 Total Watch Time by Country")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=watchtime_region.values, y=watchtime_region.index, palette='rocket', ax=ax1)
ax1.set_title("Total Days Spent Watching Anime (Top 15 Countries)")
st.pyplot(fig1)

# Merge to get genre-region popularity
merged = pd.merge(df_anime_lists, df_users[['username', 'country']], on='username', how='left')
merged = pd.merge(merged, df_anime[['anime_id', 'genre']], on='anime_id', how='left')
sample = merged.sample(10000, random_state=42)
sample['genre'] = sample['genre'].fillna('Unknown').str.split(', ')
sample = sample.explode('genre')

genre_region = sample.groupby(['country', 'genre']).size().reset_index(name='count')
top_regions = genre_region.groupby('country')['count'].sum().sort_values(ascending=False).head(10).index
genre_region_top = genre_region[genre_region['country'].isin(top_regions)]
heatmap_data = genre_region_top.pivot_table(index='genre', columns='country', values='count', fill_value=0)

st.subheader("🔥 Genre Popularity Heatmap (Top 10 Countries)")
fig2, ax2 = plt.subplots(figsize=(14, 10))
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.5, ax=ax2)
st.pyplot(fig2)
