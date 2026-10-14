import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.neighbors import NearestNeighbors

saved = joblib.load(Path(__file__).resolve().parent / "recommend_model.pkl")
listings = saved["listings"]
scaler = saved["scaler"]

FURN_TYPES = ["Furnished", "Semi-Furnished", "Unfurnished"]
W_RENT, W_BHK, W_FURN = 3, 2, 1

def recommend_homes(data: dict, k: int = 5) -> list:
    """data needs: City, Max Rent, BHK, Furnishing Status"""
    pool = listings[(listings["City"] == data["City"]) &
                    (listings["Rent"] <= data["Max Rent"])]
    if pool.empty:
        return []

    furn = pd.get_dummies(pool["Furnishing Status"], dtype=float) \
             .reindex(columns=FURN_TYPES, fill_value=0.0)
    features = np.hstack([pool[["rent_s"]].values * W_RENT,
                          pool[["bhk_s"]].values * W_BHK,
                          furn.values * W_FURN])

    q = scaler.transform(pd.DataFrame([[np.log1p(data["Max Rent"]), data["BHK"]]],
                                      columns=["log_rent", "BHK"]))[0]
    query = [q[0] * W_RENT, q[1] * W_BHK] + \
            [W_FURN * float(c == data["Furnishing Status"]) for c in FURN_TYPES]

    knn = NearestNeighbors(n_neighbors=min(k, len(pool))).fit(features)
    _, idx = knn.kneighbors([query])
    cols = ["BHK", "Size", "Furnishing Status", "Rent", "Area Locality"]
    return pool.iloc[idx[0]][cols].to_dict("records")