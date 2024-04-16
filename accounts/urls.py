from dj_rest_auth.registration.views import RegisterView
from django.urls import include, path
from accounts.views import SignUpAPIView, AuthAPIView

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    path('signup/', SignUpAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
]