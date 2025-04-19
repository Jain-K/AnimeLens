import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import networkx as nx

# Load data
st.set_page_config(layout="wide")
st.title("🎥 Anime Studio Insights Dashboard")
df_anime = pd.read_csv("./data/anime_cleaned.csv")

# Preprocess genre-studio data
df_genre_studio = df_anime[['studio', 'genre']].dropna()
df_genre_studio['genre'] = df_genre_studio['genre'].str.split(',')
df_genre_studio = df_genre_studio.explode('genre')
df_genre_studio['genre'] = df_genre_studio['genre'].str.strip()
df_genre_studio['studio'] = df_genre_studio['studio'].str.strip()

studio_genre_counts = df_genre_studio.groupby(['genre', 'studio']).size().reset_index(name='count')

# Section: Top studios by genre
st.header("🏆 Top Studios by Genre")
top_n = st.slider("Select Top N Studios per Genre", 1, 10, 3)

top_studios_by_genre = studio_genre_counts.sort_values(['genre', 'count'], ascending=[True, False])
top_studios = top_studios_by_genre.groupby('genre').head(top_n)

st.subheader("📊 Faceted Barplot (Top Studios by Genre)")
genres = st.multiselect("Pick genres to show:", sorted(top_studios['genre'].unique()), default=['Action', 'Romance', 'Comedy'])
filtered = top_studios[top_studios['genre'].isin(genres)]

g = sns.FacetGrid(filtered, col="genre", col_wrap=3, sharex=False, height=4)
g.map_dataframe(sns.barplot, y="studio", x="count", palette="Set2")
g.set_titles("{col_name}")
g.set_axis_labels("Anime Count", "Studio")
st.pyplot(g.fig)

# Section: Heatmap
st.header("🔥 Heatmap: Anime Counts by Studio and Genre")
heatmap_data = studio_genre_counts.pivot(index='studio', columns='genre', values='count').fillna(0)
top_heatmap_studios = heatmap_data.sum(axis=1).sort_values(ascending=False).head(10).index
heatmap_data = heatmap_data.loc[top_heatmap_studios]

plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Top 10 Studios: Genre Spread")
st.pyplot(plt.gcf())

# Section: Sunburst & Treemap
st.header("🌞 Sunburst & Treemap Visualizations")
sunburst_df = studio_genre_counts[studio_genre_counts['count'] > 2]

tab1, tab2 = st.tabs(["Sunburst Chart", "Treemap"])
with tab1:
    fig = px.sunburst(sunburst_df, path=['genre', 'studio'], values='count', color='genre',
                      title='Sunburst: Genres → Studios')
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    fig = px.treemap(sunburst_df, path=['genre', 'studio'], values='count',
                     title='Treemap: Studio Dominance by Genre')
    st.plotly_chart(fig, use_container_width=True)

# Section: NetworkX Graph
st.header("🔗 Studio–Genre Relationship Network")
G = nx.Graph()
for _, row in studio_genre_counts.iterrows():
    G.add_edge(row['genre'], row['studio'], weight=row['count'])

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.35)
nx.draw(G, pos, with_labels=True, node_size=1000, font_size=8, edge_color='gray', node_color='skyblue')
st.pyplot(plt.gcf())

# Section: Studio Scores
st.header("🏅 Studios with Consistently High Scores")
df_scores = df_anime[['studio', 'score']].dropna()
df_scores['studio'] = df_scores['studio'].str.strip()

studio_scores = df_scores.groupby('studio').agg(
    avg_score=('score', 'mean'),
    anime_count=('score', 'count')
).reset_index()

min_anime = st.slider("Minimum Anime to Consider", 1, 20, 5)
studio_scores = studio_scores[studio_scores['anime_count'] >= min_anime]
top_studios_by_score = studio_scores.sort_values('avg_score', ascending=False).head(10)

st.subheader("🎯 Top 10 Studios by Average Score")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_studios_by_score, y='studio', x='avg_score', palette='viridis', ax=ax)
ax.set_title("Top Studios by Score")
st.pyplot(fig)

# Violin + Swarm Plot
st.subheader("🎻 Score Distribution of Top 10 Most Productive Studios")
top_studios = df_anime['studio'].value_counts().head(10).index
df_top = df_anime[df_anime['studio'].isin(top_studios)]

fig, ax = plt.subplots(figsize=(12, 6))
sns.violinplot(data=df_top, x='studio', y='score', inner=None, palette='Spectral', ax=ax)
sns.swarmplot(data=df_top, x='studio', y='score', size=3, color='k', alpha=0.5, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Bubble Plot: Quality vs Quantity
st.subheader("🫧 Studio Productivity vs Quality")
studio_stats = df_anime.groupby('studio').agg({'score': 'mean', 'anime_id': 'count'}).rename(
    columns={'anime_id': 'anime_count'}).reset_index()
top_studio_stats = studio_stats[studio_stats['anime_count'] > 10]

fig = px.scatter(
    top_studio_stats,
    x='anime_count',
    y='score',
    size='anime_count',
    color='score',
    hover_name='studio',
    title='Bubble Plot: Productivity vs Quality',
    size_max=40
)
st.plotly_chart(fig, use_container_width=True)

# Studio Score Over Years
st.header("📈 Studio Score Trends Over Time")
df_anime['aired_from_year'] = pd.to_numeric(df_anime['aired_from_year'], errors='coerce')
pivot = df_anime.pivot_table(values='score', index='studio', columns='aired_from_year', aggfunc='mean')
pivot = pivot.dropna(thresh=5)

top_studios = pivot.mean(axis=1).sort_values(ascending=False).head(10).index
pivot_top = pivot.loc[top_studios]

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot_top, annot=True, fmt=".1f", cmap='YlGnBu', linewidths=0.5, cbar_kws={'label': 'Average Score'})
plt.title("Top Anime Studios by Average Score Over the Years", fontsize=14)
st.pyplot(fig)
