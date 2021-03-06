from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text',)
        fields = ('title','text',)
    
class UserForm(forms.Form):
    sinaido = forms.CharField(label='親愛度',max_length=100)
    voltage = forms.CharField(label='ボルテージ',max_length=100)
    accuracy = forms.CharField(label='精度',max_length=100)
    criteria = forms.CharField(label='基準レベル',max_length=100)
    increase_rate = forms.CharField(label='精度低下率',max_length=100)
