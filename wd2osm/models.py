from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    wd_p31 = models.IntegerField()


class Alignment(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    wd_item = models.IntegerField()
