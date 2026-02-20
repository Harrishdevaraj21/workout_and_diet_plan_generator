"""model_loader.py — Loads all ML models with graceful fallback stubs."""

import os
import logging
import numpy as np
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

# ─── Try importing joblib, fall back to pickle ────────────────────────────────
try:
    import joblib
    _LOADER = joblib.load
except ImportError:
    import pickle
    def _LOADER(path):
        with open(path, "rb") as f:
            return pickle.load(f)


# ─── Stub classes for when models are not present ─────────────────────────────
class _StubScaler:
    """Pass-through scaler when scaler.pkl is absent."""
    def transform(self, X):
        return X


class _StubKMeans:
    """Deterministic cluster assignment based on feature sum."""
    def predict(self, X):
        feature_sum = np.sum(X, axis=1)
        return (feature_sum % 4).astype(int)


class _StubPreprocessor:
    """Returns features as a DataFrame column vector."""
    def transform(self, df):
        return df.values if hasattr(df, "values") else np.array(df)


class _StubDTR:
    """Harris-Benedict-flavoured calorie predictor."""
    def predict(self, X):
        # X row: [age, gender_enc, height, weight, bmi, bmr, tdee, activity_enc, goal_enc]
        if hasattr(X, "shape") and X.ndim == 2:
            tdee_col = X[:, 6] if X.shape[1] > 6 else X[:, 0]
            return tdee_col * np.random.uniform(0.95, 1.05, size=tdee_col.shape)
        return np.array([2000.0])


class _StubSentenceTransformer:
    """Returns random unit-normalised embeddings."""
    def encode(self, sentences, **kwargs):
        rng = np.random.default_rng(abs(hash(str(sentences))) % (2**32))
        vecs = rng.standard_normal((len(sentences) if isinstance(sentences, list) else 1, 384))
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs / np.maximum(norms, 1e-9)


# ─── ModelLoader ──────────────────────────────────────────────────────────────
class ModelLoader:
    """
    Loads all five models from disk.  If a model file is missing, a stub
    that preserves the expected API is substituted and a warning is shown.
    """

    MODEL_FILES = {
        "scaler":               "models/scaler.pkl",
        "kmeans":               "models/kmeans_model.pkl",
        "calorie_preprocessor": "models/calorie_preprocessor.pkl",
        "dtr":                  "models/dtr_model.pkl",
        "sentence_transformer": "models/sentence_transformer_model.pkl",
    }

    STUBS = {
        "scaler":               _StubScaler(),
        "kmeans":               _StubKMeans(),
        "calorie_preprocessor": _StubPreprocessor(),
        "dtr":                  _StubDTR(),
        "sentence_transformer": _StubSentenceTransformer(),
    }

    def __init__(self, model_dir: str = "."):
        self._models: dict = {}
        self._warnings: list[str] = []
        self._model_dir = model_dir
        self._load_all()
        if self._warnings:
            with st.sidebar:
                st.warning(
                    "⚠️ **Demo mode** — some model files were not found. "
                    "Stub predictions are being used:\n"
                    + "\n".join(f"- `{w}`" for w in self._warnings)
                )

    def _load_all(self):
        for key, filename in self.MODEL_FILES.items():
            path = os.path.join(self._model_dir, filename)
            try:
                self._models[key] = _LOADER(path)
                logger.info(f"✅ Loaded {filename}")
            except FileNotFoundError:
                self._models[key] = self.STUBS[key]
                self._warnings.append(filename)
                logger.warning(f"⚠️ {filename} not found — using stub")
            except Exception as e:
                self._models[key] = self.STUBS[key]
                self._warnings.append(f"{filename} (error: {e})")
                logger.error(f"❌ Error loading {filename}: {e}")

    # ── Public API ────────────────────────────────────────────────────────────

    def scale(self, features: np.ndarray) -> np.ndarray:
        """Scale features with scaler.pkl."""
        return self._models["scaler"].transform(features)

    def predict_cluster(self, scaled_features: np.ndarray) -> int:
        """Predict KMeans fitness cluster."""
        return int(self._models["kmeans"].predict(scaled_features)[0])

    def preprocess_calories(self, feature_dict: dict) -> np.ndarray:
        """
        Convert feature dict → DataFrame → preprocessor → array.
        Handles both sklearn ColumnTransformer/Pipeline and raw arrays.
        """
        df = pd.DataFrame([feature_dict])
        prep = self._models["calorie_preprocessor"]
        try:
            return prep.transform(df)
        except Exception:
            # Fallback: numeric columns only
            numeric_cols = df.select_dtypes(include=[np.number]).values
            return numeric_cols

    def predict_calories(self, processed_features: np.ndarray) -> float:
        """Predict daily calorie requirement."""
        result = self._models["dtr"].predict(processed_features)
        return float(np.clip(result[0], 1200, 6000))

    def match_preferences(
        self,
        free_text: str,
        fitness_level: str,
        fitness_goal: str,
    ) -> list[str]:
        """
        Use sentence transformer to embed free-text preferences and
        return adjustment notes by similarity to a preset candidate bank.
        """
        model = self._models["sentence_transformer"]
        candidates = self._build_candidate_bank(fitness_level, fitness_goal)

        query_emb   = model.encode([free_text])
        cand_embs   = model.encode(candidates)

        # Cosine similarity
        query_norm  = query_emb  / (np.linalg.norm(query_emb,  axis=1, keepdims=True) + 1e-9)
        cand_norms  = cand_embs  / (np.linalg.norm(cand_embs,  axis=1, keepdims=True) + 1e-9)
        sims        = (query_norm @ cand_norms.T).flatten()

        # Top-3 most similar
        top_idx     = np.argsort(sims)[::-1][:3]
        return [candidates[i] for i in top_idx if sims[i] > 0.25]

    @staticmethod
    def _build_candidate_bank(fitness_level: str, fitness_goal: str) -> list[str]:
        """Pre-defined adjustment notes used as embedding candidates."""
        return [
            "Avoid high-impact exercises due to knee pain; substitute with low-impact alternatives.",
            "Incorporate swimming or cycling for cardiovascular training.",
            "Focus on upper-body exercises only to protect lower back injury.",
            "Add yoga and mobility work for flexibility improvement.",
            "Include daily stretching routine for injury prevention.",
            "Prefer plant-based protein sources like lentils, tofu, and tempeh.",
            "Avoid gluten-containing foods; use rice and quinoa as carb bases.",
            "Incorporate high-fibre vegetables for digestive health.",
            "Reduce sodium intake; focus on whole, unprocessed foods.",
            "Include omega-3 rich foods like flaxseed and walnuts.",
            "Prefer spicy cuisine; incorporate jalapeños and hot sauce.",
            "Focus on quick-prep meals under 20 minutes.",
            "Batch-cook on Sundays for the week ahead.",
            "Include intermittent fasting window (16:8).",
            "Focus on progressive overload with barbell compound movements.",
            "Use resistance bands as primary equipment for home workouts.",
            "Incorporate HIIT sessions three times per week.",
            "Prioritise recovery; include active rest days with walking.",
        ]
