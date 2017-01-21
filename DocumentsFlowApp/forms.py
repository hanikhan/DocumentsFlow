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
    name = forms.CharField(label='Subsemnatul(a)', max_length=100)
    function = forms.CharField(label='Avand titulatura/functia de:', max_length=100)
    department = forms.CharField(label='In cadrul Facultatii/Departamentului(pentru personalul administrativ) de', max_length=100)
    to = forms.CharField(label='Deplasarea la(se precizeaza localitatea/tara)', max_length=100)
    route = forms.CharField(label='Ruta', max_length=100)
    period = forms.CharField(label='Perioada cand are loc actiunea', max_length=100)
    periodOfDeparture = forms.CharField(label='Perioada de deplasare', max_length=100)
    vehicle = forms.CharField(label='Cu mijloc de transport', max_length=100)
    phoneNumber = forms.CharField(label='Numar telefon', max_length=100)
    email = forms.CharField(label='Adresa de email', max_length=100)
    scopeOfDeparture = forms.CharField(label='Scopul deplasarii', max_length=100)
    expenses = forms.CharField(label='Cheltuielile aferente mobilitatii sunt suportate de', max_length=100)
    cuantum = forms.CharField(label='Cuantum pe zi(diurna)', max_length=100)
    nrOfDays = forms.CharField(label='Numar de zile(diurna)', max_length=100)
    total = forms.CharField(label='Total(diurna)', max_length=100)
    accomodationCuantum = forms.CharField(label='Cuantum pe zi(cazare)', max_length=100)
    accomodationNrOfDays = forms.CharField(label='Numar de zile(cazare)', max_length=100)
    accomodationTotal = forms.CharField(label='Total(cazare)', max_length=100)
