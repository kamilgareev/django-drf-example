from django.urls import path, include
from .views import *


urlpatterns = [
    path('', homepage),
    path('auth/register/', RegisterView.as_view(),
         name='register'),
    path('auth/login-with-otp/', LoginWithOTPView.as_view(),
         name='login-with-otp'),
    path('auth/validate-otp/', ValidateOTPView.as_view(),
         name='validate-otp'),
    path('auth/logout/', LogoutView.as_view(),
         name='logout'),
    path('users/', UserListView.as_view(),
         name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(),
         name='user-detail'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(),
         name='user-delete'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(),
         name='user-update'),
]



















# from django.urls import path, include, re_path
# from .views import *
# from rest_framework import routers
#
# router = routers.SimpleRouter()
# router.register(r'users', UserViewSet)
#
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('auth/', include('djoser.urls')),
#     path('auth/login/', LoginView.as_view()),
#     # re_path(r'^auth/', include('djoser.urls.authtoken')),
# ]
