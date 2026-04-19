from django.urls import path
from profiles.views import ProfileListCreateView, ProfileDetailView


urlpatterns = [
    path('', ProfileListCreateView.as_view()),        # /api/profiles/
    path('<uuid:id>/', ProfileDetailView.as_view()),  # /api/profiles/<id>/
]