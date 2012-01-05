from django.shortcuts import render_to_response, redirect
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.http import Http404
from django.template.context import RequestContext
from forms import PasswordInitialSetForm, SignupForm
from models import UserWithEmail

def initial_password_set(request, token, template_name='emailauth/set_password.html'):
    if request.method == 'POST':
        form = PasswordInitialSetForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth_authenticate(email = user.primary_email.email, password = form.cleaned_data['password'])
            print ("user backend %s" % user.backend)
            auth_login(request, user)
            return redirect('achievements')
    elif token:
        form = PasswordInitialSetForm(initial = {'token': token})
    else: 
        raise Http404('Need token')
    return render_to_response(template_name, {'form': form, 'token':token}, context_instance=RequestContext(request))

def signup(request, template_name='emailauth/signup.html', user_class=UserWithEmail):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_class.objects.create_user(**form.cleaned_data)
            redirect('will_notify')
    else:
        form = SignupForm()
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
