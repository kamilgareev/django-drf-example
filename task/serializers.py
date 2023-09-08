import pytz
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions
from .models import CustomUser as User
from django.contrib.auth import authenticate
from datetime import datetime
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        try:
            validate_password(password=validated_data.get('password'))
        except ValidationError as err:
            raise serializers.ValidationError({'password': err.messages})
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[EmailValidator],
        error_messages={'required': 'You must enter an email'}
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
        validators=[validate_password],
        error_messages={'required': 'You must enter a password'},
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class ValidateOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[EmailValidator],
        error_messages={'required': 'You must enter an email'}
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
        validators=[validate_password],
        error_messages={'required': 'You must enter a password'},
    )
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        otp = data.get('otp')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password"'
            raise serializers.ValidationError(msg, code='authorization')

        if not otp:
            msg = 'Must include "otp"'
            raise serializers.ValidationError({'otp': 'Must include otp'})

        if user.otp == otp and user.otp_valid_until >= datetime.now(tz=pytz.UTC):
            data['user'] = user
            return data
        else:
            msg = 'Invalid otp or otp expired'
            raise serializers.ValidationError(msg, code='authorization')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            if not user.is_admin:
                raise serializers.\
                    ValidationError({'authorize': 'You are now allowed to perform this action'})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']

        instance.save()
        return instance

