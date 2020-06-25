from django import forms

class CreateProjectForm(forms.Form):
    description = forms.CharField(max_length=50)
    file_field = forms.FileField()
    due_date = forms.DateTimeField()

class SubmitProjectForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'multiple': True,
        }))
    message = forms.CharField(max_length=500)