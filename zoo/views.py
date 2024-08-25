from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Ticket, Animal, Category, Booking
from django.conf import settings
from django.contrib import messages
from instamojo_wrapper import Instamojo
from django.utils import timezone

api = Instamojo(
    api_key=settings.API_KEY,
    auth_token= settings.AUTH_TOKEN,
    endpoint= #InstamojoEndpoint
)

# Create your views here.
def index(request):
    now = timezone.localtime(timezone.now())
    opening_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    closing_time = now.replace(hour=19, minute=0, second=0, microsecond=0)
    is_open = opening_time <= now <= closing_time
    cat = Category.objects.all()
    booking = Booking.objects.all()
    animalcount = Animal.objects.count()
    return render(request, 'zoo/index.html', {
        'cat' : cat,
        'booking' : booking,
        'animalcount' : animalcount,
        'is_open': is_open,
        'now' : now
    })

def get_animals(request, category_id):
    animals = Animal.objects.filter(category_id=category_id)
    animals_data = [
         {
            'name': animal.name,
            'description': animal.description,
            'image_url': animal.image.url,
            'quantity' : animal.quantity
        }
        for animal in animals ]
    return JsonResponse({'animals': animals_data})

def payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        phone = request.POST.get('phone')

        # Name validation: Ensure name is provided
        if not name or not name.strip():
            messages.error(request, "Name is required.")
            return redirect('index')
            
        # Quantity validation: Ensure quantity is provided, is a number, and is positive
        if not quantity or not quantity.isdigit() or int(quantity) <= 0:
            messages.error(request, "Quantity must be atleast 1.")
            return redirect('index')

        # Phone validation: Ensure phone is provided and is a valid 10-digit number starting with 7,8 or 9
        if not phone or not phone.isdigit() or len(phone) != 10 or phone[0] not in ['7', '8', '9']:
            messages.error(request, "Phone number must be a valid 10-digit number.")
            return redirect('index')

        total = int(quantity) * 50
        response = api.payment_request_create(
            amount = str(total),
            purpose = "Ticket Booking",
            buyer_name = name,
            phone = phone,
            email = "test@test.com",
            redirect_url = "http://127.0.0.1:8000/zoo/ordersuccess"
        )
        ticket = Ticket(
            name = name,
            quantity = quantity,
            phone = phone,
            totalprice = total)
        ticket.save()
        return render(request, 'zoo/paymentpage.html', context = {
            'payment_url' : response['payment_request']['longurl']
        })
    return redirect('index')

def success(request):
    messages.success(request, 'Payment Successful.')
    return redirect('index')
