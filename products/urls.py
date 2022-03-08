from django.urls import path

from .views import OrderView, CommentView, LikeView, ProductListView, ProductView

urlpatterns = [
    path('/<int:course_id>/order', OrderView.as_view()),
    path('/like', LikeView.as_view()),
    path('/detail/<int:course_id>', ProductView.as_view()),
    path('/<int:course_id>/comments', CommentView.as_view()),
    path('', ProductListView.as_view()),
]