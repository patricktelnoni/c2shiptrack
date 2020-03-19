from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests, json
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


from .forms import *

def room(request, room_name):
    return render(request, 'maps/room.html', {
        'room_name': room_name
    })

def index(request):
    return render(request, 'maps/index.html', {})\

def login_form(request):
    return render(request, 'maps/form_login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/maps')

def lokasi_form(request):
    form = LokasiForm()
    return render(request, 'maps/lokasi_form.html', {'form':form})

def user_form(request):
    userForm = UserForm()
    lokasiForm = LokasiUserForm

    return render(request, 'maps/user_form.html', {'user_form':userForm, 'lokasi_form': lokasiForm})

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'maps/dashboard.html')
    else:
        return HttpResponseRedirect('/maps')

def process_login(request):
    username = request.POST['username']
    password = request.POST['password']
    checkAuthenticated = requests.get('http://127.0.0.1:8000/api/login/'+username+'/'+password+'', params=request.GET)
    if len(checkAuthenticated.content) > 0:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('index')
    else:
        return redirect('index')
def process_user(request):
    username    = request.POST['username']
    password    = request.POST['password']
    nama        = request.POST['nama']
    lokasi      = request.POST['lokasi']
    data_user = {
        "username": username,
        "password": password,
        "nama": nama,
        "lokasi": lokasi,
    }
    print(data_user)

    # save into patient table of another project
    createLokasi = requests.post('http://127.0.0.1:8000/api/login/', data=data_user)
    return redirect('form_user')

def list_lokasi(request):
    # .get('https://api.coindesk.com/v1/bpi/currentprice.json')
    lokasi = requests.get('http://127.0.0.1:8000/api/lokasi/').content

    return render(request, "maps/list_lokasi.html")

def list_session(request):
    # .get('https://api.coindesk.com/v1/bpi/currentprice.json')

    return render(request, "maps/session_list.html")

def list_user(request):
    return render(request, "maps/user_list.html")


@csrf_protect
def process_lokasi(request):
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    lokasi = request.POST['lokasi']

    data_lokasi = {
        "latitude": latitude,
        "longitude": longitude,
        "lokasi": lokasi,
    }
    print(data_lokasi)

    # save into patient table of another project
    createLokasi = requests.post('http://127.0.0.1:8000/api/lokasi/', data=data_lokasi)
    return redirect('form_lokasi')
