
from .models import MessageModel
from rest_framework import serializers
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=MessageModel
        fields=['id','message','receiver','sender','is_read']
        read_only_fields=['id','sender']