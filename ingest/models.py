from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from ingest.utils import change_upload_path


# Create your models here.

# User profile information
@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    interest = models.CharField(max_length=100, null=True)
    occupation = models.CharField(max_length=30, null=True)

    # sets the field of interest
    def set_interest(self, interest):
        self.interest = interest

    # sets the occupation
    def set_occupation(self, occupation):
        self.occupation = occupation

    # string representation of the model
    def __str__(self):
        return 'Username: %s, Occupation: %s' % (self.user, self.occupation)


# Keeps track of account logs
@python_2_unicode_compatible
class AccountLog(models.Model):
    acc_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    time_in = models.TimeField()
    time_out = models.TimeField()
    date = models.DateField(null=True)

    # string representation of the Account log
    def __str__(self):
        return 'User: %s, Time in: %s, Time out %s' % (self.acc_user, self.time_in, self.time_out)


# Class represents an archive repository
@python_2_unicode_compatible
class Repository(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    repo_size = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=True)

# Class represents the Archive Content
@python_2_unicode_compatible
class Content(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, null=True)
    content_name = models.CharField(max_length=100)
    repo_name = models.CharField(max_length=30, null=True)
    file = models.FileField(upload_to=change_upload_path, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # string representation of the content
    def __str__(self):
        return '%s' % self.content_name


# Class represents content metadata
@python_2_unicode_compatible
class ContentMetadata(models.Model):
    content = models.OneToOneField(Content, primary_key=True)
    file_type = models.CharField(max_length=20)
    file_size = models.IntegerField(default=0)
    date_uploaded = models.DateTimeField(auto_now=True)
    meta_tags = models.CharField(max_length=100)
    description = models.TextField()
    permissions = models.TextField()

    # sets meta tags
    def set_meta_tags(self, tags=None):
        if type(tags) != type([]):
            return
        self.meta_tags = ','.join(tags)


# Class to represent uploaded files
class Upload(models.Model):
    title = models.CharField(max_length=40)
    uploaded_file = models.FileField(upload_to=settings.MEDIA_ROOT)
