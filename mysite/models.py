from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class auth_help( models.Model ):
  #i had to make this model so that i could create a permission.
  #this is the permission that determines whether a user can use
  #the app. it is called 'psu_gcal', so referencing it is: psu_gcal.psu_gcal
  field = models.CharField( max_length=1 )
  class Meta:
    permissions = (
      ( 'psu_gcal', 'can use the app' ),
    )
