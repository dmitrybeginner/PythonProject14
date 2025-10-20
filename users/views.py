from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema


class UserCreateView(generics.CreateAPIView):
    """Представление для создания (регистрации) нового пользователя."""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        operation_summary="Регистрация пользователя"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
