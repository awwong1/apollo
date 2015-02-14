from django.db import models


class TermsOfService(models.Model):
    last_modified = models.DateTimeField(
        auto_now=True, help_text="When was this terms of service created?"
    )
    title = models.CharField(
        max_length=255, help_text="What is the title of this terms of service document?"
    )
    content = models.TextField(
        help_text="What is the content of this terms of service document?"
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
