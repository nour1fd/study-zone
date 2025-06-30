from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Topic(models.Model):
    """Model definition for Topic."""

    # TODO: Define fields here
    name=models.CharField( max_length=50)


    class Meta:
        """Meta definition for Topic."""

        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        """Unicode representation of Topic."""
        return self.name


class Room(models.Model):
    """Model definition for Room."""

    # TODO: Define fields here
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField( max_length=50)
    participants=models.ManyToManyField(User, related_name="participants",blank=True)
    description=models.TextField(null=True,blank=True)
    update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Room."""
        ordering= ['-update','-created']

        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        """Unicode representation of Room."""
        return self.name
    

class Message (models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     room=models.ForeignKey(Room,on_delete=models.CASCADE)
     body=models.TextField()
     update=models.DateTimeField(auto_now=True)
     created=models.DateTimeField(auto_now_add=True)

     class Meta:
        """Meta definition for Room."""
        ordering= ['-update','-created']

 
    #  class Meta:
    #      verbose_name = _("")
    #      verbose_name_plural = _("s")
 
     def __str__(self):
         return self.body[0:50]
    #  def get_absolute_url(self):
    #      return reverse("_detail", kwargs={"pk": self.pk})
 

 