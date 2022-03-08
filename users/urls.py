from django.urls import path

from .views import KakaoSignInView

urlpatterns = [
    path('/kakaosignin', KakaoSignInView.as_view()),
    # path('/stats', UserStatView.as_view()),
]