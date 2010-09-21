from django import newforms as forms
import re

class AddForm(forms.Form):
    name = forms.CharField(required=True)
    birthday = forms.CharField(required=True)

    def clean_birthday(self):
        birthday = self.clean_data.get('birthday', '')
        if not re.search(r'^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$', birthday):
            raise forms.ValidationError("Invalid Date")

        return birthday

class PhotoForm(forms.Form):
    name = forms.CharField(required=True)
