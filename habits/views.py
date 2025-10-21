from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner
from .pagination import HabitPagination
from drf_yasg.utils import swagger_auto_schema


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

    @swagger_auto_schema(
        operation_description="Получить, обновить или удалить привычку пользователя",
        operation_summary="Детали привычки"
    )
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.none()


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination

    @swagger_auto_schema(
        operation_description="Получить список публичных привычек",
        operation_summary="Публичные привычки"
    )
    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
