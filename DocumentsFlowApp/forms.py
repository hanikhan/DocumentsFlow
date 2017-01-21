from django import forms

class UploadFileForm(forms.Form):
    abstract = forms.CharField(label='Abstract', max_length=100)
    keywords = forms.CharField(label='Cuvinte cheie', max_length=100)
    file = forms.FileField()

class UploadNewVersionForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=100)
    file = forms.FileField()

class CreateFileForm(forms.Form):
    doctitle = forms.CharField(label='Document title', max_length=100)
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', max_length=256)

