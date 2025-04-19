import pandas as pd
import streamlit as st
from collections import Counter
from itertools import combinations
import networkx as nx
from pyvis.network import Network
from streamlit.components.v1 import html

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv('./data/anime_cleaned.csv')
    df['genre'] = df['genre'].fillna('Unknown')
    df['genre'] = df['genre'].str.split(', ')
    return df

# Build graph from genre data
def build_genre_network(df, threshold=50):
    pair_counter = Counter()
    genre_counter = Counter()

    for genres in df['genre']:
        genre_counter.update(genres)
        if isinstance(genres, list) and len(genres) > 1:
            pairs = combinations(sorted(set(genres)), 2)
            pair_counter.update(pairs)

    G = nx.Graph()

    for genre, count in genre_counter.items():
        G.add_node(genre, size=count)

    for (g1, g2), weight in pair_counter.items():
        if weight >= threshold:
            G.add_edge(g1, g2, value=weight)

    return G

# Create and save interactive graph
def generate_pyvis_graph(G):
    net = Network(height="600px", width="100%", bgcolor="#1e1e1e", font_color="white", notebook=False)
    net.from_nx(G)

    for node in net.nodes:
        node['size'] = G.nodes[node['id']]['size'] * 0.2
        node['title'] = f"{node['id']} ({G.nodes[node['id']]['size']} shows)"
    
    for edge in net.edges:
        edge['title'] = f"Co-occurrences: {edge['value']}"
        edge['width'] = edge['value'] * 0.05

    net.repulsion(node_distance=120, spring_length=200)
    net.save_graph("genre_network.html")

# Streamlit app
def main():
    st.set_page_config(page_title="Anime Genre Network", layout="wide")
    st.title("🎭 Anime Genre Co-occurrence Network")
    st.markdown("Explore how different anime genres are frequently paired together using an interactive network.")

    df = load_data()

    threshold = st.slider("Minimum Co-occurrence Threshold", min_value=10, max_value=100, value=50, step=5)
    st.write(f"Showing genre pairs that occur together in at least **{threshold}** shows.")

    G = build_genre_network(df, threshold)
    generate_pyvis_graph(G)

    # Display the network
    with open("genre_network.html", "r", encoding="utf-8") as f:
        html_graph = f.read()
    html(html_graph, height=600, width=1000)

if __name__ == "__main__":
    main()
