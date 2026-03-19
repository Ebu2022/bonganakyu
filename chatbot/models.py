from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models


class FAQ(models.Model):
    answer = models.TextField()

    keywords = models.CharField(
        max_length=255,
        help_text="Comma separated keywords (e.g fees, payment, exam)"
    )

    def __str__(self):
        return self.keywords


class Navigation(models.Model):
    place = models.CharField(max_length=255)
    description = models.TextField()

    # ✅ FIXED: Cloudinary image field
    image = CloudinaryField('image', blank=True, null=True)

    # ✅ KEEP ONLY ONE keywords field
    keywords = models.CharField(
        max_length=255,
        help_text="Comma separated keywords"
    )

    def __str__(self):
        return self.place


class AttachmentOpportunity(models.Model):
    degree_programme = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.degree_programme} - {self.company_name}"


class ChatLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.TextField()
    response_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.message[:40]}"
