"""
╔══════════════════════════════════════════════════════════════╗
║     PERSONALIZED WORKOUT & DIET PLANNER — Streamlit App      ║
║     Full-stack AI application with ML model integration      ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from config import APP_CONFIG, STYLE_CONFIG
from model_loader import ModelLoader
from health_metrics import HealthMetrics
from planner import WorkoutPlanner, DietPlanner
from ui_components import (
    render_header,
    render_user_input_section,
    render_health_metrics_dashboard,
    render_workout_plan,
    render_diet_plan,
    render_calorie_visualization,
    render_explainability_section,
)

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Fitness Planner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject Custom CSS ────────────────────────────────────────────────────────
st.markdown(STYLE_CONFIG.CSS, unsafe_allow_html=True)


# ─── Load Models (cached) ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI models...")
def load_models():
    return ModelLoader()


# ─── Main Application ─────────────────────────────────────────────────────────
def main():
    models = load_models()

    render_header()

    # ── Sidebar: User Profile Input ──────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚡ Your Profile")
        st.markdown("---")
        user_data = render_user_input_section()
        generate_btn = st.button(
            "🚀 Generate My Plan", type="primary", use_container_width=True
        )

    # ── Main Content ─────────────────────────────────────────────────────────
    if not generate_btn and "plan_data" not in st.session_state:
        _render_landing()
        return

    if generate_btn:
        with st.spinner("🤖 Computing your personalized plan..."):
            plan_data = _compute_plan(user_data, models)
        st.session_state["plan_data"] = plan_data
        st.session_state["user_data"] = user_data

    if "plan_data" in st.session_state:
        plan_data = st.session_state["plan_data"]
        user_data = st.session_state["user_data"]

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Health Metrics", "🏋️ Workout Plan", "🥗 Diet Plan",
             "📈 Calorie Balance", "🧠 AI Insights"]
        )

        with tab1:
            render_health_metrics_dashboard(plan_data)
        with tab2:
            render_workout_plan(plan_data, user_data)
        with tab3:
            render_diet_plan(plan_data, user_data)
        with tab4:
            render_calorie_visualization(plan_data)
        with tab5:
            render_explainability_section(plan_data, user_data)


def _render_landing():
    st.markdown("""
    <div class="landing-hero">
        <h1 class="hero-title">AI-Powered Fitness Intelligence</h1>
        <p class="hero-sub">
            Fill in your profile on the left to generate a hyper-personalized
            workout & diet plan powered by machine learning.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("🧠", "ML Clustering", "K-Means fitness level prediction tailored to your biometrics"),
        ("🍽️", "Calorie AI", "Decision tree model predicts your exact daily calorie needs"),
        ("💬", "NLP Matching", "Sentence transformers match your preferences to curated plans"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)


def _compute_plan(user_data: dict, models: "ModelLoader") -> dict:
    """Central computation pipeline: metrics → models → plans."""

    # 1. Derived health metrics
    metrics = HealthMetrics(user_data)
    bmi = metrics.bmi()
    bmr = metrics.bmr()
    tdee = metrics.tdee()
    bmi_category = metrics.bmi_category()

    # 2. Predict fitness level cluster via KMeans
    # Features must match training exactly:
    # age, bmi,
    # activity_level_active, activity_level_light, activity_level_moderate,
    # activity_level_sedentary, activity_level_very active  (one-hot)
    activity = user_data["activity_level"]
    activity_ohe = {
        "activity_level_active":      1 if activity == "Very Active"        else 0,
        "activity_level_light":       1 if activity == "Lightly Active"     else 0,
        "activity_level_moderate":    1 if activity == "Moderately Active"  else 0,
        "activity_level_sedentary":   1 if activity == "Sedentary"          else 0,
        "activity_level_very active": 1 if activity == "Extremely Active"   else 0,
    }
    cluster_features = np.array([[
        user_data["age"],
        bmi,
        activity_ohe["activity_level_active"],
        activity_ohe["activity_level_light"],
        activity_ohe["activity_level_moderate"],
        activity_ohe["activity_level_sedentary"],
        activity_ohe["activity_level_very active"],
    ]])
    scaled_features = models.scale(cluster_features)
    fitness_cluster = models.predict_cluster(scaled_features)
    fitness_level = _cluster_to_fitness_level(fitness_cluster)

    # 3. Predict daily calories via DTR
    calorie_features = models.preprocess_calories({
        "age": user_data["age"],
        "gender": user_data["gender"],
        "height_cm": user_data["height_cm"],
        "weight_kg": user_data["weight_kg"],
        "activity_level": user_data["activity_level"],
        "fitness_goal": user_data["fitness_goal"],
        "bmi": bmi,
        "bmr": bmr,
        "tdee": tdee,
    })
    predicted_calories = models.predict_calories(calorie_features)

    # 4. Macro split based on goal
    macros = _compute_macros(predicted_calories, user_data["fitness_goal"])

    # 5. NLP embedding similarity (if free-text provided)
    embedding_notes = []
    if user_data.get("free_text_prefs"):
        embedding_notes = models.match_preferences(
            user_data["free_text_prefs"],
            fitness_level,
            user_data["fitness_goal"],
        )

    # 6. Generate plans
    workout_plan = WorkoutPlanner.generate(
        fitness_level=fitness_level,
        fitness_goal=user_data["fitness_goal"],
        available_equipment=user_data["available_equipment"],
        notes=embedding_notes,
    )

    diet_plan = DietPlanner.generate(
        daily_calories=predicted_calories,
        macros=macros,
        dietary_preference=user_data["dietary_preference"],
        cultural_food_habits=user_data["cultural_food_habits"],
        budget_usd=user_data["budget_usd_per_day"],
        notes=embedding_notes,
    )

    # 7. Calorie burn estimate
    weekly_burn = WorkoutPlanner.estimate_weekly_calorie_burn(
        fitness_level, user_data["fitness_goal"], user_data["weight_kg"]
    )

    return {
        "bmi": round(bmi, 2),
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "bmi_category": bmi_category,
        "fitness_cluster": int(fitness_cluster),
        "fitness_level": fitness_level,
        "predicted_calories": round(predicted_calories, 0),
        "macros": macros,
        "workout_plan": workout_plan,
        "diet_plan": diet_plan,
        "embedding_notes": embedding_notes,
        "weekly_burn": weekly_burn,
    }


def _cluster_to_fitness_level(cluster: int) -> str:
    mapping = {0: "Beginner", 1: "Intermediate", 2: "Advanced", 3: "Elite"}
    return mapping.get(cluster % 4, "Intermediate")


def _compute_macros(calories: float, goal: str) -> dict:
    splits = {
        "Weight Loss":       {"protein": 0.35, "carbs": 0.35, "fat": 0.30},
        "Muscle Gain":       {"protein": 0.30, "carbs": 0.45, "fat": 0.25},
        "Endurance":         {"protein": 0.20, "carbs": 0.55, "fat": 0.25},
        "General Fitness":   {"protein": 0.25, "carbs": 0.45, "fat": 0.30},
        "Maintenance":       {"protein": 0.25, "carbs": 0.45, "fat": 0.30},
    }
    split = splits.get(goal, splits["General Fitness"])
    return {
        "protein_g":  round((calories * split["protein"]) / 4, 1),
        "carbs_g":    round((calories * split["carbs"])   / 4, 1),
        "fat_g":      round((calories * split["fat"])     / 9, 1),
        "protein_pct": split["protein"],
        "carbs_pct":   split["carbs"],
        "fat_pct":     split["fat"],
    }


if __name__ == "__main__":
    main()
