from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, \
    IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, \
    ValidateOTPSerializer, UserSerializer, UserUpdateSerializer
from rest_framework import generics
from .models import CustomUser as User
from .utils import generate_otp
from .tasks import send_otp_email_celery
from django.contrib.auth import login, logout
from .permissions import IsNotAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsNotAuthenticated]
    serializer_class = RegisterSerializer


class LoginWithOTPView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        email = user.email

        otp, otp_valid_until = generate_otp()
        user.otp = otp
        user.otp_valid_until = otp_valid_until
        user.otp_sent = True
        user.save()

        send_otp_email_celery.delay(email, otp)

        return Response({'message': 'OTP has been sent to your email'},
                        status=status.HTTP_200_OK)


class ValidateOTPView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = ValidateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user.otp = None
        user.otp_valid_until = None
        user.otp_sent = False

        login(request, user)
        return Response({'message': 'Successfully logged in'},
                        status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'},
                        status=status.HTTP_200_OK)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.email != instance.email:
            if not request.user.is_admin:
                return Response({'message': 'You are now allowed to perform this action'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            self.perform_destroy(instance)
            return Response({'message': 'User deleted successfully '},
                            status=status.HTTP_200_OK)


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer


from django.http import HttpResponse


def homepage(request):
    html = f'''
    <head>
        <link rel="shortcut icon" href="#" />
    </head>
    <html>
        <body>
            <h1>Homepage</h1>
        </body>
    </html>
    '''
    return HttpResponse(html)
