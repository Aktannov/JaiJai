from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    password = serializers.CharField(required=True, min_length=6)
    password_confirmation = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Адрес почты занят')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self):
        attrs = self.validated_data
        user = User.objects.create_user(**attrs)
        code = user.generate_activation_code()
        user.send_registration_mail(user.email)
        user.send_activation_mail(user.email, code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation = serializers.CharField(required=True, min_length=8, max_length=8)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('пожалуйста зарегайтесь')
        return email

    def validate_activation(self, activation):
        if not User.objects.filter(activation=activation).exists():
            raise serializers.ValidationError('пожалуйста зарегайтесь')
        return activation

    def validate(self, attrs):
        email = attrs.get('email')
        activation = attrs.get('activation')
        if not User.objects.filter(email=email, activation=activation).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=6)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('пожалуйста зарегайтесь')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Пороль или email непраильный')
        else:
            raise serializers.ValidationError('Заполните все поля')
        attrs['user'] = user
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.generate_activation_code()
        send_mail(
            'Восстановление пароля',
            f'Ваш код подтверждения: {user.activation}',
            'test@gmail.com',
            [email]
        )

class ForgotPasswordFinalSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    forgotcode = serializers.CharField(required=True, min_length=8, max_length=8)
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('пожалуйста зарегайтесь')
        return email

    def validate_forgotpassword(self, forgotcode):
        if not User.objects.filter(activation=forgotcode).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return forgotcode

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_pass(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()

