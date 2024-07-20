from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm, LoginForm, BlogForm, EditProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog, Profile
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request,'blog/home.html',{'blogs':blogs})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user, image=form.cleaned_data.get('image'))
            profile.save()
            messages.success(request, "CONGRATULATION, You are Registered!")

            # Ensure the 'Author' group exists, if not, create it
            group, created = Group.objects.get_or_create(name='Author')
            user.groups.add(group)

            return HttpResponseRedirect("/login/")
    else:
        form = SignUpForm()
    
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=uname, password=pwd)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


from django.core.exceptions import ObjectDoesNotExist


def dashboard(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            print(profile)
            profile_image_url = profile.image.url if profile.image else settings.MEDIA_URL + 'profile_pics/default.jpg'
            print(profile_image_url)
        except ObjectDoesNotExist:
            profile_image_url = settings.MEDIA_URL + 'profile_pics/default.jpg'

        blogs = Blog.objects.filter(author=request.user.first_name)
        context = {
            'blogs': blogs,
            'profile_image': profile_image_url,
            'full_name': f'{request.user.first_name} {request.user.last_name}',
            'groups': request.user.groups.all()
        }
        print(context)  # Print the context for debugging purposes
        return render(request, 'blog/dashboard.html', context)
    else:
        return HttpResponseRedirect('login')  # Redirect to the login page if user is not authenticated

        
def add_blog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                cont = form.cleaned_data['cont']
                author = request.user.first_name
                Blog.objects.create(title=title, cont=cont, author=author)
                return HttpResponseRedirect('/dashboard/')  # Redirect to the dashboard after successful submission
        else:
            form = BlogForm()
        return render(request, 'blog/addblog.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')
def update_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blog = Blog.objects.get(pk=id)
            form = BlogForm(request.POST,instance = blog)
            if form.is_valid():
                form.save()
        else:
            pi = Blog.objects.get(pk=id)
            form = BlogForm(instance=pi)
        return render(request, 'blog/updateblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blog = Blog.objects.get(pk=id)
            blog.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = user.get_full_name()
        return render(request, 'blog/profile.html',{'full_name':full_name})
    else:
        return HttpResponseRedirect('/')

@login_required  # Decorator to ensure user is authenticated
def updateprofile(request):
    if request.method == "POST":
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile')
    else:
        form = EditProfile(instance=request.user)


    return render(request, 'blog/editprofile.html', {'form': form, 'user': request.user})


def changepassword(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user = request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/profile')
        else:
            fm = PasswordChangeForm(user = request.user)
        return render(request, 'blog/changepwd.html',{'form':fm})
    else:
        return HttpResponseRedirect('/')