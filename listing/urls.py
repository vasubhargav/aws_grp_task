
from django.urls import path
from . import views
from .views import upload_listing_image
urlpatterns = [
    # Get all properties
    path('properties/', views.get_properties, name='get_properties'),

    # Get one property by ID
    path('properties/<int:listing_id>/', views.get_property, name='get_property'),

    # Create a property
    path('properties/create/', views.createlisting, name='create_listing'),

    # Update a property (PUT)
    path('properties/<int:pk>/update/', views.updatelisting, name='update_listing'),

    #update a property (PATCH)
    path('properties/<int:pk>/partial-update/', views.updateproperty, name='partial_update_listing'),

    # Delete
    path('properties/<int:pk>/delete/', views.delete_property, name='delete_property'),

    #image_upload
    path('properties/<int:pk>/upload-image/',upload_listing_image, name='upload-listing-image'),

    path('properties/browse/', views.browse_properties, name='browse_properties'),

]
