from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment, Report
from django.contrib.auth.models import User
import sys
sys.path.append("..")   #상위 폴더 import는 이렇게 한다
from Member.models import Profile 


# Create your views here.

def posting(request):
    postings=Post.objects.filter(user_id=request.user.id).order_by('-pub_date') #현재 유저의 포스팅만 가져오기
    #postings=Post.objects.all().order_by('-pub_date')  #이건 타임라인에서 쓸 것
    profile=Profile.objects.get(owner_id=request.user.id)
    comment = Comment()
    comment = Comment.objects.all()
    allprofile = Profile.objects.all()
    return render(request, 'Posting/My_posting_list.html',{'postings':postings, 'profile':profile,'all_comment':comment,'who':allprofile}) #dictionary 여러개 보내는 거 되나? 하나안엔 되네

def new(request):
    return render(request,'Posting/new.html')

def create(request):
    post = Post()
    if request.POST.get('image') == '':
        return redirect("new")
    elif request.POST['title'] =='' :
        return redirect("new")
    post.title = request.POST.get('title',False)
    post.description = request.POST.get('des',False)
    post.pub_date = timezone.datetime.now()
    post.image = request.FILES['image']
    post.like=0
    post.TMP=0
    post.user=Profile.objects.get(owner_id = request.POST['user_id'])
    post.save()
    return redirect("posting")

def delete(request, post_id):
    post=get_object_or_404(Post, pk=post_id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit(request, post_id):
     next_path = request.GET.get('next')
     if request.method=="POST":
        post=get_object_or_404(Post,pk=post_id)
        post.title = request.POST.get('title',False)
        post.description = request.POST.get('des',False)
        post.pub_date = timezone.datetime.now()
        if(request.POST.get('image')!=''):
            post.image=request.FILES['image']
        post.save()
        return redirect(next_path)
     else :
        old_post = get_object_or_404(Post,pk=post_id)
        return render(request, "Posting/edit.html", {"old" : old_post,'nextpage' : next_path})


#--------------------------comment-------------------------------------//대화형식으로 만들어보자

def comment_create(request,post_pk):
    #cur_post = get_object_or_404(Post, id = post_pk )
    new_comment = Comment()
    new_comment.body = request.POST['body']
    new_comment.cub_date = timezone.datetime.now()
    new_comment.post =  Post.objects.get(id = post_pk)
    #new_comment.owner = Profile.objects.get(owner_id = new_comment.post.user_id)
    comment_user=request.user
    comment_user_profile=Profile.objects.get(owner_id=comment_user.id)
    new_comment.owner = comment_user_profile
    new_comment.save() 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def comment_update(request,comment_pk) :
    next_path = request.GET.get('next')
    if request.method=="POST":
        updated = Comment.objects.get(id = comment_pk)
        updated.body = request.POST['body']
        updated.cub_date = timezone.datetime.now()
        updated.save()
        return redirect(next_path)
        #return redirect("posting")
    else :
        updated = Comment.objects.get(id = comment_pk)
        return render(request,"Comments/comment_update.html",{'comment':updated,'nextpage' : next_path})

def comment_delete(request,comment_pk):
    delcomment = Comment.objects.get(id = comment_pk)
    delcomment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #cur_comment = get_object_or_404(Comment,id = comment_pk)


#------------------------report--------------------------------------

def report_post(request, post_pk) :
    next_path = request.GET.get('next')
    if request.method == "POST" :
        form = Report()
        form.title = request.POST['title']
        form.content = request.POST['content']
        form.rub_date = timezone.datetime.now()
        form.post = Post.objects.get(id = post_pk)
        form.save()
        return redirect(next_path)
    else :
        form = Report()
        reportone = Post.objects.get(id = post_pk)
        return render(request, "Posting/report_post_page.html",{'form' : form, 'post' : reportone,'nextpage' : next_path})
    