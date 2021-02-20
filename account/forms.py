from django import forms
from django.contrib.auth.models import User
from posts.models import Post
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('This email already exists!')
        return email

    def clean(self):
        cleaned_data=super().clean()
        p1 = cleaned_data['password1']
        p2 = cleaned_data['password2']
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('passowrds must match!')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'age')
