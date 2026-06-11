from django.shortcuts import render,redirect
from .forms import RegistrationForm,ProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.



def register(request):
    if request.method == 'POST':
        fm = RegistrationForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            Profile.objects.create(user=user)
            username = fm.cleaned_data.get('username')
            messages.success(
                request,
                f'Account created successfully for {username}!'
            )
            return redirect('users:login')
    else:
       fm = RegistrationForm()
    return render(request,'users/register.html',{'form':fm})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('myapp:index')

@login_required
def profile(request):
    profile = request.user.profile
    return render(request,'users/profile.html',{'profile':profile})



@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})