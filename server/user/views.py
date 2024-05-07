import logging
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from user import serializers, models
import random
logger = logging.getLogger(__name__)
def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = models.User.objects.raw('SELECT * FROM user WHERE email = %s AND password = %s', [email, password])

    if user:
        tokens = get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        res.data = tokens
        res["X-CSRFToken"] = csrf.get_token(request)
        logger.info("Successful login for email: %s", email)
        return res
    logger.warning("Login failed for email: %s", email)
    raise rest_exceptions.AuthenticationFailed("Email or Password is incorrect!")
# @rest_decorators.api_view(["POST"])
# @rest_decorators.permission_classes([])
# def registerView(request):
#     serializer = serializers.RegistrationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     if user != None:
#         # Vulnerability: XSS
#         return response.Response("Registered!<script>alert('XSS Attack');</script>")
#     logger.warning("Registration failed for email: %s", serializer.validated_data["email"])
#     return rest_exceptions.AuthenticationFailed("Invalid credentials!")

# Register view
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def registerView(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    if user != None:
        # Vulnerability: XSS
        # Injecting a script tag into the response
        return response.Response("Registered!<script>alert('XSS Attack');</script>")
    logger.warning("Registration failed for email: %s", serializer.validated_data["email"])
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")

@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()
        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"] = None
        return res
    except Exception as e:
        logger.error("Error during logout: %s", str(e))
        raise rest_exceptions.ParseError("Invalid token")
class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')
class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except models.User.DoesNotExist:
        return response.Response(status_code=404)
    serializer = serializers.UserSerializer(user)
    return response.Response(serializer.data)

@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def list_events(request):
    print("here")
    events = models.Event.objects.all()
    print(events)
    serializer = serializers.EventSerializer(events, many=True)
    return response.Response(serializer.data)

@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def list_tasks(request):
    try:
        tasks = models.Tasks.objects.filter(assignee=request.user)
        serializer = serializers.TaskSerializer(tasks, many=True)
        return response.Response(serializer.data)
    except Exception as e:
        print("Error", e)

def generate_random():
    return random.randint(1, 64)