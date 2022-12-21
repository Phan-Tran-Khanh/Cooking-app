from django.views.generic import TemplateView
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from .forms import SignupForm, LoginForm, ProfileForm
from .models import UserInfo, UserRecipe


@login_required(login_url='accounts/login')
def index(request):
    return render(request, 'index.html')

class Authentication(TemplateView):
    f_login = LoginForm
    f_signup = SignupForm
    context = {}
    template_name = 'login_signup.html'

    def get(self, request, *args, **kwargs):
        self.context = {
            'login_form': self.f_login(),
            'signup_form': list(self.f_signup(request=request)),
        }
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        # Case: Login information is submitted
        if 'login' in request.POST:
            form = self.f_login(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Email or Password is incorrect.")
            self.context = {
                'login_form': form,
                'signup_form': list(self.f_signup(request=request)),
            }
        # Case: Signup information is submitted
        if 'signup' in request.POST:
            form = self.f_signup(request.POST, request=request)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/')
            self.context = {
                'login_form': self.f_login(),
                'signup_form': list(form),
            }
        return render(request, self.template_name, self.context)

@method_decorator(login_required(login_url='accounts/login'), name='dispatch')
class Exit(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

@method_decorator(login_required(login_url='accounts/login'), name='dispatch')
class PersonalInfo(TemplateView):
    form_class = ProfileForm
    context = {}
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            self.context = {
                'user_info': UserInfo.objects.get(user=user_id),
                'user_recipes': UserRecipe.objects.filter(created_by=user_id),
            }
        except Exception as e:
            print("self.context")
            messages.error(request, message=e)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass