from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'', include('app.src.person.person_url')),
    re_path(r'', include('app.src.vehicle.vehicle_url')),
    re_path(r'', include('app.src.officer.officer_url')),
    re_path(r'', include('app.src.violation.violation_url')),
]
