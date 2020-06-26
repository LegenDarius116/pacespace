from django import forms
import datetime 

class CreateMissionForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(
        max_length=1000,
        required=False,
    )
    instructions = forms.FileField(
        label='Mission Instructions',
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            'class':'file_input',
        }),
    )
    due_date = forms.DateTimeField(
        label='Date Due',
        widget=forms.SelectDateWidget(),
    )

    def clean_date(self):
        date = self.cleaned_data['due_date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

class SubmitMissionForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        }))
    message = forms.CharField(max_length=500)