"""
Definition of urls for PictoryProject.
"""
from datetime import datetime
#from django.conf.urls import url
from django.urls import path,include
import django.contrib.auth.views
from django.contrib import admin
import Posting.views as post
import Member.views as member
from django.conf import settings #settings.py에서 설정한 내용 불러옴
from django.conf.urls.static import static  #urlpatterns 연결

#from django.urls import path 2.0에서 추가된 기능
#url(r'^sum/(?P<x>\d+)/$', views.mysum) : ()안에 d+가 부합한다면, x값을 view로 넘긴다


urlpatterns = [
    path('admin/', admin.site.urls),

    #-------------Regist, login, logout------------

    path('',member.home,name='home'),
    path('register/',member.register,name='register'),
    path('login/',member.loginview,name='login'),
    path('logout/',member.logoutview,name='logout'),
    path('<int:post_pk>/like',member.like_plus,name='like_plus'),
    path('<int:post_pk>/TMP',member.TMP_plus,name='TMP_plus'),
    path('myprofile/profile/signout',member.signoutview,name='signout'),
   
    #--------------posting----------------

    path('posting/',post.posting,name='posting'),
    path('posting/new/',post.new,name='new'),
    path('posting/create/',post.create,name='create'),
    path('posting/delete/<int:post_id>/',post.delete,name='delete_post'),
    path('posting/edit/<int:post_id>/',post.edit,name='edit_post'),
    path('posting/report/<int:post_pk>',post.report_post, name='report_post'),
   #path('posting/update/<int:post_id>/',post.update,name='update_post'),

    #----------------comment---------------
    path('comment/create/<int:post_pk>',post.comment_create,name='comment_create'),
    path('comment/delete/<int:comment_pk>',post.comment_delete,name='comment_delete'),
    path('comment/update/<int:comment_pk>',post.comment_update,name='comment_update'),
    
    #--------------profile----------------
    path('my_profile/profile/',member.myprofile,name='myprofile'),
    path('my_profile/profile/follow_list', member.myfollow_list_view, name = 'myfollow_list'),
    path('user_list/',member.user_list,name='user_list'),
    path('user_list/<int:profile_id>/profile/',member.user_detail,name='user_detail'),
    
    #---------------edit----------------
    path('my_profile/edit/',member.profile_edit,name='profile_edit'),
    path('my_profile/password_edit/',member.password_edit,name='password_edit'),

    #---------------follow---------------
    path('user_list/<int:profile_id>/follow/',member.follow_this_account,name='follow_acc'),
    path('user_list/<int:profile_id>/follow_del/',member.dont_follow,name='del_follow'),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
