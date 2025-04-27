# AnimeLens: Interactive Anime Data Analytics Dashboard

**AnimeLens** is an interactive dashboard for exploring anime trends, genres, studios, regional preferences, and success prediction, powered by Streamlit and advanced data visualization.

 **Deployed Link:** https://vedantadlak-anime-lens-home-vakjge.streamlit.app

---

## 🚀 Features

- **Genre Trends:** Visualize popularity of anime genres over time.
- **Seasonal Patterns:** Analyze how anime releases and ratings vary by season.
- **Studio Specialization:** Explore which studios excel in which genres.
- **Episode Analysis:** Understand how episode count relates to popularity and ratings.
- **Regional Preferences:** Discover how anime tastes differ across countries and regions.
- **Success Prediction:** Predict anime success using machine learning.
- **Genre Co-occurrence Network:** See how genres blend together in anime storytelling.

---

## 🛠️ Setup Instructions

1. **Clone the repository:**
    ```
    git clone https://github.com/Jain-K/AnimeLens/tree/master
    cd AnimeLens
    python3 -m venv anime
    source anime/bin/activate
    cd AnimeDashboard
    ```
2. **Make Virtual Environment:**
    ```
    cd AnimeLens
    python3 -m venv anime
    source anime/bin/activate
    cd AnimeDashboard
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Download Data:**
      - **Important:** The file `animelists_cleaned.csv` is very large and **cannot be stored on GitHub**.
      - **Download it from Kaggle:**  
        [MyAnimeList Dataset on Kaggle](https://www.kaggle.com/datasets/azathoth42/myanimelist?select=animelists_cleaned.csv)
      - Place it in: `AnimeDashboard/data/animelists_cleaned.csv`

4. **Run the app:**
    ```
    streamlit run Home.py
    ```

---

## ⚠️ Note about `animelists_cleaned.csv`

- The file `animelists_cleaned.csv` is **very large** (multiple GB).Hence it can not uploaded on Github
- Instead, download it directly from Kaggle:  
  [https://www.kaggle.com/datasets/azathoth42/myanimelist?select=animelists_cleaned.csv](https://www.kaggle.com/datasets/azathoth42/myanimelist?select=animelists_cleaned.csv)
- Place it in the `AnimeDashboard/data` folder before running the app.
- This is required for the **5_Regional_Anime_Preferences** page.

---

## 💡 Usage

- Launch the app with `streamlit run Home.py`
- Use the left sidebar to navigate between dashboard sections.
- Interact with filters, sliders, and dropdowns for custom analytics.
- Download processed data from within the app as needed.

---

## 📢 Acknowledgements

- [MyAnimeList Dataset on Kaggle](https://www.kaggle.com/datasets/azathoth42/myanimelist)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)

---


