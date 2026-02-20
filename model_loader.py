"""model_loader.py — Loads all ML models with graceful fallback stubs."""

import os
import sys
import types
import pickle
import logging
import numpy as np
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

# ─── Try importing joblib, fall back to pickle ────────────────────────────────
try:
    import joblib
    _JOBLIB_LOAD = joblib.load
except ImportError:
    _JOBLIB_LOAD = None


# ─── Inject stub modules for removed sentence_transformers submodules ─────────
def _inject_missing_submodules():
    """
    sentence_transformers removed model_card in newer versions but old .pkl
    files still reference it. Injecting a dummy module lets pickle deserialise
    the object without crashing.
    """
    stubs_needed = [
        "sentence_transformers.model_card",
        "sentence_transformers.model_card_templates",
    ]
    for mod_name in stubs_needed:
        if mod_name not in sys.modules:
            parent_name, _, child_name = mod_name.rpartition(".")
            stub = types.ModuleType(mod_name)
            stub.ModelCardData = type(
                "ModelCardData", (), {"__init__": lambda self, **kw: None}
            )
            sys.modules[mod_name] = stub
            if parent_name in sys.modules:
                setattr(sys.modules[parent_name], child_name, stub)


class _SafeUnpickler(pickle.Unpickler):
    """Unpickler that substitutes a stub for any unresolvable class."""

    def find_class(self, module, name):
        _inject_missing_submodules()
        try:
            return super().find_class(module, name)
        except (ImportError, AttributeError):
            logger.warning(f"Cannot resolve {module}.{name} — injecting stub")
            return type(name, (), {
                "__init__": lambda self, *a, **kw: None,
                "encode": lambda self, sentences, **kw: np.zeros(
                    (len(sentences) if isinstance(sentences, list) else 1, 384)
                ),
            })


def _safe_load(path: str):
    """
    1. Inject missing submodule stubs.
    2. Try joblib/pickle normally.
    3. Fall back to _SafeUnpickler if an ImportError / ModuleNotFoundError occurs.
    """
    _inject_missing_submodules()

    # First attempt — normal load
    try:
        if _JOBLIB_LOAD:
            return _JOBLIB_LOAD(path)
        with open(path, "rb") as f:
            return pickle.load(f)
    except (ImportError, ModuleNotFoundError) as e:
        logger.warning(f"Normal load failed ({e}), retrying with safe unpickler…")

    # Second attempt — safe unpickler
    with open(path, "rb") as f:
        return _SafeUnpickler(f).load()


# ─── Stub classes ─────────────────────────────────────────────────────────────
class _StubScaler:
    def transform(self, X):
        return X if not hasattr(X, "values") else X.values


class _StubKMeans:
    def predict(self, X):
        arr = X.values if hasattr(X, "values") else np.asarray(X)
        return (np.sum(arr, axis=1) % 4).astype(int)


class _StubPreprocessor:
    def transform(self, df):
        return df.values if hasattr(df, "values") else np.array(df)


class _StubDTR:
    def predict(self, X):
        arr = X.values if hasattr(X, "values") else np.asarray(X)
        if arr.ndim == 2 and arr.shape[1] > 0:
            return arr[:, 0] * np.random.uniform(0.95, 1.05, size=arr.shape[0])
        return np.array([2000.0])


class _StubSentenceTransformer:
    def encode(self, sentences, **kwargs):
        n = len(sentences) if isinstance(sentences, list) else 1
        rng = np.random.default_rng(abs(hash(str(sentences))) % (2**32))
        vecs = rng.standard_normal((n, 384))
        return vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9)


# ─── ModelLoader ──────────────────────────────────────────────────────────────
class ModelLoader:
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

    # Exact column names the scaler/kmeans were trained on
    SCALER_COLUMNS = [
        "age",
        "bmi",
        "activity_level_active",
        "activity_level_light",
        "activity_level_moderate",
        "activity_level_sedentary",
        "activity_level_very active",
    ]

    def __init__(self, model_dir: str = "."):
        self._models: dict = {}
        self._warnings: list = []
        self._model_dir = model_dir
        self._load_all()
        if self._warnings:
            with st.sidebar:
                st.warning(
                    "⚠️ **Demo mode** — some model files were not found.\n"
                    "Stub predictions are being used:\n"
                    + "\n".join(f"- `{w}`" for w in self._warnings)
                )

    def _load_all(self):
        for key, filename in self.MODEL_FILES.items():
            path = os.path.join(self._model_dir, filename)
            try:
                self._models[key] = _safe_load(path)
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
        df = pd.DataFrame(features, columns=self.SCALER_COLUMNS)
        return self._models["scaler"].transform(df)

    def predict_cluster(self, scaled_features: np.ndarray) -> int:
        df = pd.DataFrame(scaled_features, columns=self.SCALER_COLUMNS)
        return int(self._models["kmeans"].predict(df)[0])

    def preprocess_calories(self, feature_dict: dict) -> np.ndarray:
        df = pd.DataFrame([feature_dict])
        prep = self._models["calorie_preprocessor"]
        try:
            return prep.transform(df)
        except Exception:
            return df.select_dtypes(include=[np.number]).values

    def predict_calories(self, processed_features: np.ndarray) -> float:
        result = self._models["dtr"].predict(processed_features)
        return float(np.clip(result[0], 1200, 6000))

    def match_preferences(
        self,
        free_text: str,
        fitness_level: str,
        fitness_goal: str,
    ) -> list:
        model = self._models["sentence_transformer"]
        candidates = self._build_candidate_bank(fitness_level, fitness_goal)

        query_emb  = model.encode([free_text])
        cand_embs  = model.encode(candidates)

        q_norm = query_emb / (np.linalg.norm(query_emb, axis=1, keepdims=True) + 1e-9)
        c_norm = cand_embs / (np.linalg.norm(cand_embs, axis=1, keepdims=True) + 1e-9)
        sims   = (q_norm @ c_norm.T).flatten()

        top_idx = np.argsort(sims)[::-1][:3]
        return [candidates[i] for i in top_idx if sims[i] > 0.25]

    @staticmethod
    def _build_candidate_bank(fitness_level: str, fitness_goal: str) -> list:
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
