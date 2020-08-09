from django.urls import path
from UserProfile.views import UserProfileView

urlpatterns = [
    path('<username>/', UserProfileView.as_view(),name='single_profile'),
]