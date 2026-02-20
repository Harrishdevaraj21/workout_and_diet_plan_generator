"""planner.py — Workout and diet plan generation logic."""

from __future__ import annotations
import random


# ─────────────────────────────────────────────────────────────────────────────
# Exercise Database
# ─────────────────────────────────────────────────────────────────────────────

EXERCISE_DB = {
    "Beginner": {
        "Weight Loss": {
            "Bodyweight": [
                {"name": "Jumping Jacks",       "sets": "3×30s",  "muscle": "Full Body"},
                {"name": "Bodyweight Squats",   "sets": "3×15",   "muscle": "Quads / Glutes"},
                {"name": "Push-ups (Knee)",      "sets": "3×10",   "muscle": "Chest / Triceps"},
                {"name": "Mountain Climbers",    "sets": "3×20",   "muscle": "Core / Cardio"},
                {"name": "Glute Bridges",        "sets": "3×15",   "muscle": "Glutes / Hamstrings"},
                {"name": "Plank Hold",           "sets": "3×20s",  "muscle": "Core"},
            ],
            "Dumbbells": [
                {"name": "DB Goblet Squat",      "sets": "3×12",   "muscle": "Quads"},
                {"name": "DB Romanian Deadlift", "sets": "3×12",   "muscle": "Hamstrings"},
                {"name": "DB Shoulder Press",    "sets": "3×10",   "muscle": "Shoulders"},
                {"name": "DB Bent-over Row",     "sets": "3×12",   "muscle": "Back"},
                {"name": "DB Bicep Curl",        "sets": "3×12",   "muscle": "Biceps"},
                {"name": "DB Tricep Kickback",   "sets": "3×12",   "muscle": "Triceps"},
            ],
        },
        "Muscle Gain": {
            "Bodyweight": [
                {"name": "Push-ups",             "sets": "4×12",   "muscle": "Chest / Triceps"},
                {"name": "Inverted Rows",        "sets": "4×10",   "muscle": "Back / Biceps"},
                {"name": "Jump Squats",          "sets": "4×10",   "muscle": "Quads / Glutes"},
                {"name": "Dips (Chair)",         "sets": "3×10",   "muscle": "Triceps / Chest"},
                {"name": "Pike Push-ups",        "sets": "3×10",   "muscle": "Shoulders"},
                {"name": "Plank to Push-up",     "sets": "3×8",    "muscle": "Core / Chest"},
            ],
            "Dumbbells": [
                {"name": "DB Bench Press",       "sets": "4×10",   "muscle": "Chest"},
                {"name": "DB Deadlift",          "sets": "4×10",   "muscle": "Posterior Chain"},
                {"name": "DB Squat",             "sets": "4×12",   "muscle": "Quads / Glutes"},
                {"name": "DB Overhead Press",    "sets": "4×10",   "muscle": "Shoulders"},
                {"name": "DB Row",               "sets": "4×10",   "muscle": "Back"},
                {"name": "DB Curl + Press",      "sets": "3×10",   "muscle": "Biceps / Shoulders"},
            ],
        },
    },
    "Intermediate": {
        "Weight Loss": {
            "Bodyweight": [
                {"name": "Burpees",              "sets": "4×10",   "muscle": "Full Body"},
                {"name": "Box Jumps",            "sets": "4×8",    "muscle": "Legs / Power"},
                {"name": "Spiderman Push-ups",   "sets": "4×10",   "muscle": "Chest / Core"},
                {"name": "Bulgarian Split Squat","sets": "3×12",   "muscle": "Quads / Glutes"},
                {"name": "Bear Crawls",          "sets": "3×20m",  "muscle": "Full Body"},
                {"name": "V-ups",                "sets": "4×15",   "muscle": "Core"},
            ],
            "Barbell": [
                {"name": "Barbell Squat",        "sets": "4×10",   "muscle": "Quads / Glutes"},
                {"name": "Deadlift",             "sets": "4×8",    "muscle": "Posterior Chain"},
                {"name": "Bench Press",          "sets": "4×10",   "muscle": "Chest"},
                {"name": "Bent-over Row",        "sets": "4×10",   "muscle": "Back"},
                {"name": "Overhead Press",       "sets": "3×10",   "muscle": "Shoulders"},
                {"name": "Romanian Deadlift",    "sets": "3×12",   "muscle": "Hamstrings"},
            ],
        },
        "Muscle Gain": {
            "Barbell": [
                {"name": "Barbell Squat",        "sets": "5×5",    "muscle": "Quads / Glutes"},
                {"name": "Bench Press",          "sets": "5×5",    "muscle": "Chest"},
                {"name": "Deadlift",             "sets": "4×5",    "muscle": "Full Posterior"},
                {"name": "Barbell Row",          "sets": "4×6",    "muscle": "Back"},
                {"name": "Overhead Press",       "sets": "4×6",    "muscle": "Shoulders"},
                {"name": "Barbell Hip Thrust",   "sets": "4×10",   "muscle": "Glutes"},
            ],
            "Dumbbells": [
                {"name": "DB Incline Press",     "sets": "4×10",   "muscle": "Upper Chest"},
                {"name": "DB Lateral Raise",     "sets": "4×15",   "muscle": "Side Delts"},
                {"name": "Hammer Curl",          "sets": "3×12",   "muscle": "Biceps / Brachialis"},
                {"name": "Skull Crushers",       "sets": "3×12",   "muscle": "Triceps"},
                {"name": "Bulgarian Split Squat","sets": "4×10",   "muscle": "Quads / Glutes"},
                {"name": "DB Shrugs",            "sets": "3×15",   "muscle": "Traps"},
            ],
        },
    },
    "Advanced": {
        "Muscle Gain": {
            "Barbell": [
                {"name": "Squat (Heavy)",        "sets": "6×4",    "muscle": "Quads / Glutes"},
                {"name": "Deadlift (Heavy)",     "sets": "5×3",    "muscle": "Full Posterior"},
                {"name": "Bench Press (Heavy)",  "sets": "5×4",    "muscle": "Chest"},
                {"name": "Weighted Pull-ups",    "sets": "5×5",    "muscle": "Back / Biceps"},
                {"name": "Push Press",           "sets": "4×5",    "muscle": "Shoulders / Triceps"},
                {"name": "Barbell Lunge",        "sets": "4×8/leg","muscle": "Quads / Glutes"},
            ],
            "Bodyweight": [
                {"name": "Muscle-ups",           "sets": "4×5",    "muscle": "Full Upper Body"},
                {"name": "Pistol Squats",        "sets": "4×6/leg","muscle": "Quads / Balance"},
                {"name": "Handstand Push-ups",   "sets": "3×6",    "muscle": "Shoulders / Triceps"},
                {"name": "Dragon Flags",         "sets": "3×6",    "muscle": "Core"},
                {"name": "One-arm Row",          "sets": "4×8",    "muscle": "Back"},
                {"name": "Plyometric Push-ups",  "sets": "4×10",   "muscle": "Chest / Power"},
            ],
        },
        "Endurance": {
            "Bodyweight": [
                {"name": "EMOM Burpees (10min)", "sets": "1×10min","muscle": "Full Body"},
                {"name": "Double Unders",        "sets": "5×50",   "muscle": "Cardio / Calves"},
                {"name": "Air Squats Tabata",    "sets": "8×20s",  "muscle": "Legs"},
                {"name": "Pull-ups AMRAP",       "sets": "4×max",  "muscle": "Back / Biceps"},
                {"name": "Push-up AMRAP",        "sets": "4×max",  "muscle": "Chest / Triceps"},
                {"name": "L-sit Hold",           "sets": "4×15s",  "muscle": "Core"},
            ],
        },
    },
    "Elite": {
        "Muscle Gain": {
            "Barbell": [
                {"name": "Competition Squat",    "sets": "7×3",    "muscle": "Quads / Glutes"},
                {"name": "Sumo Deadlift",        "sets": "6×2",    "muscle": "Full Posterior"},
                {"name": "Close-grip Bench",     "sets": "5×4",    "muscle": "Chest / Triceps"},
                {"name": "Pendlay Row",          "sets": "5×5",    "muscle": "Back"},
                {"name": "Z-press",              "sets": "4×6",    "muscle": "Shoulders"},
                {"name": "Pause Squat",          "sets": "4×5",    "muscle": "Quads / Core"},
            ],
            "Bodyweight": [
                {"name": "Ring Muscle-ups",      "sets": "5×5",    "muscle": "Full Upper Body"},
                {"name": "Planche Hold",         "sets": "5×5s",   "muscle": "Chest / Core"},
                {"name": "Front Lever Row",      "sets": "4×5",    "muscle": "Back"},
                {"name": "HSPUs (Strict)",       "sets": "5×5",    "muscle": "Shoulders"},
                {"name": "Pistol Squat Depth",   "sets": "4×8/leg","muscle": "Quads"},
                {"name": "Dragon Flag",          "sets": "4×8",    "muscle": "Core"},
            ],
        },
    },
}

