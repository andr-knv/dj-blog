from django import forms
from tinymce.widgets import TinyMCE

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 25}),
        }
