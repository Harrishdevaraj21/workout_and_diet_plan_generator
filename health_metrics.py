"""health_metrics.py — BMI, BMR, TDEE and related computations."""

ACTIVITY_MULTIPLIERS = {
    "Sedentary":        1.2,
    "Lightly Active":   1.375,
    "Moderately Active":1.55,
    "Very Active":      1.725,
    "Extremely Active": 1.9,
}

BMI_CATEGORIES = [
    (0,    18.5, "Underweight",    "🔵"),
    (18.5, 25.0, "Normal Weight",  "🟢"),
    (25.0, 30.0, "Overweight",     "🟡"),
    (30.0, 35.0, "Obese Class I",  "🟠"),
    (35.0, 40.0, "Obese Class II", "🔴"),
    (40.0, 999,  "Obese Class III","🔴"),
]


class HealthMetrics:
    def __init__(self, user_data: dict):
        self.age      = user_data["age"]
        self.gender   = user_data["gender"]
        self.height   = user_data["height_cm"]       # cm
        self.weight   = user_data["weight_kg"]       # kg
        self.activity = user_data["activity_level"]
        self.goal     = user_data["fitness_goal"]

    def bmi(self) -> float:
        h_m = self.height / 100
        return self.weight / (h_m ** 2)

    def bmi_category(self) -> dict:
        b = self.bmi()
        for lo, hi, label, emoji in BMI_CATEGORIES:
            if lo <= b < hi:
                return {"label": label, "emoji": emoji, "value": round(b, 1)}
        return {"label": "Unknown", "emoji": "⚪", "value": round(b, 1)}

    def bmr(self) -> float:
        """Harris-Benedict revised equation."""
        if self.gender == "Male":
            return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)

    def tdee(self) -> float:
        multiplier = ACTIVITY_MULTIPLIERS.get(self.activity, 1.55)
        return self.bmr() * multiplier

    def ideal_weight_range(self) -> tuple[float, float]:
        """BMI 18.5–24.9 → kg range."""
        h_m = self.height / 100
        return round(18.5 * h_m**2, 1), round(24.9 * h_m**2, 1)

    def body_fat_estimate(self) -> float:
        """U.S. Navy formula approximation using BMI."""
        b = self.bmi()
        if self.gender == "Male":
            return round(1.20 * b + 0.23 * self.age - 16.2, 1)
        else:
            return round(1.20 * b + 0.23 * self.age - 5.4, 1)
