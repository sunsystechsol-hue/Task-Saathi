from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework import exceptions, status
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from users.models import Users


# Custom Failure Class
class TokenBackendError(Exception):
    pass


class DetailDictMixin:
    def __init__(self, detail=None, code=None):
        """
        Builds a detail dictionary for the error to give more information to API
        users.
        """
        detail_dict = {"detail": self.default_detail, "code": self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict["detail"] = detail

        if code is not None:
            detail_dict["code"] = code

        super().__init__(detail_dict)


class AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed):
    pass


class TokenError(Exception):
    pass


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token is invalid or expired"
    default_code = "token_not_valid"


# Add more info to Token
class CustomTokenPairSerializer(TokenObtainPairSerializer):
    email = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField()
    
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, data):
        """
        Check if the user exists.
        """
        try:
            # Support both email and username fields, but prioritize email
            email = data.get('email') or data.get('username')
            if not email:
                raise serializers.ValidationError(
                    "Email or username is required"
                )
            
            user = Users.objects.get(email=email)
            if user.signInMethod != "email" and user.password is None:
                msg = "User is registered with Google SignIn"
                raise serializers.ValidationError(_(msg))
            if not user.is_active:
                raise serializers.ValidationError(
                    _("User is inactive")
                )
            if not user.isVerified:
                raise serializers.ValidationError(
                    _("User is not verified")
                )
            
            # Validate password manually since we're using email
            password = data.get('password')
            if not password or not user.check_password(password):
                raise serializers.ValidationError(
                    _("Invalid credentials")
                )
            
            token = RefreshToken.for_user(user)
            
            # Get company info if user is employer
            company = None
            if user.userRole == 'EMPLOYER':
                from tasksaathi.models import Company
                company_obj = Company.objects.filter(
                    userId=user
                ).first()
                if company_obj:
                    company = {
                        'id': str(company_obj.id),
                        'name': company_obj.name,
                        'isVerified': company_obj.isVerified
                    }
            
            data = dict()
            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            data['user'] = {
                'id': str(user.id),
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'userRole': user.userRole,
                'phoneNumber': user.phoneNumber,
                'profilePicture': user.profilePicture,
                'company': company
            }
            return data
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                _("Invalid email or password")
            )


# Add more info to Token
class AdminCustomTokenPairSerializer(TokenObtainPairSerializer):
    email = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField()
    
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, data):
        """
        Check if the user exists and is admin.
        """
        try:
            # Support both email and username fields
            email = data.get('email') or data.get('username')
            if not email:
                raise serializers.ValidationError(
                    "Email or username is required"
                )
            
            user = Users.objects.get(email=email)
            
            # Validate password manually since we're using email
            password = data.get('password')
            if not password or not user.check_password(password):
                raise serializers.ValidationError(
                    _("Invalid credentials")
                )
            
            if user.signInMethod != "email" and user.password is None:
                msg = "User is registered with Google SignIn"
                raise serializers.ValidationError(_(msg))
            if not user.is_active:
                raise serializers.ValidationError(
                    _("User is inactive")
                )
            if not user.isVerified:
                raise serializers.ValidationError(
                    _("User is not verified")
                )
            if not user.is_superuser or user.level != 5:
                raise serializers.ValidationError(
                    _("User is not an admin")
                )

            token = RefreshToken.for_user(user)
            data = dict()
            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            data['user'] = {
                'id': str(user.id),
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'is_superuser': user.is_superuser,
                'level': user.level
            }
            return data
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                _("Invalid email or password")
            )


# Get Token View
class LoginView(TokenObtainPairView):
    """
    Takes email and password as input  and returns an access type JSON web
    token and a refresh type JSON web token
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = CustomTokenPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# Get Token View
class AdminLoginView(TokenObtainPairView):
    """
    Takes email and password as input  and returns an access type JSON web
    token and a refresh type JSON web token.
    This view is only for admin users
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = AdminCustomTokenPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# class RefreshTokenView(TokenRefreshView):
#     # permission_classes = (AllowAny,)
#     # authentication_classes = ()
#     # serializer_class = TokenRefreshSerializer
#     # renderer_classes = [AtomicJsonRenderer]

#     # def post(self, request, *args, **kwargs):
#     #     serializer = self.serializer_class(data=request.data)
#     #     try:
#     #         serializer.is_valid(raise_exception=True)
#     #     except TokenError as e:
#     #         raise InvalidToken(e.args[0])
#     #     # obj =  User.objects.filter(email=request.data['email']).first()
#     #     # serializer.validated_data['email'] = obj.email
#     #     # serializer.validated_data['id'] = obj.id
#     #     # serializer.validated_data['firstName'] = obj.firstName
#     #     return Response(serializer.validated_data, status=status.HTTP_200_OK)
