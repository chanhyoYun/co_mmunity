from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/withdraw/', views.WithdrawView.as_view(), name='withdraw'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('follow/{user_id}', views.FollowView.as_view(), name='follow_view'),
]