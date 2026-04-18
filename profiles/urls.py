from django.urls import path
from profiles.views import ProfileListCreateView, ProfileDetailView

urlpatterns = [
    path('api/profiles', ProfileListCreateView.as_view()),
    path('api/profiles/', ProfileListCreateView.as_view()),

    path('api/profiles/<uuid:id>', ProfileDetailView.as_view()),
    path('api/profiles/<uuid:id>/', ProfileDetailView.as_view()),
]