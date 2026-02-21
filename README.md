# 🏋️‍♂️ AI-Powered Personalized Workout & Diet Plan Generator

An intelligent, AI-driven web application that generates **personalized
workout and diet plans** based on user-specific health metrics, fitness
goals, cultural food habits, budget constraints, and available
equipment.

Built using **Machine Learning + Streamlit**, this system combines
clustering, regression modeling, and NLP-based personalization to
deliver customized fitness guidance.

------------------------------------------------------------------------

## 🚀 Live Demo

🔗 Streamlit App:\
https://workout-and-diet-plan-generator.streamlit.app/

------------------------------------------------------------------------

## 🎯 Project Objective

Most fitness applications provide generic plans that do not adapt to:

-   Individual health parameters\
-   Cultural dietary preferences\
-   Budget constraints\
-   Available workout equipment\
-   Fitness level

This project solves that problem by using **machine learning models** to
generate tailored plans for each user.

------------------------------------------------------------------------

## 📁 Project Structure

```
workout_diet_planner/
├── app.py                  ← Main Streamlit entry point
├── config.py               ← App settings & custom CSS
├── model_loader.py         ← Loads all 5 .pkl models with graceful fallback stubs
├── health_metrics.py       ← BMI, BMR, TDEE computations
├── planner.py              ← Workout & diet plan generators
├── ui_components.py        ← All Streamlit rendering functions (tabbed UI)
├── requirements.txt        ← Python dependencies
├── .streamlit/
│   └── config.toml         ← Streamlit Cloud deployment config
│
└── [Your model files here]:
    ├── scaler.pkl
    ├── kmeans_model.pkl
    ├── calorie_preprocessor.pkl
    ├── dtr_model.pkl
    └── sentence_transformer_model.pkl
```

---

## 🤖 ML Model Integration

| Model File | Usage |
|---|---|
| `scaler.pkl` | StandardScaler/MinMaxScaler applied to `[age, gender, height, weight, BMI, BMR, TDEE, activity_level]` before KMeans |
| `kmeans_model.pkl` | Predicts fitness level cluster (0–3 → Beginner/Intermediate/Advanced/Elite) |
| `calorie_preprocessor.pkl` | ColumnTransformer/Pipeline that encodes categoricals and scales numerics before DTR |
| `dtr_model.pkl` | Decision Tree Regressor predicting daily calorie requirement |
| `sentence_transformer_model.pkl` | SentenceTransformer that embeds free-text preferences; cosine similarity to 18-candidate bank |

**Demo mode:** If any `.pkl` file is absent, a mathematically equivalent stub is used automatically and a sidebar warning is shown.

---

## 🔬 Computation Pipeline

```
User Inputs
    │
    ▼
Health Metrics (BMI, BMR, TDEE)  [health_metrics.py]
    │
    ├─► scaler.pkl → kmeans_model.pkl → fitness_level cluster
    │
    ├─► calorie_preprocessor.pkl → dtr_model.pkl → predicted_calories
    │
    ├─► sentence_transformer_model.pkl → cosine similarity → NLP notes
    │
    └─► WorkoutPlanner + DietPlanner → 7-day plans
```

---

## 🖥️ UI Sections

| Tab | Content |
|---|---|
| 📊 Health Metrics | BMI/BMR/TDEE cards, macro donut chart, fitness level badge |
| 🏋️ Workout Plan | 7-day exercise cards with sets/reps/muscle groups |
| 🥗 Diet Plan | Day-selector meal cards + weekly overview table |
| 📈 Calorie Balance | TDEE vs predicted vs net-after-workout charts |
| 🧠 AI Insights | Model pipeline explainability, macro rationale, JSON export |

---

## 🚀 Running Locally

```bash
# 1. Clone / copy files to a folder
cd workout_diet_planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place your .pkl model files in the same directory as app.py

# 4. Launch
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Set **Main file path** to `app.py`.
4. Add model files via **Streamlit Secrets** or upload to the repo directly.
5. Click **Deploy** — the `.streamlit/config.toml` handles theming automatically.

---

## 🔧 Customisation

**Adding new exercises:** Edit `EXERCISE_DB` dict in `planner.py`.

**Adding new food items:** Edit `FOOD_DB` dict in `planner.py`.

**Changing model input features:** Update `_compute_plan()` in `app.py` and the
`preprocess_calories()` call in `model_loader.py`.

**Supporting more KMeans clusters:** Extend `_cluster_to_fitness_level()` in `app.py`.

---

## 📦 Input Variables Expected by Models

### scaler.pkl → kmeans_model.pkl
```
[age, gender_enc(0/1), height_cm, weight_kg, bmi, bmr, tdee, activity_level_enc(0–4)]
```

### calorie_preprocessor.pkl → dtr_model.pkl
```python
pd.DataFrame([{
    "age": int, "gender": str, "height_cm": float, "weight_kg": float,
    "activity_level": str, "fitness_goal": str,
    "bmi": float, "bmr": float, "tdee": float
}])
```
The preprocessor handles all encoding internally.

### sentence_transformer_model.pkl
```python
model.encode(["free text string"])  # returns (1, embedding_dim) array
```

---

*Built with Streamlit · scikit-learn · Plotly · Sentence Transformers*


## 💡 Key Features

✔ Personalized workout plans\
✔ Budget-aware diet plans\
✔ Cultural dietary adaptability\
✔ Equipment-based workout filtering\
✔ Machine learning-driven calorie estimation\
✔ NLP-based personalization\
✔ Interactive dashboard

------------------------------------------------------------------------

## 📈 Future Enhancements

-   🔄 Progress tracking system\
-   📱 Mobile optimization\
-   📊 User history storage\
-   🤖 Chat-based AI fitness assistant\
-   🧬 Integration with wearable devices

------------------------------------------------------------------------

## 👨‍💻 Author

**Harrish Devaraj**\
AI & Machine Learning Enthusiast

GitHub:\
https://github.com/Harrishdevaraj21

------------------------------------------------------------------------

## 📜 License

This project is developed for academic and demonstration purposes.

