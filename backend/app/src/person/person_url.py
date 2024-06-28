from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.src.person.person_view import PersonAPIView, CreatePersonAPIView, AllPersonAPIView, PersonEmailAPIView

urlpatterns = [
    # GET: Retrieves a person's details by their email.
    path('person_by_email/<str:email>/', PersonEmailAPIView.as_view(), name='person'),

    # GET, PUT, DELETE: Retrieves, updates or deletes a specific person's details by their identifier.
    path('person/<int:identifier>/', PersonAPIView.as_view(), name='person_detail'),

    # POST: Creates a new person.
    path('person/', CreatePersonAPIView.as_view(), name='person'),

    # GET: Retrieves the details of all persons.
    path('all_person/', AllPersonAPIView.as_view(), name='person'),
]
