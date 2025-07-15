from django import forms
from .models import RoomBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'Select Check-in Date',
                'autocomplete': 'off'
            }),
            'check_out': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'Select Check-out Date',
                'autocomplete': 'off'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out must be after check-in date.")
        return cleaned_data