WEEKLY_STRUCTURE = {
    "Weight Loss":  ["Full Body HIIT", "Rest / Walk", "Upper Body", "Cardio", "Lower Body", "Full Body", "Rest"],
    "Muscle Gain":  ["Push",           "Pull",        "Legs",       "Rest",   "Push",        "Pull",      "Legs"],
    "Endurance":    ["Cardio",         "Strength",    "Cardio",     "Rest",   "Cardio",      "Strength",  "Long Cardio"],
    "General Fitness": ["Full Body",   "Cardio",      "Rest",       "Upper",  "Lower",       "Cardio",    "Rest"],
    "Maintenance":  ["Full Body",      "Rest",        "Full Body",  "Cardio", "Full Body",   "Cardio",    "Rest"],
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class WorkoutPlanner:
    @staticmethod
    def generate(
        fitness_level: str,
        fitness_goal: str,
        available_equipment: list[str],
        notes: list[str],
    ) -> list[dict]:
        """Return a 7-day workout plan."""
        structure = WEEKLY_STRUCTURE.get(fitness_goal, WEEKLY_STRUCTURE["General Fitness"])

        # Find best exercise set
        level_db = EXERCISE_DB.get(fitness_level, EXERCISE_DB["Intermediate"])
        goal_db  = level_db.get(fitness_goal, next(iter(level_db.values())))

        # Pick equipment tier
        equip_order = _rank_equipment(available_equipment)
        exercises = goal_db.get(equip_order[0], next(iter(goal_db.values())))

        plan = []
        for i, (day, focus) in enumerate(zip(DAYS, structure)):
            if "Rest" in focus:
                plan.append({
                    "day": day, "focus": focus, "type": "rest",
                    "exercises": [],
                    "duration_min": 0, "notes": "Active recovery: light walking or stretching",
                })
            else:
                # Pick 4-6 exercises with slight variation per day
                rng = random.Random(i + hash(fitness_level))
                shuffled = exercises.copy()
                rng.shuffle(shuffled)
                n = min(6, max(4, len(shuffled)))
                plan.append({
                    "day": day, "focus": focus, "type": "workout",
                    "exercises": shuffled[:n],
                    "duration_min": 45 if fitness_level in ("Beginner", "Intermediate") else 60,
                    "notes": _workout_note(focus, fitness_goal, notes),
                })
        return plan

    @staticmethod
    def estimate_weekly_calorie_burn(
        fitness_level: str, fitness_goal: str, weight_kg: float
    ) -> float:
        """Rough weekly calorie burn from workouts."""
        sessions = {"Beginner": 4, "Intermediate": 5, "Advanced": 6, "Elite": 6}.get(fitness_level, 5)
        met      = {"Weight Loss": 7.0, "Muscle Gain": 5.5, "Endurance": 8.5,
                    "General Fitness": 6.0, "Maintenance": 5.0}.get(fitness_goal, 6.0)
        duration_h = 0.75
        return round(met * weight_kg * duration_h * sessions, 0)


def _rank_equipment(equipment: list[str]) -> list[str]:
    """Prefer barbell > dumbbells > resistance bands > bodyweight."""
    priority = ["Barbell", "Dumbbells", "Resistance Bands", "Bodyweight", "Machines"]
    owned = set(equipment)
    return [e for e in priority if e in owned] + [e for e in priority if e not in owned]


def _workout_note(focus: str, goal: str, nlp_notes: list[str]) -> str:
    base_notes = {
        "Full Body HIIT": "Keep rest < 30s; heart rate 75-85% max.",
        "Upper Body":     "Focus on mind-muscle connection; controlled negatives.",
        "Lower Body":     "Drive through heels; full depth on squats.",
        "Push":           "Progressive overload: add 2.5kg when you hit top of rep range.",
        "Pull":           "Control the eccentric; aim for full shoulder extension.",
        "Legs":           "Warm up thoroughly; prioritise form over load.",
        "Cardio":         "Maintain conversational pace for aerobic base.",
        "Strength":       "Rest 2-3 min between heavy sets.",
        "Full Body":      "Compound-first ordering; save isolation for the end.",
        "Long Cardio":    "Zone 2 intensity: 60-70% max HR for 45-90 min.",
    }
    note = base_notes.get(focus, "Focus on quality reps over speed.")
    if nlp_notes:
        note += f" ★ {nlp_notes[0]}"
    return note


# ─────────────────────────────────────────────────────────────────────────────
# Diet Planner
# ─────────────────────────────────────────────────────────────────────────────

FOOD_DB = {
    "Vegetarian": {
        "South Asian": {
            "breakfast": [
                {"item": "Masala Oats with milk", "protein": 12, "carbs": 45, "fat": 8, "cost": 0.80},
                {"item": "Idli (3) + Sambar + Chutney", "protein": 10, "carbs": 55, "fat": 4, "cost": 0.60},
                {"item": "Poha with peanuts + boiled egg",  "protein": 14, "carbs": 48, "fat": 7, "cost": 0.70},
            ],
            "lunch": [
                {"item": "Brown rice + Dal + Mixed veg sabzi + Raita", "protein": 18, "carbs": 70, "fat": 6, "cost": 1.20},
                {"item": "Roti (3) + Paneer curry + Salad", "protein": 22, "carbs": 55, "fat": 14, "cost": 1.50},
                {"item": "Rajma rice + Curd", "protein": 20, "carbs": 72, "fat": 5, "cost": 1.10},
            ],
            "snack": [
                {"item": "Greek yogurt + banana", "protein": 14, "carbs": 30, "fat": 2, "cost": 0.50},
                {"item": "Roasted chana + sprouts", "protein": 12, "carbs": 22, "fat": 3, "cost": 0.40},
                {"item": "Paneer cubes + cucumber", "protein": 16, "carbs": 5, "fat": 10, "cost": 0.70},
            ],
            "dinner": [
                {"item": "Chapati (2) + Palak tofu + Dal soup", "protein": 24, "carbs": 55, "fat": 8, "cost": 1.30},
                {"item": "Khichdi (rice + moong) + Ghee + Papad", "protein": 16, "carbs": 65, "fat": 7, "cost": 0.90},
                {"item": "Paneer tikka + roti (2) + salad", "protein": 28, "carbs": 48, "fat": 12, "cost": 1.80},
            ],
        },
        "Western": {
            "breakfast": [
                {"item": "Overnight oats + chia + berries", "protein": 12, "carbs": 55, "fat": 8, "cost": 1.20},
                {"item": "Whole-grain toast + avocado + poached eggs", "protein": 18, "carbs": 38, "fat": 16, "cost": 2.00},
                {"item": "Smoothie bowl (banana, protein powder, granola)", "protein": 22, "carbs": 60, "fat": 5, "cost": 1.80},
            ],
            "lunch": [
                {"item": "Quinoa salad + chickpeas + feta + olive oil", "protein": 18, "carbs": 52, "fat": 12, "cost": 2.50},
                {"item": "Lentil soup + whole-grain bread", "protein": 16, "carbs": 55, "fat": 5, "cost": 1.50},
                {"item": "Buddha bowl (brown rice, roasted veg, tahini)", "protein": 14, "carbs": 65, "fat": 10, "cost": 2.20},
            ],
            "snack": [
                {"item": "Apple + almond butter", "protein": 5, "carbs": 28, "fat": 8, "cost": 0.80},
                {"item": "Cottage cheese + pineapple", "protein": 18, "carbs": 18, "fat": 2, "cost": 1.00},
                {"item": "Hummus + carrot sticks", "protein": 7, "carbs": 20, "fat": 6, "cost": 0.70},
            ],
            "dinner": [
                {"item": "Stuffed bell peppers (quinoa, black beans, cheese)", "protein": 22, "carbs": 55, "fat": 10, "cost": 2.80},
                {"item": "Pasta primavera + parmesan", "protein": 18, "carbs": 68, "fat": 9, "cost": 2.00},
                {"item": "Veggie stir-fry with tofu + brown rice", "protein": 24, "carbs": 62, "fat": 8, "cost": 1.80},
            ],
        },
    },
    "Non-Vegetarian": {
        "South Asian": {
            "breakfast": [
                {"item": "Egg omelette (3 eggs) + toast + milk", "protein": 24, "carbs": 35, "fat": 14, "cost": 0.90},
                {"item": "Chicken poha + boiled egg", "protein": 22, "carbs": 50, "fat": 8, "cost": 1.00},
                {"item": "Oats + whey protein + banana", "protein": 28, "carbs": 55, "fat": 5, "cost": 1.20},
            ],
            "lunch": [
                {"item": "Chicken biryani (200g chicken) + raita", "protein": 35, "carbs": 75, "fat": 12, "cost": 1.80},
                {"item": "Fish curry + brown rice + salad", "protein": 32, "carbs": 68, "fat": 10, "cost": 1.50},
                {"item": "Egg curry (3 eggs) + roti (3) + dal", "protein": 30, "carbs": 60, "fat": 14, "cost": 1.20},
            ],
            "snack": [
                {"item": "Boiled eggs (2) + chaat masala", "protein": 14, "carbs": 2, "fat": 10, "cost": 0.40},
                {"item": "Tuna salad on whole-grain crackers", "protein": 20, "carbs": 18, "fat": 4, "cost": 1.10},
                {"item": "Greek yogurt + protein powder", "protein": 24, "carbs": 18, "fat": 2, "cost": 0.80},
            ],
            "dinner": [
                {"item": "Grilled chicken (200g) + quinoa + steamed broccoli", "protein": 42, "carbs": 45, "fat": 8, "cost": 2.50},
                {"item": "Prawn stir-fry + roti (2) + dal soup", "protein": 35, "carbs": 55, "fat": 9, "cost": 2.20},
                {"item": "Mutton keema (150g) + roti (2) + salad", "protein": 38, "carbs": 48, "fat": 16, "cost": 2.80},
            ],
        },
        "Western": {
            "breakfast": [
                {"item": "Scrambled eggs (4) + turkey bacon + sourdough", "protein": 32, "carbs": 40, "fat": 18, "cost": 2.50},
                {"item": "Greek yogurt parfait + granola + chicken sausage", "protein": 28, "carbs": 52, "fat": 12, "cost": 2.20},
                {"item": "Protein pancakes + maple syrup + bacon", "protein": 30, "carbs": 58, "fat": 14, "cost": 2.80},
            ],
            "lunch": [
                {"item": "Grilled chicken salad + vinaigrette + whole-grain roll", "protein": 38, "carbs": 42, "fat": 10, "cost": 3.50},
                {"item": "Tuna wrap + Greek salad", "protein": 32, "carbs": 48, "fat": 8, "cost": 2.50},
                {"item": "Salmon bowl + quinoa + avocado", "protein": 36, "carbs": 52, "fat": 16, "cost": 4.00},
            ],
            "snack": [
                {"item": "Cottage cheese + almonds", "protein": 22, "carbs": 10, "fat": 12, "cost": 1.20},
                {"item": "Turkey slices + celery + hummus", "protein": 20, "carbs": 12, "fat": 5, "cost": 1.50},
                {"item": "Whey protein shake + banana", "protein": 28, "carbs": 32, "fat": 2, "cost": 1.00},
            ],
            "dinner": [
                {"item": "Grilled salmon (200g) + sweet potato + asparagus", "protein": 42, "carbs": 45, "fat": 14, "cost": 5.00},
                {"item": "Beef stir-fry + brown rice + bok choy", "protein": 38, "carbs": 58, "fat": 12, "cost": 4.50},
                {"item": "Baked chicken thighs + roasted veg + couscous", "protein": 40, "carbs": 52, "fat": 10, "cost": 3.50},
            ],
        },
    },
    "Vegan": {
        "South Asian": {
            "breakfast": [
                {"item": "Tofu scramble + roti (2) + coconut milk chai", "protein": 18, "carbs": 45, "fat": 10, "cost": 0.90},
                {"item": "Moong dosa + coconut chutney + sambar", "protein": 14, "carbs": 55, "fat": 6, "cost": 0.80},
                {"item": "Oats porridge with almond milk + chia seeds", "protein": 10, "carbs": 52, "fat": 8, "cost": 1.00},
            ],
            "lunch": [
                {"item": "Rajma (kidney bean) curry + brown rice + salad", "protein": 18, "carbs": 72, "fat": 4, "cost": 1.00},
                {"item": "Chana masala + roti (3) + onion salad", "protein": 20, "carbs": 65, "fat": 5, "cost": 0.90},
                {"item": "Mixed dal + millet roti + sabzi", "protein": 16, "carbs": 60, "fat": 5, "cost": 0.80},
            ],
            "snack": [
                {"item": "Roasted makhana + green tea", "protein": 5, "carbs": 20, "fat": 2, "cost": 0.40},
                {"item": "Banana + peanut butter", "protein": 8, "carbs": 35, "fat": 10, "cost": 0.50},
                {"item": "Sprout chaat", "protein": 12, "carbs": 25, "fat": 2, "cost": 0.40},
            ],
            "dinner": [
                {"item": "Tofu palak + roti (2) + dal soup", "protein": 22, "carbs": 50, "fat": 8, "cost": 1.20},
                {"item": "Lentil kitchari + coconut raita", "protein": 18, "carbs": 62, "fat": 7, "cost": 0.80},
                {"item": "Chickpea tikka + roti (2) + salad", "protein": 20, "carbs": 55, "fat": 6, "cost": 1.00},
            ],
        },
        "Western": {
            "breakfast": [
                {"item": "Açaí bowl + granola + mixed berries + hemp seeds", "protein": 10, "carbs": 65, "fat": 8, "cost": 3.50},
                {"item": "Overnight oats (oat milk) + flaxseed + walnuts", "protein": 12, "carbs": 58, "fat": 12, "cost": 1.80},
                {"item": "Tofu scramble + avocado + sourdough (2 slices)", "protein": 18, "carbs": 45, "fat": 14, "cost": 2.50},
            ],
            "lunch": [
                {"item": "Lentil & roasted vegetable bowl + tahini", "protein": 18, "carbs": 62, "fat": 10, "cost": 2.50},
                {"item": "Black bean tacos (3) + guacamole + salsa", "protein": 16, "carbs": 70, "fat": 12, "cost": 2.80},
                {"item": "Chickpea pasta + marinara + nutritional yeast", "protein": 20, "carbs": 72, "fat": 6, "cost": 2.20},
            ],
            "snack": [
                {"item": "Edamame + sea salt", "protein": 16, "carbs": 14, "fat": 5, "cost": 0.80},
                {"item": "Almond butter + apple slices", "protein": 6, "carbs": 30, "fat": 10, "cost": 1.00},
                {"item": "Pumpkin seeds + dark chocolate", "protein": 8, "carbs": 20, "fat": 12, "cost": 1.20},
            ],
            "dinner": [
                {"item": "Tempeh stir-fry + brown rice + broccoli", "protein": 26, "carbs": 60, "fat": 8, "cost": 3.00},
                {"item": "Stuffed portobello + quinoa + roasted tomatoes", "protein": 18, "carbs": 55, "fat": 8, "cost": 3.50},
                {"item": "Red lentil soup + crusty sourdough + side salad", "protein": 18, "carbs": 65, "fat": 5, "cost": 2.00},
            ],
        },
    },
}

MEAL_NAMES = ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner"]
MEAL_CALORIE_SPLITS = [0.25, 0.10, 0.30, 0.10, 0.25]


class DietPlanner:
    @staticmethod
    def generate(
        daily_calories: float,
        macros: dict,
        dietary_preference: str,
        cultural_food_habits: str,
        budget_usd: float,
        notes: list[str],
    ) -> dict:
        """Return a structured 7-day diet plan."""
        # Resolve DB keys
        diet_key    = _resolve_diet_key(dietary_preference)
        culture_key = _resolve_culture_key(cultural_food_habits)
        meal_db     = FOOD_DB.get(diet_key, FOOD_DB["Non-Vegetarian"])
        culture_db  = meal_db.get(culture_key, next(iter(meal_db.values())))

        # Build a daily template
        daily_template = _build_daily_meals(
            culture_db, daily_calories, MEAL_CALORIE_SPLITS, budget_usd
        )

        # 7-day plan with slight variation
        weekly_plan = []
        for day in DAYS:
            rng = random.Random(hash(day))
            day_meals = []
            for i, (meal_name, split, budget_split) in enumerate(
                zip(MEAL_NAMES, MEAL_CALORIE_SPLITS, [0.15, 0.05, 0.40, 0.05, 0.35])
            ):
                cat_map = {
                    0: "breakfast", 1: "snack", 2: "lunch", 3: "snack", 4: "dinner"
                }
                cat   = cat_map[i]
                items = culture_db.get(cat, [])
                item  = rng.choice(items) if items else {"item": "Mixed salad", "protein": 10, "carbs": 20, "fat": 5, "cost": 1.00}
                target_cal = daily_calories * split
                day_meals.append({
                    "name":     meal_name,
                    "item":     item["item"],
                    "calories": round(target_cal),
                    "protein":  item["protein"],
                    "carbs":    item["carbs"],
                    "fat":      item["fat"],
                    "cost":     round(item["cost"], 2),
                })
            weekly_plan.append({"day": day, "meals": day_meals})

        nlp_adjustment = notes[1] if len(notes) > 1 else None

        return {
            "weekly_plan":       weekly_plan,
            "daily_template":    daily_template,
            "total_daily_cal":   daily_calories,
            "macros":            macros,
            "budget_usd":        budget_usd,
            "dietary_preference":dietary_preference,
            "cultural_food_habits": cultural_food_habits,
            "nlp_adjustment":    nlp_adjustment,
        }


def _build_daily_meals(culture_db, total_cal, splits, budget):
    meals = []
    cats  = ["breakfast", "snack", "lunch", "snack", "dinner"]
    for name, split, cat in zip(MEAL_NAMES, splits, cats):
        items  = culture_db.get(cat, [])
        item   = items[0] if items else {"item": "Mixed salad", "protein": 10, "carbs": 20, "fat": 5, "cost": 1.00}
        meals.append({
            "name":     name,
            "item":     item["item"],
            "calories": round(total_cal * split),
            "protein":  item["protein"],
            "carbs":    item["carbs"],
            "fat":      item["fat"],
        })
    return meals


def _resolve_diet_key(pref: str) -> str:
    mapping = {
        "Vegetarian": "Vegetarian",
        "Vegan":      "Vegan",
        "Pescatarian":"Non-Vegetarian",
        "Non-Vegetarian": "Non-Vegetarian",
        "Keto":       "Non-Vegetarian",
        "Paleo":      "Non-Vegetarian",
    }
    return mapping.get(pref, "Non-Vegetarian")


def _resolve_culture_key(culture: str) -> str:
    if any(k in culture for k in ["Indian", "South Asian", "Middle Eastern", "Southeast Asian"]):
        return "South Asian"
    return "Western"
