from django import forms
from .models import Workspace


class UploadFileFormSrc(forms.Form):
    title_src = forms.CharField(max_length=50)
    file_src = forms.FileField()

class CreateWorkspace(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = '__all__'
