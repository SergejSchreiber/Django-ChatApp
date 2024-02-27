from django.http import HttpResponseRedirect
from django.shortcuts import render
from chat.models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login/')

def index(request):
    print(request.method)
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=2)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=2)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect })

def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password-repeat')
        if password != password_repeat:
            return render(request, 'auth/registration.html', {'wrongPassword': True})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/registration.html', {'wrongUser': True})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect('/chat/')

    return render(request, 'auth/registration.html')
