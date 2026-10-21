from django.urls import path
from . import views

urlpatterns = [
    path("rent-prediction/", views.predict_rent, name="rent-prediction"),
    path("check-listing/", views.check_listing, name="check-listing"),
    path("recommend-homes/", views.recommend_homes, name="recommend-homes"),
]