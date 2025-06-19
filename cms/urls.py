from django.urls import path
from .views import RegisterView, LoginView, ContentListCreateView, ContentDetailView , ApiRootView

urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),  
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('content/', ContentListCreateView.as_view()),
    path('content/<int:pk>/', ContentDetailView.as_view()),
    
]