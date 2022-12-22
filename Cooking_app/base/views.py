from django.views.generic import TemplateView
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from .forms import SignupForm, LoginForm, ProfileForm
from .models import UserInfo, User


def home_anon(request):
    pass

def home_user(request):
    context = {
        'user_here': user
    }
    return render(request, 'index.html', context)

def signup_acc(request):
    template_name = 'signup.html'
    context = {}
    if request.method == 'POST':
        fullname = request.POST.get('fullname-signup-input')
        email = request.POST.get('email-signup-input')
        username = request.POST.get('username-signup-input')
        password1 = request.POST.get('password-signup-input')
        password2 = request.POST.get('repassword-signup-input')

        context = {
            'fullname': fullname,
            'email': email,
            'username': username,
        }
        
        # Case: Signup Information Validation
        dup_username = User.objects.filter(username=username)
        dup_email = User.objects.filter(email=email)
        if dup_email or dup_username or password1 != password2:
            if password1 != password2:
                messages.error(request, "Confirm password does not match.")
            if dup_username:
                messages.error(request, "Username was already taken.")
            if dup_email:
                messages.error(request, "Email was already signed up.")
            return render(request, template_name, context)
        user = User.objects.create(
            username=username,
            password=make_password(password1),
            email=email,
        )
        UserInfo.objects.create_user(
            user=user,
            fullname=fullname,
        )
        login(request, user)
        return redirect('/')
        print(request.POST.keys())
    return render(request, template_name, context)

def login_acc(request):
    context = {}
    template_name = 'login.html'
    if request.method == 'POST':
        username = request.POST.get('username-input')
        password = request.POST.get('password-input')
        context = {
            'username': username,
        }
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return render(request, 'index.html', {'user':user})

        messages.error(request, "Email or Password is incorrect.")
    return render(request, template_name, context)



# Starting from here 













"""
We will start again from here on now
"""

# class Authentication(TemplateView):
#     f_login = LoginForm
#     f_signup = SignupForm
#     context = {}
#     template_name = 'login_signup.html'

#     def get(self, request, *args, **kwargs):
#         self.context = {
#             'login_form': self.f_login(),
#             'signup_form': list(self.f_signup(request=request)),
#         }
#         return render(request, self.template_name, self.context)
    
#     def post(self, request, *args, **kwargs):
#         # Case: Login information is submitted
#         if 'login' in request.POST:
#             form = self.f_login(request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')
#                 user = authenticate(request, username=username, password=password)
#                 if user:
#                     login(request, user)
#                     return redirect('/')
#                 else:
#                     messages.error(request, "Email or Password is incorrect.")
#             self.context = {
#                 'login_form': form,
#                 'signup_form': list(self.f_signup(request=request)),
#             }
#         # Case: Signup information is submitted
#         if 'signup' in request.POST:
#             form = self.f_signup(request.POST, request=request)
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 return redirect('/')
#             self.context = {
#                 'login_form': self.f_login(),
#                 'signup_form': list(form),
#             }
#         return render(request, self.template_name, self.context)

# @method_decorator(login_required(login_url='accounts/login'), name='dispatch')
# class Exit(TemplateView):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('/')

# @method_decorator(login_required(login_url='accounts/login'), name='dispatch')
# class PersonalInfo(TemplateView):
#     form_class = ProfileForm
#     context = {}
#     template_name = 'profile.html'

#     def get_object(self, request):
#         return UserInfo.objects.get(user=request.user)

#     def get(self, request, *args, **kwargs):
#         user_info = self.get_object(request)
#         self.context = {
#             'user_info': self.form_class(request.POST, instance=user_info),
#             # 'user_recipes': UserRecipe.objects.filter(created_by=user_info.id),
#             #TODO: UserRecipe Model
#         }
#         return render(request, self.template_name, self.context)

#     def post(self, request, *args, **kwargs):
#         user_info = self.get_object(request)
#         form = self.form_class(request.POST, instance=user_info)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')

#         print(form)
#         """ self.context = {
#             'user_info': form,
#             # 'user_recipes': UserRecipe.objects.filter(created_by=user_info.id),
#             #TODO: UserRecipe Model
#         } """
#         return render(request, self.template_name, self.context)