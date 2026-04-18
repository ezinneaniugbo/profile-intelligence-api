from django.urls import path
from profiles.views import ProfileListCreateView, ProfileDetailView

urlpatterns = [
    path('api/profiles/', ProfileListCreateView.as_view(), name='profiles-list-create'),
    path('api/profiles/<uuid:id>/', ProfileDetailView.as_view(), name='profiles-detail'),
]