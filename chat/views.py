from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from chat.models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login/')

def index(request):
    """
    Render the chat HTML view.

    This view renders the chat HTML page. If the request method is POST, it handles the submission
    of new chat messages. It creates a new message object and returns its serialized JSON representation
    as a JsonResponse. Otherwise, it retrieves existing chat messages and renders them along with the chat
    HTML page.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with chat messages.
    """
    if request.method == 'POST':
        myChat = Chat.objects.get(id=2)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [ new_message ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=2)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    """
    Handle user login.

    This view handles user authentication and login. If the request method is POST, it attempts to
    authenticate the user based on the provided username and password. If authentication is successful,
    the user is logged in and redirected to the requested page. Otherwise, the login page is rendered
    with an error message.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered login page.
    """
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
    """
    Handle user registration.

    This view handles user registration. If the request method is POST, it validates the registration
    form data, creates a new user, logs in the user, and redirects to the chat page upon successful
    registration. If the form data is invalid or the username already exists, the registration page
    is rendered with appropriate error messages.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered registration page.
    """
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

def logout_view(request):
    """
    Handle user logout.

    This view handles user logout. It logs out the current user and redirects to the chat page.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponseRedirect: Redirect to the chat page.
    """
    logout(request)
    return HttpResponseRedirect('/chat/')