from django import forms
from .models import Category



class PersonalPreferencesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.filter(is_main=True)
        for category in categories:
            self.fields[category.slug] = forms.BooleanField(label=category.name, required=False, widget=forms.CheckboxInput(attrs={'class': 'shadow-default switch', 'id': 'finances'}))