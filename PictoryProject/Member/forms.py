from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from Member.models import Profile

class UserForm(ModelForm):
    password=forms.CharField(max_length=30,widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

#-------------profile--------------

class ProfileShowForm(ModelForm): #변경도 일단은 동일하게
    class Meta:
        model = Profile
        fields = ['name','email','phone','introduction']

class ProfileEditForm(ModelForm) :
    class Meta:
        model = Profile
        fields = ['photo','name','email','phone','introduction'] 
        
        #leaveparty는 차후 수정, isactive 필드를 false하는것이 바람직하다고 함

#pw변경은 set_password(raw_password)을 사용
class PasswordEditForm(ModelForm) :
    class Meta :
        model = User
        fields = ["password"]


