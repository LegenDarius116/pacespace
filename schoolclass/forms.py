from django import forms

class ClassForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        label='Add New Class',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Class Name', 
            'class':'class_name_input',
        }),
    )
