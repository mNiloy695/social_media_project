from django.urls import path,include
from .views import PostView,CommentView,NotificationView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register('list',PostView)
router.register('comment',CommentView)


urlpatterns = [
    path('',include(router.urls)),
    path('notification/',NotificationView.as_view()),
]
