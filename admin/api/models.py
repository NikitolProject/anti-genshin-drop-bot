from django.db import models


class YouTuber(models.Model):

    class Meta:
        db_table = "YouTubers"
        verbose_name = "Ютуберы"
        verbose_name_plural = "Ютубер"

    username = models.CharField(max_length=255)
    url = models.CharField(max_length=1024)

    def username_tag(self: "YouTuber") -> str:
        return self.username

    username.short_description = "Ник ютубера"
    
    def __str__(self: "YouTuber") -> str:
        return self.username
