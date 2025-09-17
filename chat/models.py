
from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your models here.
class MessageModel(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_messages')
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_read=models.BooleanField(default=False)

    def __str__(self):
        return f"message send by {self.sender.full_name} to {self.receiver.full_name}"