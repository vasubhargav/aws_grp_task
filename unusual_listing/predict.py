import pandas as pd
import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "unusual_model.pkl"
saved = joblib.load(MODEL_PATH)
model = saved["model"]
city_medians = saved["city_medians"]

def check_listing(data: dict) -> dict:
    """data needs: BHK, Size, City, Rent"""
    city = data["City"]
    if city not in city_medians:
        return {"unusual": None, "message": "City not supported"}
    if data["Size"] <= 0 or data["BHK"] <= 0 or data["Rent"] <= 0:
        return {"unusual": True, "message": "Invalid values"}

    rent_vs_city = (data["Rent"] / data["Size"]) / city_medians[city]
    sqft_per_bhk = data["Size"] / data["BHK"]
    row = pd.DataFrame([{"log_rent_vs_city": np.log(rent_vs_city),
    "log_sqft_per_bhk": np.log(sqft_per_bhk)}])
    return {"unusual": bool(model.predict(row)[0] == -1)}