from django.db import models


class Cinema(models.Model):
    region = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=20)
    tel = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=50)
    x = models.CharField(max_length=50)
    y = models.CharField(max_length=50)
    url = models.URLField(max_length=250)
    public = models.TextField(blank=True, null=True)
    parking = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, default='기타')
    img = models.URLField(max_length=250, blank=True, null=True)
    score = models.FloatField(blank=True, default=0)

