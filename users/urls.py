from django.urls import path

from .views import KakaoSignInView, UserDetailView

urlpatterns = [
    path('/kakaosignin', KakaoSignInView.as_view()),
    path('/detail', UserDetailView.as_view()),
]