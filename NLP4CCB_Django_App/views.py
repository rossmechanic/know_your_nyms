from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from forms import UserForm


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
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


def signout(request):
    logout(request)
    return redirect('/')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', context={'user_form': UserForm()})
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            return redirect('/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors
            return redirect('/')