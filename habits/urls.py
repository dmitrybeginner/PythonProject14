from django.urls import path
from .views import (
    HabitListCreateView,
    HabitDetailView,
    PublicHabitListView,
)

urlpatterns = [
    path('habits/public/', PublicHabitListView.as_view(), name='public-habit-list'),
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
]
