from django import forms
from .models import Post

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )