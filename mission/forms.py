from django import forms
from datetime import date

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
        required=False,
    )
    date_due = forms.DateField(
        label='Due Date',
        initial=date.today(),
        widget=forms.SelectDateWidget(),
    )

    # def clean_date(self):
    #     date = self.cleaned_data['due_date']
    #     if date < date.today():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #     return date
    
    def is_valid(self):
        valid = super(CreateMissionForm, self).is_valid()
        if not valid:
            print(self.errors)
        return valid

class SubmissionForm(forms.Form):
    file_submission = forms.FileField(
        label='Submission',
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            'class':'file_input',
        })
    )
    message = forms.CharField(
        max_length=500,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Leave a message',
            }
        )
    )

    def is_valid(self):
        valid = super(SubmissionForm, self).is_valid()
        if not valid:
            print(self.errors)
        return valid