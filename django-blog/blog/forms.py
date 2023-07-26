from django import forms
from tinymce.widgets import TinyMCE

from blog.models import Post


class PostFormCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'publish_date']
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 25}),
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class PostFormUpdate(PostFormCreate):
    class Meta(PostFormCreate.Meta):
        fields = ['title', 'text', 'image']