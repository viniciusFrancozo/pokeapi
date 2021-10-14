from django import forms


class PokeForm(forms.Form):
    pokemon = forms.CharField(max_length=50, label='Pokemon Name')