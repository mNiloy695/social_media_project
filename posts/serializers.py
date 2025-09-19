from .models import PostModel,CommentModel,Notification
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    like_count =serializers.SerializerMethodField()
    class Meta:
        model=PostModel
        fields=['id','content','image','is_public','like_count','user']
        read_only_fields=['like_count','user']
    def get_like_count(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentModel
        fields="__all__"
        read_only_fields=['user']



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields='__all__'
        read_only_fields=['id','post','created_at','updated_at','title']