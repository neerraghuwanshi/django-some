from django.urls import path

from .views import BettingListView


urlpatterns = [
    path('', BettingListView.as_view(), name='betting'),
]