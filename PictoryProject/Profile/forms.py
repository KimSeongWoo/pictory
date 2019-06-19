from django import forms
from django.forms import ModelForm
from .models import Profile

class ProfileStateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'myid' ,'myname', 'myemail', 'introduction','phonenum']

class ProfileModifyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['myname','myemail','introduction','phonenum','leavebool']
