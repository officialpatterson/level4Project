# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import UserForm

def overview(request):
    context = RequestContext(request)
    return render_to_response('application/overview.html',{}, context)

def entity(request):
    context = RequestContext(request)
    return render_to_response('application/Entity-Viewer.html',{}, context)

def search(request):
    context = RequestContext(request)
    return render_to_response('application/search.html',{}, context)

def system(request):
    context = RequestContext(request)
    return render_to_response('application/system.html',{}, context)

def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/app/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('application/login.html', {'msg':'Incorrect Login Details'}, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('application/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/app/')

@login_required
def notifications(request):
    context = RequestContext(request)
    return render_to_response('application/notifications.html',{}, context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        else:
            print user_form.errors


    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'application/register.html',
            {'user_form': user_form, 'registered': registered},
            context)
