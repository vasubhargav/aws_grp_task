from fastapi import FastAPI
from pydantic import BaseModel
from rent.predict import predict_rent
from unusual.predict import check_listing
from recommend.predict import recommend_homes

app = FastAPI()

class RentRequest(BaseModel):
    bhk: int
    size: int
    floor: int
    bathroom: int
    city: str
    area_type: str
    furnishing_status: str
    tenant_preferred: str

@app.post("/predict-rent")
def rent(req: RentRequest):
    data = {
        "BHK": req.bhk, "Size": req.size, "Floor": req.floor,
        "Bathroom": req.bathroom, "City": req.city,
        "Area Type": req.area_type,
        "Furnishing Status": req.furnishing_status,
        "Tenant Preferred": req.tenant_preferred,
    }
    return {"estimated_rent": predict_rent(data)}


class ListingCheckRequest(BaseModel):
    bhk: int
    size: int
    city: str
    rent: int

@app.post("/check-listing")
def check(req: ListingCheckRequest):
    data = {"BHK": req.bhk, "Size": req.size, "City": req.city, "Rent": req.rent}
    return check_listing(data)


class RecommendRequest(BaseModel):
    city: str
    max_rent: int
    bhk: int
    furnishing_status: str

@app.post("/recommend-homes")
def recommend(req: RecommendRequest):
    data = {
        "City": req.city, "Max Rent": req.max_rent,
        "BHK": req.bhk, "Furnishing Status": req.furnishing_status,
    }
    return {"homes": recommend_homes(data)}