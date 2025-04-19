import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Anime EDA Dashboard", layout="wide")

st.title("📊 Anime Episode Analysis Dashboard")


df_anime = pd.read_csv("./data/anime_cleaned.csv")

# Data Cleaning
df_anime['episodes'] = pd.to_numeric(df_anime['episodes'], errors='coerce')
df_anime['popularity'] = pd.to_numeric(df_anime['popularity'], errors='coerce')
df_anime['score'] = pd.to_numeric(df_anime['score'], errors='coerce')

# Episode Count vs Popularity
df_pop = df_anime.dropna(subset=['episodes', 'popularity'])

st.subheader("📈 Episode Count vs Popularity")

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_pop, x='episodes', y='popularity', alpha=0.6, color='blue', ax=ax1)
sns.regplot(data=df_pop, x='episodes', y='popularity', scatter=False, color='red', ax=ax1)
ax1.set_title("Episode Count vs Popularity")
ax1.set_xlabel("Number of Episodes")
ax1.set_ylabel("Popularity")
st.pyplot(fig1)

# Episode Count vs Rating
df_rating = df_anime.dropna(subset=['episodes', 'score'])

st.subheader("⭐ Episode Count vs Rating")

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_rating, x='episodes', y='score', alpha=0.6, color='green', ax=ax2)
sns.regplot(data=df_rating, x='episodes', y='score', scatter=False, color='orange', ax=ax2)
ax2.set_title("Episode Count vs Rating")
ax2.set_xlabel("Number of Episodes")
ax2.set_ylabel("Average Rating")
st.pyplot(fig2)

# Boxplot: Episode Length vs Rating
bins = [0, 12, 24, 50, 200]
labels = ['Short', 'Medium', 'Long', 'Very Long']
df_rating['episode_bin'] = pd.cut(df_rating['episodes'], bins=bins, labels=labels)

st.subheader("📦 Boxplot: Episode Length vs Rating")

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_rating, x='episode_bin', y='score', palette='viridis', ax=ax3)
ax3.set_title("Episode Length vs Rating")
ax3.set_xlabel("Episode Length")
ax3.set_ylabel("Average Rating")
st.pyplot(fig3)

# Show correlations
corr_popularity = df_pop['episodes'].corr(df_pop['popularity'])
corr_rating = df_rating['episodes'].corr(df_rating['score'])

st.subheader("📌 Correlation Insights")
st.markdown(f"- **Correlation between Episode Count and Popularity**: `{corr_popularity:.2f}`")
st.markdown(f"- **Correlation between Episode Count and Rating**: `{corr_rating:.2f}`")


