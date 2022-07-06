from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='Nome:', max_length=20)
