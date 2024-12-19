from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'欢迎回来, {username}!')
                return redirect('page:home')
            else:
                messages.error(request, '用户名或密码错误')
    else:
        form = AuthenticationForm()
    return render(request, 'muggle/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功!')
            return redirect('page:home')
    else:
        form = UserCreationForm()
    return render(request, 'muggle/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'muggle/profile.html')

def logout_view(request):
    logout(request)
    messages.info(request, '您已安全退出')
    return redirect('page:home')
