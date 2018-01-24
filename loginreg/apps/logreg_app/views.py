# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request):
    return render(request, 'logreg_app/index.html')

def register(request):
    errors = User.objects.registration_validation(request.POST)
    if len(errors): #there are errors
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        person = User.objects.create(
        name = request.POST['name'],
        alias = request.POST['alias'],
        password = request.POST['password'],
        email_address = request.POST['email'])
        request.session['name'] = request.POST['name']
        request.session['id'] = person.id
        return redirect ('/display')

def login(request):
    errors = User.objects.user_validation(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        logged_in_user = User.objects.get(email_address=request.POST['email'])
        print logged_in_user
        request.session['name'] = logged_in_user.name
        request.session['id'] = logged_in_user.id
        return redirect ('/display')

def display(request):
    context = {
        'users' :User.objects.all(),
        'trips' : Trip_Created.objects.filter(joined_by=User.objects.get(id=request.session['id'])),
        'other_trips': Trip_Created.objects.exclude(joined_by=User.objects.get(id=request.session['id']))
    }
    return render(request, 'logreg_app/display.html', context)

def logout(request):
    request.session.clear()
    return redirect ('/')
# Create your views here.

def add(request):
    return render(request, 'logreg_app/add_trip.html')

def create(request):
    if request.method == 'POST':
        errors = Trip_Created.objects.trip_validation(request.POST)
        if len(errors):  # if there's errors -- see models.py for error list!
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('users:add'))
        else:
            user = User.objects.get(id=request.session['id'])
            trip = Trip_Created.objects.create(
                destination = request.POST['destination'],
                description = request.POST['description'],
                travel_start = request.POST['travel_start'],
                travel_end = request.POST['travel_end'],
                created_by=user
            )
            trip.joined_by.add(user)
            trip.save()
            return redirect(reverse('users:display'))
    else:
        return redirect(reverse('users:display'))

# def show(request, user_id):
#     context = {
#         'trip' : Add_trip.objects.get(id=user_id)
#     }
#     return render(request, 'logreg_app/display.html', context)

def join(request, trip_id):
    user = User.objects.get(id=request.session['id'])
    trip = Trip_Created.objects.get(id=trip_id)
    trip.joined_by.add(user)
    trip.save()
    return redirect('/display')


def leave(request, trip_id):
    user = User.objects.get(id=request.session['id'])
    trip = Trip_Created.objects.get(id=trip_id)
    trip.joined_by.remove(user)
    trip.save()
    return redirect('/display')

def info(request, trip_id):
    trip = Trip_Created.objects.get(id=trip_id)
    context = {

        'trip': trip,
        'other_users' : User.objects.exclude(created_trips__created_by=trip.created_by)
    }
    return render(request, 'logreg_app/destination.html', context)