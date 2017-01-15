from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class CreateFileForm(forms.Form):
    doctitle = forms.CharField(label='Document title', max_length=100)
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', max_length=256)

