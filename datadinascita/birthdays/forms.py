from django import newforms as forms

class AddForm(forms.Form):
    name = forms.CharField()
    birthday = forms.CharField()