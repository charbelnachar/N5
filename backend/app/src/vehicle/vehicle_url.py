from django.urls import include, path
from app.src.vehicle.vehicle_view import VehicleAPIView, CreateVehicleAPIView, AllVehicleAPIView

urlpatterns = [
    # POST: Creates a new vehicle
    path('vehicle/', CreateVehicleAPIView.as_view(), name='vehicle'),

    # GET, PUT, DELETE: Retrieves, updates or deletes a specific vehicle by its license plate
    path('vehicle/<str:license_plate>/', VehicleAPIView.as_view(), name='vehicle'),

    # GET: Retrieves all vehicles
    path('get_all_vehicles/', AllVehicleAPIView.as_view(), name='vehicle'),
]
