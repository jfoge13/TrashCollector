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
            if customer.suspend_end == None and customer.suspend_end == None:
                some_list.append(customer)
            elif today > customer.suspend_end or today < customer.suspend_start:
                some_list.append(customer)
            else:
                pass
        for customer in day_filter:
            if customer.suspend_end == None and customer.suspend_end == None:
                some_list.append(customer)
            elif today > customer.suspend_end or today < customer.suspend_start:
                some_list.append(customer)   
            else:
                pass
        for customer in some_list:
            if customer.date_of_last_pickup == today:
                some_list.remove(customer)
        if len(some_list) == 1:
            for customer in some_list:
                if customer.date_of_last_pickup == today:
                    some_list.clear()
        # counter = 0
        # while counter < len(some_list) + 1:
        #     if customer.date_of_last_pickup == today:
        #         some_list.remove(customer)
        #     counter += 1

        # while some_list != []:
        #     for customer in some_list:
        #         if customer.date_of_last_pickup == today:
        #             some_list.remove(customer)
        results = []
        if request.method == "POST":
            search_from_form = request.POST.get('index')
            customer_list = []
            customer_list.append(Customer.objects.all())
            # for customer in customer_list:
            #     if search_from_form != customer.weekly_pickup:
            #         customer_list.remove(customer)
            results = Customer.objects.filter(weekly_pickup = search_from_form)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'some_list': some_list,
            'results': results
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

# def matching_zipcodes(request):
#     logged_in_user = request.user
#     Customer = apps.get_model('customers.Customer')
#     matching_zip = Customer.objects.filter(logged_in_user.zip_code == Customer.zip_code)
#     context = {
#         'matching_zip': matching_zip
#     }
#     return render(request, 'employees/matching_zipcodes.html', context)

def confirm(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer_update = Customer.objects.get(pk=customer_id)
    customer_update.balance += 20.00
    customer_update.date_of_last_pickup = date.today()
    customer_update.save()
    return HttpResponseRedirect(reverse('employees:index'))

# def search_day(request):
#     if request.method == "POST":
#         Customer = apps.get_model('customers.Customer')
#         search_from_form = request.POST.get('search_day')
#         customer_list = []
#         customer_list.append(Customer.objects.all())
#         # for customer in customer_list:
#         #     if search_from_form != customer.weekly_pickup:
#         #         customer_list.remove(customer)
#         results = Customer.objects.filter(weekly_pickup = search_from_form)
#         context = {
            
#         }
    

    # if search_from_form == 
    #     return HttpResponseRedirect(reverse('customers:index'))
# def confirm(request, customer_id):
#     Customer = apps.get_model('customers.Customer')
#     customer = Customer.objects.get(pk=customer_id)
#     customer.date_of_last_pickup = date.today()
#     # some_list.remove(customer)
#     return HttpResponseRedirect(reverse('employees:index'))


#     return HttpResponseRedirect(reverse('employees:index'))
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

