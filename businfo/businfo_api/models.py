from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class BusInfo(models.Model):
    BusID = models.IntegerField()
    Info = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.BusID}"

    def exists(self):
        return BusInfo.objects.filter(BusID=self.BusID).exists()

    def update_info(self, info):
        self.Info = info
        self.save()
