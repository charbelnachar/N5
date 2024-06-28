from django.urls import include, path

from app.src.violation.violationView import ReportViolationView, ViolationAPIView, CreateViolationView, \
    GetAllViolationAPIView

urlpatterns = [
    # Get:Get violations for a person based on their email
    path('generar_informe/', ReportViolationView.as_view(), name='create_violation'),

    # POST: Creates a new violation
    path('cargar_infraccion/', CreateViolationView.as_view(), name='create_violation'),

    # GET, PUT, DELETE: Retrieves, updates or deletes a specific violation by its ID
    path('infraccion/<int:violation_id>/', ViolationAPIView.as_view(), name='violation_list_create'),

    # GET: Retrieves all violations
    path('get_all_infraccion/', GetAllViolationAPIView.as_view(), name='violation_list_create'),
]
