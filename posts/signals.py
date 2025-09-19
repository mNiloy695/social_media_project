from .models import PostModel,Notification
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save,sender=PostModel)
def notification(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(
            title="New Post Created",
            post=instance

        )

