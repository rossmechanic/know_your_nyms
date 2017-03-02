from django.shortcuts import *
from django.contrib.auth import authenticate, login

def signin(request):
    context = {'login_failed': False}
    if request.method == 'GET':
        return render(request, 'signin.html', context)
    elif request.method == 'POST':
        print request.POST
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # Rerenders page with login failed message.
            context['login_failed'] = True
            return render(request, 'signin.html', context)


def signup(request):
	return render(request, 'signup.html');