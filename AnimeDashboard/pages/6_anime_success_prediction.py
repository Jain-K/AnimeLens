import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Setup
st.set_page_config(page_title="🎯 Anime Success Prediction", layout="wide")
st.title("🎯 Predicting Anime Success with Machine Learning")

@st.cache_data
def load_data():
    return pd.read_csv("./data/anime_cleaned.csv")

df_anime = load_data()

# Preprocessing
df_anime['successful'] = df_anime['score'] >= 7.5
df_anime['genre'] = df_anime['genre'].fillna('Unknown').str.split(', ')
genres_dummies = df_anime['genre'].explode().str.get_dummies().groupby(level=0).sum()

top_studios = df_anime['studio'].value_counts().nlargest(20).index
df_anime['studio'] = df_anime['studio'].where(df_anime['studio'].isin(top_studios), 'Other')
studio_dummies = pd.get_dummies(df_anime['studio'], prefix='studio')

features = pd.concat([
    df_anime[['episodes', 'duration_min', 'aired_from_year']].fillna(0),
    genres_dummies,
    studio_dummies
], axis=1)

labels = df_anime['successful']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Display Results
st.subheader("🧠 Classification Report")
report = classification_report(y_test, y_pred, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose())

st.subheader("📊 Confusion Matrix")
cm = confusion_matrix(y_test, y_pred)
fig_cm, ax_cm = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm)
st.pyplot(fig_cm)

# Feature Importance
st.subheader("💡 Top Feature Importances")
importances = pd.Series(clf.feature_importances_, index=features.columns)
top_importances = importances.nlargest(15)
fig_imp, ax_imp = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_importances.values, y=top_importances.index, ax=ax_imp)
st.pyplot(fig_imp)
