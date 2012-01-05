from django.shortcuts import render_to_response, redirect
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.http import Http404
from django.template.context import RequestContext
from forms import PasswordInitialSetForm

def initial_password_set(request, token, template_name='emailauth/set_password.html'):
    if request.method == 'POST':
        form = PasswordInitialSetForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth_authenticate(email = user.primary_email.email, password = form.cleaned_data['password'])
            print ("user backend %s" % user.backend)
            auth_login(request, user)
            return redirect(dispatch)
    elif token:
        form = PasswordInitialSetForm(initial = {'token': token})
    else: 
        raise Http404('Need token')
    return render_to_response(template_name, {'form': form, 'token':token}, context_instance=RequestContext(request))
    
def dispatch(request):
    user = request.user
    if user.is_authenticated():
        return redirect(user.next_step())
    else:
        return redirect('login')
