from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone
# Create your models here.
class Item(models.Model):
    class Meta:
        indexes = [
           models.Index(fields=['user_name','item_price']),
        ]
    def __str__(self):
        return self.item_name
    
    def get_absolute_url(self):
        return reverse('myapp:index')
    
    def delete(self,using=None,keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    item_name = models.CharField(max_length=200,db_index=True)
    item_desc = models.TextField()
    item_price = models.IntegerField(db_index=True)
    item_image = models.ImageField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ItemManager()
    all_objects = models.Manager()

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True) 