from django import forms
from .models import Member,OngoingEvent

class MemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'email', 'membership_type', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

class OngoingEventForm(forms.ModelForm):
    class Meta:
        model = OngoingEvent
        fields = ['title', 'location', 'capacity', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }