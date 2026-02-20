"""ui_components.py — All Streamlit rendering functions."""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

from health_metrics import ACTIVITY_MULTIPLIERS

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#e8e8f0"),
    margin=dict(l=20, r=20, t=40, b=20),
)

ACCENT_GREEN  = "#00ff88"
ACCENT_ORANGE = "#ff6b35"
ACCENT_BLUE   = "#4d9fff"


# ─── Header ───────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="app-header">
        <div class="app-title">⚡ AI FITNESS PLANNER</div>
        <div class="app-tagline">MACHINE LEARNING · PERSONALIZATION · PERFORMANCE</div>
    </div>
    """, unsafe_allow_html=True)


# ─── User Input ───────────────────────────────────────────────────────────────
def render_user_input_section() -> dict:
    age    = st.slider("Age", 16, 80, 28, help="Your current age in years")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", 140, 230, 170, step=1)
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, step=0.5)

    st.markdown("---")

    activity = st.selectbox(
        "Activity Level",
        list(ACTIVITY_MULTIPLIERS.keys()),
        index=2,
        help="Current weekly activity excluding planned workouts",
    )
    fitness_goal = st.selectbox(
        "Fitness Goal",
        ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness", "Maintenance"],
        index=0,
    )
    dietary_pref = st.selectbox(
        "Dietary Preference",
        ["Non-Vegetarian", "Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo"],
    )
    cultural_food = st.selectbox(
        "Cultural Food Habits",
        ["South Asian (Indian/Pakistani/Sri Lankan)", "East Asian (Chinese/Japanese/Korean)",
         "Southeast Asian (Thai/Vietnamese/Filipino)", "Middle Eastern",
         "Western (European/American)", "Latin American", "African"],
        index=4,
    )

    st.markdown("---")

    budget = st.number_input("Daily Food Budget (USD $)", 2.0, 50.0, 10.0, step=0.5)
    equipment = st.multiselect(
        "Available Equipment",
        ["Bodyweight", "Dumbbells", "Barbell", "Resistance Bands",
         "Machines", "Pull-up Bar", "Kettlebell"],
        default=["Bodyweight", "Dumbbells"],
    )
    if not equipment:
        equipment = ["Bodyweight"]

    st.markdown("---")

    free_text = st.text_area(
        "Preferences / Injuries / Notes (optional)",
        placeholder="e.g. bad left knee, love spicy food, prefer morning workouts...",
        height=80,
        help="AI will use NLP to incorporate these into your plan",
    )

    # Activity level encoded for model
    activity_map = {k: i for i, k in enumerate(ACTIVITY_MULTIPLIERS.keys())}
    goal_map     = {"Weight Loss": 0, "Muscle Gain": 1, "Endurance": 2,
                    "General Fitness": 3, "Maintenance": 4}

    return {
        "age":                    age,
        "gender":                 gender,
        "height_cm":              height,
        "weight_kg":              weight,
        "activity_level":         activity,
        "activity_level_encoded": activity_map.get(activity, 2),
        "fitness_goal":           fitness_goal,
        "fitness_goal_encoded":   goal_map.get(fitness_goal, 3),
        "dietary_preference":     dietary_pref,
        "cultural_food_habits":   cultural_food,
        "budget_usd_per_day":     budget,
        "available_equipment":    equipment,
        "free_text_prefs":        free_text.strip() if free_text.strip() else None,
    }


# ─── Health Metrics Dashboard ─────────────────────────────────────────────────
def render_health_metrics_dashboard(plan: dict):
    st.markdown('<div class="section-header">📊 Health Metrics Dashboard</div>',
                unsafe_allow_html=True)

    bmi_cat = plan["bmi_category"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BMI</div>
            <div class="metric-value">{plan['bmi']}</div>
            <div class="metric-unit">{bmi_cat['emoji']} {bmi_cat['label']}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-label">BMR</div>
            <div class="metric-value orange">{plan['bmr']:.0f}</div>
            <div class="metric-unit">kcal / day (at rest)</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card blue">
            <div class="metric-label">TDEE</div>
            <div class="metric-value blue">{plan['tdee']:.0f}</div>
            <div class="metric-unit">kcal / day (total expenditure)</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Predicted Calories</div>
            <div class="metric-value">{plan['predicted_calories']:.0f}</div>
            <div class="metric-unit">kcal / day (AI model)</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown(f"""
        <div class="info-box">
            🏋️ <b>AI Fitness Level:</b>
            <span class="fitness-badge">{plan['fitness_level']}</span>
            &nbsp; (K-Means Cluster {plan['fitness_cluster']})
        </div>""", unsafe_allow_html=True)

        # Macro donut
        macros = plan["macros"]
        fig = go.Figure(go.Pie(
            labels=["Protein", "Carbs", "Fat"],
            values=[macros["protein_pct"], macros["carbs_pct"], macros["fat_pct"]],
            hole=0.65,
            marker=dict(colors=[ACCENT_GREEN, ACCENT_BLUE, ACCENT_ORANGE],
                        line=dict(color="#0a0a0f", width=2)),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>%{value*100:.0f}%<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Macro Split", font=dict(size=14, color="#6b6b8a")),
            showlegend=False,
            height=260,
            annotations=[dict(text=f"{plan['predicted_calories']:.0f}<br>kcal",
                              x=0.5, y=0.5, showarrow=False,
                              font=dict(size=16, color=ACCENT_GREEN))],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Macro grams bar chart
        macro_df = pd.DataFrame({
            "Macro":   ["Protein", "Carbs", "Fat"],
            "Grams":   [macros["protein_g"], macros["carbs_g"], macros["fat_g"]],
            "Calories":[macros["protein_g"]*4, macros["carbs_g"]*4, macros["fat_g"]*9],
        })
        fig2 = go.Figure()
        colors = [ACCENT_GREEN, ACCENT_BLUE, ACCENT_ORANGE]
        for i, row in macro_df.iterrows():
            fig2.add_trace(go.Bar(
                name=row["Macro"], x=[row["Macro"]], y=[row["Grams"]],
                marker_color=colors[i],
                text=[f"{row['Grams']}g<br>({row['Calories']:.0f} kcal)"],
                textposition="inside",
                textfont=dict(color="#0a0a0f", size=11),
            ))
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            showlegend=False,
            barmode="group",
            title=dict(text="Daily Macros (grams)", font=dict(size=14, color="#6b6b8a")),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#2a2a3d", title="Grams"),
            height=260,
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─── Workout Plan ─────────────────────────────────────────────────────────────
def render_workout_plan(plan: dict, user_data: dict):
    st.markdown('<div class="section-header">🏋️ Weekly Workout Plan</div>',
                unsafe_allow_html=True)

    col_info, col_badge = st.columns([3, 1])
    with col_info:
        st.markdown(f"""
        <div class="info-box">
            Plan tailored for <b>{plan['fitness_level']}</b> fitness level ·
            Goal: <b>{user_data['fitness_goal']}</b> ·
            Equipment: {', '.join(user_data['available_equipment'])}
        </div>""", unsafe_allow_html=True)
    with col_badge:
        est_burn = plan.get("weekly_burn", 0)
        st.metric("Est. Weekly Burn", f"{est_burn:.0f} kcal")

    if plan.get("embedding_notes"):
        st.markdown("**🧠 NLP Personalization Applied:**")
        for note in plan["embedding_notes"]:
            st.markdown(f'<div class="nlp-note">★ {note}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, day_data in enumerate(plan["workout_plan"]):
        with cols[i % 2]:
            if day_data["type"] == "rest":
                st.markdown(f"""
                <div class="day-card" style="opacity:0.6;">
                    <div class="day-title">🛌 {day_data['day']} — {day_data['focus']}</div>
                    <div style="color:var(--text-muted);font-size:0.88rem;">{day_data['notes']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                ex_html = "".join([
                    f'<div class="exercise-row">'
                    f'  <span class="ex-name">→ {ex["name"]}</span>'
                    f'  <span class="ex-sets">{ex["sets"]}</span>'
                    f'  <span class="ex-muscle">{ex["muscle"]}</span>'
                    f'</div>'
                    for ex in day_data["exercises"]
                ])
                st.markdown(f"""
                <div class="day-card">
                    <div class="day-title">⚡ {day_data['day']} — {day_data['focus']}
                        <span style="float:right;font-size:0.75rem;color:var(--text-muted);">
                            ~{day_data['duration_min']} min
                        </span>
                    </div>
                    {ex_html}
                    <div style="margin-top:0.8rem;font-size:0.80rem;color:var(--text-muted);">
                        💡 {day_data['notes']}
                    </div>
                </div>""", unsafe_allow_html=True)


# ─── Diet Plan ────────────────────────────────────────────────────────────────
def render_diet_plan(plan: dict, user_data: dict):
    st.markdown('<div class="section-header">🥗 Weekly Diet Plan</div>',
                unsafe_allow_html=True)

    diet = plan["diet_plan"]

    col_info, col_budget = st.columns([3, 1])
    with col_info:
        st.markdown(f"""
        <div class="info-box">
            {user_data['dietary_preference']} · {user_data['cultural_food_habits']} ·
            Budget: <b>${user_data['budget_usd_per_day']:.2f}/day</b>
        </div>""", unsafe_allow_html=True)
    with col_budget:
        daily_cost = sum(m["cost"] for m in diet["weekly_plan"][0]["meals"])
        st.metric("Est. Daily Cost", f"${daily_cost:.2f}", delta=None)

    if diet.get("nlp_adjustment"):
        st.markdown(f'<div class="nlp-note">🍽️ Dietary Adjustment: {diet["nlp_adjustment"]}</div>',
                    unsafe_allow_html=True)

    # Day selector
    selected_day = st.select_slider(
        "View Day", options=[d["day"] for d in diet["weekly_plan"]], value="Monday"
    )

    day_plan = next(d for d in diet["weekly_plan"] if d["day"] == selected_day)
    st.markdown(f"<br>**📅 {selected_day}**", unsafe_allow_html=True)

    meal_cols = st.columns(len(day_plan["meals"]))
    for col, meal in zip(meal_cols, day_plan["meals"]):
        with col:
            st.markdown(f"""
            <div class="meal-card">
                <div class="meal-title">{meal['name']}
                    <span class="meal-calories">{meal['calories']} kcal</span>
                </div>
                <div style="font-size:0.88rem;margin-top:0.8rem;color:var(--text);">{meal['item']}</div>
                <div style="margin-top:0.8rem;font-size:0.78rem;color:var(--text-muted);">
                    🥩 {meal['protein']}g protein &nbsp;
                    🍞 {meal['carbs']}g carbs &nbsp;
                    🧴 {meal['fat']}g fat
                </div>
            </div>""", unsafe_allow_html=True)

    # Weekly overview table
    st.markdown("<br>**📊 Weekly Meal Overview**", unsafe_allow_html=True)
    rows = []
    for day_data in diet["weekly_plan"]:
        for meal in day_data["meals"]:
            rows.append({
                "Day":      day_data["day"],
                "Meal":     meal["name"],
                "Item":     meal["item"],
                "Calories": meal["calories"],
                "Protein":  f"{meal['protein']}g",
                "Carbs":    f"{meal['carbs']}g",
                "Fat":      f"{meal['fat']}g",
                "Cost ($)": f"${meal['cost']:.2f}",
            })
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Calories": st.column_config.NumberColumn(format="%d kcal"),
        }
    )


# ─── Calorie Balance Visualization ────────────────────────────────────────────
def render_calorie_visualization(plan: dict):
    st.markdown('<div class="section-header">📈 Calorie Balance Analysis</div>',
                unsafe_allow_html=True)

    tdee        = plan["tdee"]
    predicted   = plan["predicted_calories"]
    weekly_burn = plan.get("weekly_burn", 0)
    daily_burn  = weekly_burn / 7

    net_balance = predicted - tdee
    balance_label = "Surplus" if net_balance > 0 else "Deficit"
    balance_color = ACCENT_GREEN if net_balance > 50 else (ACCENT_ORANGE if net_balance < -50 else ACCENT_BLUE)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TDEE",              f"{tdee:.0f} kcal",      help="Total Daily Energy Expenditure")
    c2.metric("Target Calories",   f"{predicted:.0f} kcal", help="AI model prediction")
    c3.metric("Workout Burn/day",  f"{daily_burn:.0f} kcal", help="Estimated from workout plan")
    c4.metric(f"Daily {balance_label}", f"{abs(net_balance):.0f} kcal",
              delta=f"{net_balance:+.0f}", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        # Grouped bar: TDEE vs Target vs Net-after-workout
        categories = ["TDEE", "Target Intake", "Net After Workout"]
        values     = [tdee, predicted, predicted - daily_burn]
        colors     = [ACCENT_ORANGE, ACCENT_GREEN, ACCENT_BLUE]
        fig = go.Figure(go.Bar(
            x=categories, y=values,
            marker_color=colors,
            text=[f"{v:.0f}" for v in values],
            textposition="outside",
            textfont=dict(color="#e8e8f0"),
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Calorie Comparison",
            yaxis=dict(showgrid=True, gridcolor="#2a2a3d"),
            xaxis=dict(showgrid=False),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Weekly accumulation line chart
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        burns = []
        cum_net = 0
        cum_nets = []
        for i, day in enumerate(plan.get("workout_plan", [])):
            b = daily_burn * 1.5 if day.get("type") == "workout" else daily_burn * 0.3
            burns.append(b)
            cum_net += (predicted - tdee - b)
            cum_nets.append(cum_net)

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(
            x=days, y=burns, name="Workout Burn",
            marker_color=ACCENT_ORANGE, opacity=0.7
        ), secondary_y=False)
        fig2.add_trace(go.Scatter(
            x=days, y=cum_nets, name="Cumulative Balance",
            mode="lines+markers", line=dict(color=ACCENT_GREEN, width=2.5),
            marker=dict(size=7),
        ), secondary_y=True)
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            title="Weekly Burn & Cumulative Balance",
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)"),
            height=320,
        )
        fig2.update_yaxes(title_text="Burn (kcal)", secondary_y=False,
                          gridcolor="#2a2a3d")
        fig2.update_yaxes(title_text="Cumulative (kcal)", secondary_y=True,
                          showgrid=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Macro energy waterfall
    macros = plan["macros"]
    protein_cal = macros["protein_g"] * 4
    carbs_cal   = macros["carbs_g"]   * 4
    fat_cal     = macros["fat_g"]     * 9
    total        = protein_cal + carbs_cal + fat_cal

    fig3 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Protein", "Carbs", "Fat", "Total"],
        y=[protein_cal, carbs_cal, fat_cal, 0],
        text=[f"{protein_cal:.0f}", f"+{carbs_cal:.0f}", f"+{fat_cal:.0f}", f"{total:.0f}"],
        textposition="outside",
        connector=dict(line=dict(color="#2a2a3d")),
        increasing=dict(marker=dict(color=ACCENT_GREEN)),
        decreasing=dict(marker=dict(color=ACCENT_ORANGE)),
        totals=dict(marker=dict(color=ACCENT_BLUE)),
    ))
    fig3.update_layout(
        **PLOTLY_LAYOUT,
        title="Calories by Macronutrient",
        yaxis=dict(showgrid=True, gridcolor="#2a2a3d"),
        height=280,
    )
    st.plotly_chart(fig3, use_container_width=True)


