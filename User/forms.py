from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from User.models import Music, Folder


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class Musicform(forms.ModelForm):
    class Meta:
        model = Music
        exclude = ('created',)


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name','genre']


class AddMusicToFolderForm(forms.Form):
    selected_tracks = forms.ModelMultipleChoiceField(queryset=Music.objects.all(), widget=forms.CheckboxSelectMultiple)
