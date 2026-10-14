import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"
model = joblib.load(MODEL_PATH)

def predict_rent(data: dict) -> float:
    return float(model.predict(pd.DataFrame([data]))[0])