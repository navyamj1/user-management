from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.contrib import messages
import os
from django.conf import settings
from.models import CustomUser as User
User = get_user_model() 
# Create your views here.
@login_required(login_url='login')
# def HomePage(request):
#     return render (request,'home.html')
def HomePage(request):
    user = request.user  # Retrieve the logged-in user
    context = {
        'user': user  # Pass the user object to the template
    }
    return render(request, 'home.html', context)



 
#  profile_picture = request.FILES.get('profile_picture')




def SignupPage(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST.get('userType') 

        if password1 != password2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            try:
                if profile_picture:
                    media_dir = os.path.join(settings.BASE_DIR, 'media', 'profiles')
                    os.makedirs(media_dir, exist_ok=True)
                    filepath = os.path.join(media_dir, profile_picture.name)
                    with open(filepath, 'wb+') as f:
                        for chunk in profile_picture.chunks():
                            f.write(chunk)
                    profile_path = f'/media/profiles/{profile_picture.name}'
                # Create a user object
                my_user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    profile_picture=profile_path
                )

                # Set user password
                my_user.set_password(password1)
                my_user.save() 

                # Assign user to the selected group (patient or doctor)
                group = Group.objects.get(name=user_type)
                group.user_set.add(my_user)

                return redirect('login')

            except Group.DoesNotExist:
                messages.error(request, 'Group does not exist. Please select a valid group.')
                # Redirect back to signup page or handle the error appropriately
                return redirect('signup')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                # Redirect back to signup page or handle the error appropriately
                return redirect('signup')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')