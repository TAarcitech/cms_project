from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import filters
from django.contrib.auth import authenticate
from .models import Content
from .serializers import UserSerializer, ContentSerializer
from .permissions import IsAuthorOrAdmin
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer




class ApiRootView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the CMS API.",
            "register": "/api/register/",
            "login": "/api/login/",
            "content": "/api/content/"
        })

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer

    # def post(self, request):
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     user = authenticate(username=username, password=password)
    #     if user:
    #         token, _ = Token.objects.get_or_create(user=user)
    #         return Response({'token': token.key})
    #     return Response({'error': 'Invalid credentials'}, status=400)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'role': user.role,
        })

class ContentListCreateView(generics.ListCreateAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'summary', 'categories']

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Content.objects.all()
        return Content.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]
    queryset = Content.objects.all()