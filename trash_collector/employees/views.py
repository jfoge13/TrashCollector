# from trash_collector.customers.views import one_time_pickup
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import Employee
import datetime
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        
        Customer = apps.get_model('customers.Customer')
        matching_zip = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        # some_list =[]
        # for thing in matching_zip:
        #     if thing.weekly_pickup == today.strftime("%A"):
        #         if thing in some_list:

        weekly_filter = matching_zip.filter(weekly_pickup = today.strftime("%A"))
        day_filter = matching_zip.filter(one_time_pickup = today.strftime("%Y-%m-%d"))
        # weekly_suspend_filter = weekly_filter.exclude(Customer.suspend_end < today.strftime("%Y-%m-%d"))
        # day_suspend_filter = day_filter.exclude(Customer.suspend_end < today.strftime("%Y-%m-%d"))

        some_list = []
        for customer in weekly_filter:
            if today > customer.suspend_end or today < customer.suspend_start:
                some_list.append(customer)
        for customer in day_filter:
            if today > customer.suspend_end or today < customer.suspend_start:
                some_list.append(customer)


        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'some_list': some_list,
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))



def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

def matching_zipcodes(request):
    logged_in_user = request.user
    Customer = apps.get_model('customers.Customer')
    matching_zip = Customer.objects.filter(logged_in_user.zip_code == Customer.zip_code)
    context = {
        'matching_zip': matching_zip
    }
    return render(request, 'employees/matching_zipcodes.html', context)

# def matching_zipcodes(request):
#     user = request.user
#     employee = Employee.objects.get(user_id=user.id)
#     Customer = apps.get_model('customers.customer')
#     customers = Customer.objects.all()
#     matching_zipcode = []
#     for customer in customers:
#         if customer.zip_code == employee.zip_code:
#             matching_zipcode.append(customer)

#     return render(request, 'employees/index.html')

