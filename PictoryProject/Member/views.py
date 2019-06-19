from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LoginForm, ProfileShowForm, ProfileEditForm, PasswordEditForm
from .models import Profile,Following,Follower
import sys
sys.path.append("..")   #상위 폴더 import는 이렇게 한다
from Posting.models import Post,Comment

# Create your views here.

def home(request):
    if not request.user.is_authenticated: 
        data ={'username': request.user,'is_authenticated': request.user.is_authenticated}
        return render(request, 'Login/home.html', context={'data': data})
    else:  #여기서 프로필 보여주는걸로
        myfollowings=Following.objects.filter(owner=request.user)
        timeline=Post.objects.filter(user_id=request.user.id)
        for myfollowing in myfollowings:
            timeline = timeline | Post.objects.filter(user_id=myfollowing.following_profile_id)
        timeline = timeline.order_by('-pub_date')
        #timeline=Post.objects.all().order_by('-pub_date')
        comments=Comment.objects.all().order_by('-cub_date')
        allprofile=Profile.objects.all()
        data ={'username': request.user.username,'password':request.user.password,'is_authenticated': request.user.is_authenticated}
        profile=Profile.objects.get(owner_id=request.user.id)
        return render(request, 'Login/home.html', context={'data': data, 'profile':profile, 'timeline':timeline,'comments':comments,'allprofile':allprofile})

def loginview(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        name = request.POST['username']
        pwd=request.POST['password']
        #인증
        user = authenticate(username=name,password=pwd)
        if user is not None:
            login(request,user)
            return redirect("home")#시작페이지로 이동
            #return redirect("Posting/posting")
        else:
            return render(request,"Login/login_error.html")
    else: #GET방식이면 로그인 페이지로 이동
        form = LoginForm()
        return render(request, "Login/login.html", {"form": form})

def logoutview(request):
    logout(request)
    return redirect("/")

def register(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        profile_num = Profile.objects.count()
        only_admin = User.objects.count()
        if form.is_valid():
            if profile_num==0: #admin만 존재하고 그 프로필이 없을경우
                admin = User.objects.first()
                Profile.objects.create(owner_id=admin.id)
            new_user = User.objects.create_user(**form.cleaned_data)
            Profile.objects.create(owner_id=new_user.id, name = new_user.username, photo='images/basic_image.jpg') #기본 프로필사진 설정
            login(request,new_user)
            return redirect("/")#시작페이지로 이동
        else:
            return render(request, 'Login/register_error.html')
    else: #GET방식이면 회원가입 페이지로 이동
        form = UserForm()
        return render(request, "Login/register.html",{"form":form}) #'A'을 html에 B로 던지겠다

#--------------------MY-----------------------------------------------------------------------------------------------------------나 관리용
#--------------------Profile----------------------
@login_required # 로그인 여부를 검사하여 접근을 통제할 수 있다. 단, 함수형 뷰일때만
def myprofile(request):
    user=request.user
    profile = Profile.objects.get(owner_id = user.id)
    data ={'사진':profile.photo,'이름': profile.name,'Email' : profile.email,'phone':profile.phone,'소개말':profile.introduction,}
    return render(request, 'profile/myprofile.html', context={'data': data})
    
#--------------------edit-----------------------프로필, 비밀번호
@login_required 
def profile_edit(request):
     if request.method=="POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid() :
            user=request.user
            new_profile = Profile.objects.get(owner_id = user.id)
            if(request.POST.get('photo')!=''):
                new_profile.photo=request.FILES['photo']
            new_profile.name = form.cleaned_data['name']
            new_profile.email = form.cleaned_data['email']
            new_profile.phone = form.cleaned_data['phone']
            new_profile.introduction = form.cleaned_data['introduction']
            new_profile.save()
            return redirect("myprofile")
        else:
            return render(request,"profile/myprofile.html")
     else: #GET방식
        form = ProfileEditForm()
        user=request.user
        old_profile = Profile.objects.get(owner_id = user.id)
        return render(request, "profile/myprofile_edit.html", context = {"form": form, "old" : old_profile})

@login_required 
def password_edit(request):
     if request.method=="POST":
        form = PasswordEditForm(request.POST)
        user=request.user
        if form.is_valid() :
            user.set_password(form.cleaned_data['password'])
            user.save()
            logout(request)
            return redirect("home")
        else:
            return render(request,"profile/password_edit_error.html")
     else: #GET방식
        form = PasswordEditForm()
        return render(request, "profile/password_edit.html", {"form": form})


#------------------------follow시 view--------------------------------
@login_required
def follow_this_account(request,profile_id):
    userprofile = Profile.objects.get(id = profile_id)
    following=Following()  
    following.owner=request.user 
    following.following_profile=userprofile
    following.save()
    thisuserprofile=Profile.objects.get(owner_id=request.user.id)
    follower=Follower()
    follower.owner=User.objects.get(id=userprofile.owner_id)
    follower.follower_profile=thisuserprofile
    follower.save()
    return redirect('user_detail', profile_id)

#팔로우를 이미 했을 때를 검사해줘야 html내
def dont_follow(request,profile_id) :
    userprofile = Profile.objects.get(id=profile_id)
    following=Following.objects.get(owner=request.user,following_profile=userprofile)
    following.delete()
    thisuserprofile=Profile.objects.get(owner_id=request.user.id)
    follower=Follower.objects.get(owner=userprofile.owner_id,follower_profile=thisuserprofile)
    follower.delete()

    return redirect('user_detail', profile_id)

def myfollow_list_view(request) :
    user = request.user
    userprofile = Profile.objects.get(owner_id = user.id)
    myfollowings=Following.objects.filter(owner=request.user)
    myfollowers=Follower.objects.filter(owner=request.user)
    context = {'followers': myfollowers, 'followings' : myfollowings}
    return render(request, 'Profile/myfollow_list.html', context)

#-----------------------------------------Others-------------------------------------------------------------타인에게 접속용

def user_list(request):
    profiles=Profile.objects.all()
    return render(request, 'user_list.html', context={'profiles':profiles})

@login_required
def user_detail(request, profile_id):
    profile = Profile.objects.get(id = profile_id)
    followed = Following.objects.filter(owner=request.user)
    followed = followed.filter(following_profile = profile.id)
    data ={'id':profile.id, '사진':profile.photo,'이름': profile.name,'Email' : profile.email,'phone':profile.phone,'소개말':profile.introduction,}
    return render(request, 'OthersProfile/user_detail.html', context={'data': data, 'profile':profile,'followed':followed})

@login_required
def userfollow_list_view(request,user_pk) :
    ...

@login_required
def user_detail_posts  (request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    profile = Profile.objects.get(owner_id = user.id)
    data ={'owner':profile.owner_id,'이름': profile.name,'Email' : profile.email,'phone':profile.phone,'소개말':profile.introduction,}
    return render(request, 'OthersProfile/user_detail_posts.html', context={'data': data})

def like_plus(request,post_pk):
    post=Post.objects.get(id=post_pk)
    post.like+=1
    post.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def TMP_plus(request,post_pk):
    post=Post.objects.get(id=post_pk)
    post.TMP+=1
    post.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def signoutview(request):
    delete_user=User.objects.get(id=request.user.id)
    logout(request)
    delete_user.delete()

    return redirect("home")