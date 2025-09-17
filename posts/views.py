from django.shortcuts import render
from .serializers import PostSerializer,CommentSerializer
from .models import PostModel,CommentModel
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# Create your views here.

class IsOwnerOnly(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        return obj.user==request.user


class PostView(viewsets.ModelViewSet):
    queryset=PostModel.objects.all().select_related()
    serializer_class=PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['user']


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        if self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsOwnerOnly()]
        return [permissions.IsAdminUser()]
    @action(detail=True, methods=['POST'],permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object() 
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)  
            liked = False
        else:
            post.likes.add(user) 
            liked = True

        return Response({'liked': liked, 'like_count': post.likes.count()})
    
    def perform_create(self, serializer):
     serializer.save(user=self.request.user)



class CommentView(viewsets.ModelViewSet):
    queryset=CommentModel.objects.all().select_related()
    serializer_class=CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['post']
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        if self.request.method =='POST':
            return [permissions.IsAuthenticated()]
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsOwnerOnly()]
        return [permissions.IsAdminUser()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


