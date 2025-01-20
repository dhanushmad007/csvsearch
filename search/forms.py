from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Search by Username', max_length=100, required=False)
