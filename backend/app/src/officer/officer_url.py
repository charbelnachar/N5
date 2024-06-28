from django.urls import path

from app.src.officer.officer_view import OfficerAPIView, AllOfficerAPIView, CreateOfficerAPIView

urlpatterns = [
    # GET: Retrieves all officers
    path('all_officer/', AllOfficerAPIView.as_view(), name='officer'),

    # POST: Creates a new officer
    path('officer/', CreateOfficerAPIView.as_view(), name='officer_detail'),

    # GET, PUT, DELETE: Retrieves, updates or deletes a specific officer by its identifier
    path('officer/<str:identifier>/', OfficerAPIView.as_view(), name='officer_detail'),
]