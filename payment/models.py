from django.db import models
from django.conf import settings

# Create your views here.

class BillAdd(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=264, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=30, blank=True)
    contry = models.CharField(max_length=20, blank=True)
    

    def __str__(self) -> str:
        return f'{self.user.profile.username} Billing Address'

    def is_fully_filled(self):
        fields = [f.name for f in self._meta.get_fields()]

        for field in fields:
            value = getattr(self, field)
            if value is None or value =="":
                return False
        return True
    
    class Meta:
        verbose_name_plural = "Billling Addresses"
