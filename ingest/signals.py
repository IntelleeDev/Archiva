from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from .models import Profile, Content, Repository

"""
    Create a new user profile when a user is created
"""
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile = Profile(user=instance)
    profile.save()

"""
    Update the size of the Repository when a new file is added to it

"""
@receiver(post_save, sender=Content)
def update_repository_size(sender, instance, created, **kwargs):
    if not created:
        return
    repository = Repository.objects.get(pk=instance.repo_id)
    repository.repo_size =  repository.repo_size + int(instance.file.size)
    repository.save()

