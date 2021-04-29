from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
    def save_user(self, request):
        obj = self.save(commit=False)
        obj.user = request.user
        obj.save()
        self.save()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
    def save_user(self, request):
        obj = self.save(commit=False)
        obj.user = request.user
        obj.save()
        self.save()

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)

# class SignUpPage(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=False)
#     email = forms.EmailField(max_length=254, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
