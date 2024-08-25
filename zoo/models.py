from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True)

    def __str__(self):
        return self.name

class Animal(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='animals')
    image = models.ImageField(upload_to='animal_images/', null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.IntegerField()
    phone = models.CharField(max_length=10)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Booking(models.Model):
    heading = models.CharField(max_length=64)
    description = models.TextField()
    title = models.CharField(max_length=64)
    subtitle = models.TextField()
    points = models.JSONField()

    def __str__(self):
        return self.heading