# ─── Explainability / AI Insights ─────────────────────────────────────────────
def render_explainability_section(plan: dict, user_data: dict):
    st.markdown('<div class="section-header">🧠 AI Insights & Explainability</div>',
                unsafe_allow_html=True)

    # Model pipeline explanation
    st.markdown("### How Your Plan Was Generated")
    pipeline_steps = [
        ("1️⃣ BMI / BMR / TDEE", "Harris-Benedict equations applied to your biometrics",
         f"BMI={plan['bmi']}, BMR={plan['bmr']:.0f} kcal, TDEE={plan['tdee']:.0f} kcal"),
        ("2️⃣ Fitness Cluster", "scaler.pkl → kmeans_model.pkl predict()",
         f"Cluster {plan['fitness_cluster']} → **{plan['fitness_level']}** fitness level"),
        ("3️⃣ Calorie Prediction", "calorie_preprocessor.pkl → dtr_model.pkl predict()",
         f"Predicted {plan['predicted_calories']:.0f} kcal/day based on {user_data['fitness_goal']} goal"),
        ("4️⃣ NLP Matching", "sentence_transformer_model.pkl encode() → cosine similarity",
         f"{len(plan.get('embedding_notes', []))} personalization notes applied from your preferences"),
        ("5️⃣ Plan Generation", "Rules-based generator using ML outputs",
         f"7-day {user_data['fitness_goal']} plan for {plan['fitness_level']} with "
         f"{', '.join(user_data['available_equipment'])}"),
    ]

    for step, method, outcome in pipeline_steps:
        with st.expander(f"{step} — {method}"):
            st.markdown(f"**Outcome:** {outcome}")
            if step.startswith("2"):
                st.markdown("""
                **K-Means Clustering Logic:**
                Features used: Age, Gender, Height, Weight, BMI, BMR, TDEE, Activity Level
                → Scaled by `scaler.pkl` → 4-cluster KMeans → Fitness Level label assigned
                """)
            elif step.startswith("3"):
                st.markdown("""
                **Decision Tree Regressor Logic:**
                Features preprocessed by `calorie_preprocessor.pkl` (encodes categoricals, 
                scales numerics) → DTR predicts exact daily calorie target based on goal & profile
                """)
            elif step.startswith("4"):
                if plan.get("embedding_notes"):
                    for note in plan["embedding_notes"]:
                        st.markdown(f"- {note}")
                else:
                    st.info("No free-text preferences were provided. Add injuries, tastes, or constraints in the sidebar to activate NLP matching.")

    # Macro rationale
    st.markdown("### Macro Target Rationale")
    macros = plan["macros"]
    goal   = user_data["fitness_goal"]

    rationale = {
        "Weight Loss":     "High protein (35%) preserves lean mass during deficit. Moderate carbs fuel workouts; healthy fats support hormonal function.",
        "Muscle Gain":     "Elevated carbs (45%) fuel hypertrophy training sessions. High protein supports muscle protein synthesis. Moderate fat for hormone production.",
        "Endurance":       "Carbohydrate-dominant (55%) macro split fuels aerobic systems. Lower protein sufficient for endurance athletes. Controlled fat for sustained energy.",
        "General Fitness": "Balanced split supporting overall health, energy, and recovery.",
        "Maintenance":     "Maintenance split mirrors General Fitness — sustaining current body composition.",
    }
    st.info(f"**{goal}:** {rationale.get(goal, '')}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Protein Target", f"{macros['protein_g']}g", f"{macros['protein_pct']*100:.0f}% of calories")
    col2.metric("Carbs Target",   f"{macros['carbs_g']}g",   f"{macros['carbs_pct']*100:.0f}% of calories")
    col3.metric("Fat Target",     f"{macros['fat_g']}g",     f"{macros['fat_pct']*100:.0f}% of calories")

    # Full plan JSON export
    st.markdown("### 📥 Export Plan Data")
    import json
    export_data = {
        "user_profile":    {k: v for k, v in user_data.items() if k != "free_text_prefs"},
        "health_metrics":  {
            "bmi": plan["bmi"], "bmi_category": plan["bmi_category"]["label"],
            "bmr": plan["bmr"], "tdee": plan["tdee"],
            "fitness_level": plan["fitness_level"], "fitness_cluster": plan["fitness_cluster"],
        },
        "targets": {"daily_calories": plan["predicted_calories"], "macros": plan["macros"]},
        "workout_summary": [
            {"day": d["day"], "focus": d["focus"], "type": d["type"]}
            for d in plan["workout_plan"]
        ],
    }
    st.download_button(
        "📥 Download Plan (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name="ai_fitness_plan.json",
        mime="application/json",
    )
