from django.db import models
from django.db.models import UniqueConstraint
import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name    

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    LOCATION_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHITTAGONG', 'Chittagong'),
        ('KHULNA', 'Khulna'),
        ('RAJSHAHI', 'Rajshahi'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('RANGPUR', 'Rangpur'),
        ('MYMENSINGH', 'Mymensingh'),
    ]
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_event = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="RSVP", related_name="events")
    image = CloudinaryField("image", null=True, blank=True)
    # image = models.ImageField("/events/", null=True, blank=True)

    def __str__(self):
        return self.name

class RSVP(models.Model):  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    response = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'event'], name='unique_user_event_rsvp')
        ]

    def __str__(self):
        return f"{self.user.username} RSVP for {self.event.title} - {self.response}"
