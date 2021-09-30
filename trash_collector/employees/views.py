# from trash_collector.customers.views import one_time_pickup
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import Employee



def index(request):
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        
        Customer = apps.get_model('customers.Customer')

        # Filters customers based on zip code, pick up day, and suspension status
        matching_zip = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        weekly_filter = matching_zip.filter(weekly_pickup = today.strftime("%A"))
        one_time_filter = matching_zip.filter(one_time_pickup = today.strftime("%Y-%m-%d"))
        complete_filter = []
        for customer in weekly_filter:
            if customer.suspend_end == None and customer.suspend_end == None:
                complete_filter.append(customer)
            elif today > customer.suspend_end or today < customer.suspend_start:
                complete_filter.append(customer)
            else:
                pass
        for customer in one_time_filter:
            if customer.suspend_end == None and customer.suspend_end == None:
                complete_filter.append(customer)
            elif today > customer.suspend_end or today < customer.suspend_start:
                complete_filter.append(customer)   
            else:
                pass
        for customer in complete_filter:
            if customer.date_of_last_pickup == today:
                complete_filter.remove(customer)
        if len(complete_filter) == 1:
            for customer in complete_filter:
                if customer.date_of_last_pickup == today:
                    complete_filter.clear()

        # Sends a list of customers with weekly pickup through context to be displayed on index.html after a search
        search_results = []
        if request.method == "POST":
            search_from_form = request.POST.get('index')
            customer_list = []
            customer_list.append(Customer.objects.all())
            search_results = Customer.objects.filter(weekly_pickup = search_from_form)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'complete_filter': complete_filter,
            'search_results': search_results
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

def confirm(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer_update = Customer.objects.get(pk=customer_id)
    customer_update.balance += 20.00
    customer_update.date_of_last_pickup = date.today()
    customer_update.save()
    return HttpResponseRedirect(reverse('employees:index'))