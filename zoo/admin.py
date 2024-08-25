from django.contrib import admin
from .models import Animal, Category, Ticket, Booking

# Register your models here.

admin.site.register(Animal)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Booking)
