from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import ParkingSpot
from .forms import ReservationForm, UserForm, ProfileForm


@login_required(login_url='/login')
def map(request):

    spots = ParkingSpot.objects.all()
    
    return render(request, 'map.html', {'spots': spots})


@login_required(login_url='/login')
def reserve(request, spot_id):
    # only allow if logged in
    spot = get_object_or_404(ParkingSpot, id=spot_id)
    form = ReservationForm(request.POST or None)

    if spot.reservation_owner == request.user:
        return render(request, 'spot.html', {'form': form, 'spot': spot})

    if spot.reservation_owner != None:
        return HttpResponseRedirect('/')
    
    if form.is_valid():
        spot.reservation_owner = request.user
        spot.reserved_until = form.cleaned_data['reserved_until']
        spot.clean()
        spot.save()
        return HttpResponseRedirect('/')

    return render(request, 'spot.html', {'form': form, 'spot': spot})


@login_required(login_url='/login')
def delete_reservation(request, spot_id):
    # Delete the reservation for spot_id if it's owned by the user
    
    spot = get_object_or_404(ParkingSpot, id=spot_id)
    if spot.reservation_owner == request.user:
        spot.reservation_owner = None
        spot.reserved_until = '1994-07-13 00:00'
        spot.save()
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    form = UserForm(request.POST)
    # profile_form = ProfileForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        # profile_form.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    context = {
        "form": form,
        # 'profile_form': profile_form
    }
    return render(request, 'register.html', context)

