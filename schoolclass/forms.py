from django import forms

class ClassForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        min_length=1,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Class Name', 
            'class':'class_name_input'
            }),
    )
