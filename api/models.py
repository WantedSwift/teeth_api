from django.db import models
from django.utils.timezone import now
# Create your models here.
class users(models.Model):


    email = models.CharField(max_length=200,default="")
    token = models.CharField(max_length=300)
    id_apple = models.CharField(max_length=300)
    fb_token = models.CharField(max_length=200)
    is_active = models.IntegerField(default=0)
    balance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_date = models.DateTimeField(default=now, editable=False)


    def __str__(self):
     return str(self.email)