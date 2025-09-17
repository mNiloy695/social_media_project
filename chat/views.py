from django.shortcuts import render
from .serializers import MessageSerializer
from .models import MessageModel
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# Create your views here.
class IsOwnerOnlyMessage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender==request.user

class MessageView(viewsets.ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class=MessageSerializer
    def get_queryset(self):
        user=self.request.user
        return self.queryset.filter(
            Q(sender=user) | Q(receiver=user)
        )
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        if self.request.method=='POST':
            return [permissions.IsAuthenticated()]
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [permissions.IsAuthenticated(),IsOwnerOnlyMessage()]
        return [permissions.IsAdminUser()]
    # def get_queryset(self):
    #     return MessageModel.objects.none() 
    
    @action(detail=False,methods=['get'],url_path='conversation/(?P<user_id>\d+)',permission_classes=[permissions.IsAuthenticated])
    def conversation(self,request,user_id=None):
        user=request.user
        messages=MessageModel.objects.filter(
            Q(sender=user,receiver_id=user_id) | Q(sender_id=user_id,receiver=user)
        ).order_by('-timestamp')
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)